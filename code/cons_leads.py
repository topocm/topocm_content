import kwant
import numpy as np

class ConservationInfiniteSystem(kwant.builder.InfiniteSystem):
    def __init__(self, lead, projector_list):
        """A lead with a conservation law. Lead modes have definite values of the conservation law observable."""
        self.__dict__ = lead.__dict__
        self.projector_list = projector_list
        assert np.allclose(sum([projector.dot(projector.conj().T) for projector in projector_list]),
                           np.eye(max(projector_list[0].shape)))

    def modes(self, energy=0, args=()):
        from kwant import physics   # Putting this here avoids a circular import.
        projector_list = self.projector_list

        ham = self.cell_hamiltonian(args)
        hop = self.inter_cell_hopping(args)
        shape = ham.shape
        assert len(shape) == 2
        assert shape[0] == shape[1]
        # Subtract energy from the diagonal.
        ham.flat[::ham.shape[0] + 1] -= energy
        
        def block_diag(*matrices):
            """Construct a block diagonal matrix out of the input matrices. Replacement for
            scipy.linalg.block_diag."""
            rows, cols = np.sum([mat.shape for mat in matrices], axis=0)
            b_mat = np.zeros((rows,cols), dtype='complex')
            rows, cols = 0, 0
            for mat in matrices:
                new_rows, new_cols = np.sum([mat.shape, (rows, cols)], axis=0)
                b_mat[rows:new_rows, cols:new_cols] = mat
                rows, cols = new_rows, new_cols
            return b_mat        

        # Project out blocks
        ham_blocks = []
        hop_blocks = []
        for projector in projector_list:
            ham_blocks.append(projector.T.conj().dot(ham).dot(projector))
            hop_blocks.append(projector.T.conj().dot(hop).dot(projector))
        
        # Check that h, t are actually block-diagonal
        projector_matrix = np.hstack(projector_list)
        assert np.allclose(projector_matrix.dot(block_diag(*ham_blocks)).dot(projector_matrix.conj().T),ham)
        assert np.allclose(projector_matrix.dot(block_diag(*hop_blocks)).dot(projector_matrix.conj().T),hop)

        # symm_modes[i] is a tuple containing PropagatingModes and StabilizedModes objects for block i.
        symm_modes = [physics.modes(h, t) for h, t in zip(ham_blocks, hop_blocks)]

        # Get wavefunctions to correct size and transform them back to the
        # tight binding basis.
        wave_functions = [modes[0].wave_functions for modes in symm_modes]
        for i, wave_function in enumerate(wave_functions):
            wave_functions[i] = projector_list[i].dot(wave_function)
        
        def rearrange(arr_list):
            """Takes a list of arrays and splits each array in half along a vertical line, into
            a left and a right half. Combines all the left halves into one array, same for the
            right halves, and then joins them together into a single array."""
            if len(arr_list[0].shape) == 1: # If list of 1D arrays
                lis = [np.split(arr, 2) for arr in arr_list if arr.size]  # Skip empty arrays
            else: # Else 2D arrays
                lis = [np.split(arr, 2, axis=1) for arr in arr_list if arr.size]  # Skip empty arrays
            if not lis:  # If lis empty
                return np.hstack(arr_list)
            else:
                lefts, rights = zip(*lis)
                return np.hstack(lefts + rights)
            
        # Reorder by direction of propagation
        wave_functions = rearrange(wave_functions)
        momenta = rearrange([modes[0].momenta for modes in symm_modes])
        velocities = rearrange([modes[0].velocities for modes in symm_modes])
        
        nmodes = [modes[1].nmodes for modes in symm_modes]
        prop_modes = kwant.physics.PropagatingModes(wave_functions, velocities, momenta)
        # Store the number of modes per block as an attribute.
        # nmodes[i] is the number of left or right moving modes in block i.
        prop_modes.block_nmodes = nmodes

        # Pick out left moving, right moving and evanescent modes from vecs and
        # vecslmbdainv, and combine into block diagonal matrices.
        # vecs[i] is a tuple, such that vecs[i][0] is the left-movers, vecs[i][1] right-movers
        # and vecs[i][2] the evanescent states for block i. vecslmbdainv has the same structure.
        vecs = [(modes[1].vecs[:, :n], modes[1].vecs[:, n:(2*n)], modes[1].vecs[:, (2*n):]) for n, modes in 
                zip(nmodes, symm_modes)]
        vecslmbdainv = [(modes[1].vecslmbdainv[:, :n], modes[1].vecslmbdainv[:, n:(2*n)], 
                         modes[1].vecslmbdainv[:, (2*n):]) for n,modes in zip(nmodes, symm_modes)]

        lvecs, rvecs, evvecs = zip(*vecs)
        lvecs = block_diag(*lvecs)
        rvecs = block_diag(*rvecs)
        evvecs = block_diag(*evvecs)
        lvecslmbdainv, rvecslmbdainv, evvecslmbdainv = zip(*vecslmbdainv)
        lvecslmbdainv = block_diag(*lvecslmbdainv)
        rvecslmbdainv = block_diag(*rvecslmbdainv)
        evvecslmbdainv = block_diag(*evvecslmbdainv)
        
        vecs = np.hstack((lvecs,rvecs,evvecs))
        vecslmbdainv = np.hstack((lvecslmbdainv,rvecslmbdainv,evvecslmbdainv))
        
        # Combine sqrt_hops into a block diagonal matrix. If it is None, replace with identity matrix
        sqrt_hops = []
        for modes, projector in zip(symm_modes, projector_list):
            if modes[1].sqrt_hop is None:
                sqrt_hops.append(np.eye(min(projector.shape)))
            else:
                sqrt_hops.append(modes[1].sqrt_hop)
        # Gather into a matrix and project back to TB basis
        sqrt_hops = (np.hstack(projector_list)).dot(block_diag(*sqrt_hops))

        stab_modes = kwant.physics.StabilizedModes(vecs, vecslmbdainv, sum(nmodes), sqrt_hops)

        return prop_modes, stab_modes


class SymmetricSMatrix(kwant.solvers.common.SMatrix):
    def __init__(self, SMatrix):
        """A scattering matrix that understands leads with conservation laws, i. e.
        one may consider subblocks corresponding to definite values of the conservation
        law. """
        self.__dict__ = SMatrix.__dict__
        # in_offsets marks beginnings and ends of blocks in the scattering matrix
        # corresponding to the in leads. The end of the block corresponding
        # to lead i is taken as the beginning of the block of i+1.
        # Same for out leads. For each lead block of the scattering matrix,
        # we want to pick out the computed blocks of the conservation law.
        # The offsets of these symmetry blocks are stored in block_offsets,
        # for all leads.
        # List of lists containing the sizes of symmetry blocks in all
        # leads. block_sizes[i][j] is the number of left or right moving
        # modes in symmetry block j of lead i. len(block_sizes[i]) is
        # the number of blocks in lead i.
        leads_block_sizes = []
        for info in self.lead_info:
            # If a lead does not have block structure, append None.
            leads_block_sizes.append(getattr(info, 'block_nmodes', None))
        self.leads_block_sizes = leads_block_sizes
        block_offsets = []
        for lead_block_sizes in self.leads_block_sizes: # Cover all leads
            if lead_block_sizes is None:
                block_offsets.append(lead_block_sizes)
            else:
                block_offset = np.zeros(len(lead_block_sizes)+1, int)
                block_offset[1:] = np.cumsum(lead_block_sizes)
                block_offsets.append(block_offset)
        # Symmetry block offsets for all leads - or None if lead does not have blocks.
        self.block_offsets = block_offsets
        # Pick out symmetry block offsets for in and out leads
        self.in_block_offsets = np.array(self.block_offsets)[list(self.in_leads)]
        self.out_block_offsets = np.array(self.block_offsets)[list(self.out_leads)]
        # Block j of in lead i starts at in_block_offsets[i][j]

    def out_block_coords(self, lead_out):
        """Return a slice with the rows in the block corresponding to lead_out.
        """
        if type(lead_out) is tuple:
            lead_ind, block_ind = lead_out
            lead_ind = self.out_leads.index(lead_ind)
            return slice(self.out_offsets[lead_ind]+self.out_block_offsets[lead_ind][block_ind],
                         self.out_offsets[lead_ind]+self.out_block_offsets[lead_ind][block_ind+1])
        else:
            lead_out = self.out_leads.index(lead_out)
            return slice(self.out_offsets[lead_out],
                         self.out_offsets[lead_out + 1])

    def in_block_coords(self, lead_in):
        """Return a slice with the columns in the block corresponding to lead_in.
        """
        if type(lead_in) is tuple:
            lead_ind, block_ind = lead_in
            lead_ind = self.in_leads.index(lead_ind)
            return slice(self.in_offsets[lead_ind]+self.in_block_offsets[lead_ind][block_ind],
                         self.in_offsets[lead_ind]+self.in_block_offsets[lead_ind][block_ind+1])
        else:
            lead_in = self.in_leads.index(lead_in)
            return slice(self.in_offsets[lead_in],
                     self.in_offsets[lead_in + 1])
        
    def transmission(self, lead_out, lead_in):
        """Return transmission from lead_in to lead_out.
        """
        if (type(lead_in) is not tuple) and (type(lead_out) is not tuple):
            return super().transmission(lead_out, lead_in)
        else:
            return np.linalg.norm(self.submatrix(lead_out, lead_in)) ** 2