import numpy as np

class PHModesLead(object):
    def __init__(self, lead, P_matrix):
        self._orig_lead = lead
        self.P_matrix = P_matrix

        assert P_matrix.shape[0] == P_matrix.shape[0]

    def cell_hamiltonian(self, args=(), sparse=False):
        return self._orig_lead.cell_hamiltonian(args, sparse)

    def inter_cell_hopping(self, args=(), sparse=False):
        return self._orig_lead.inter_cell_hopping(args, sparse)

    def selfenergy(self, energy=0, args=()):
        return self._orig_lead.selfenergy(energy=energy, args=args)

    def modes(self, energy=0, args=()):
        prop_modes, stab_modes = self._orig_lead.modes(energy=energy, args=args)

        num_orbs = self.P_matrix.shape[0]

        assert num_orbs % 2 == 0

        wf_size = prop_modes.wave_functions.shape[0]
        assert  wf_size % num_orbs == 0

        num_modes = prop_modes.wave_functions.shape[1] // 2

        # Double check if the lead actually allows for separation of
        # electrons and holes
        eh_sigma_z = np.diag(([1., -1] * (num_orbs // 2))
                             * (wf_size // num_orbs))

        h_0 = self.cell_hamiltonian(args=args)
        h_hop = self.inter_cell_hopping(args=args)

        if (np.max(np.dot(eh_sigma_z, h_0) -
                   np.dot(h_0, eh_sigma_z)) > 1e-10 or
            np.max(np.dot(eh_sigma_z, h_hop) -
                   np.dot(h_hop, eh_sigma_z)) > 1e-10):
            raise RuntimeError("This lead does not allow for separation of "
                               "electrons and holes")

        # Find the electron modes
        e_in = []
        h_in = []
        for i in range(num_modes):
            mode = prop_modes.wave_functions[:, i]

            e_dens = 0
            for j in range(0, num_orbs, 2):
                e_dens += np.sum(abs(mode[j::num_orbs])**2)

            h_dens = 0
            for j in range(1, num_orbs, 2):
                h_dens += np.sum(abs(mode[j::num_orbs])**2)

            if e_dens > h_dens and abs(h_dens) < 1e-8:
                e_in.append(i)
            elif h_dens > e_dens and abs(e_dens) < 1e-8:
                h_in.append(i)
            else:
                raise RuntimeError("Unexpected mixture of e and h")

        e_out = []
        h_out = []
        for i in range(num_modes, num_modes*2):
            mode = prop_modes.wave_functions[:, i]

            e_dens = 0
            for j in range(0, num_orbs, 2):
                e_dens += np.sum(abs(mode[j::num_orbs])**2)

            h_dens = 0
            for j in range(1, num_orbs, 2):
                h_dens += np.sum(abs(mode[j::num_orbs])**2)

            if e_dens > h_dens and abs(h_dens) < 1e-8:
                e_out.append(i)
            elif h_dens > e_dens and abs(e_dens) < 1e-8:
                h_out.append(i)
            else:
                raise RuntimeError("Unexpected mixture of e and h")

        prop_modes.n_e_in = len(e_in)
        prop_modes.n_e_out = len(e_out)
        prop_modes.n_h_in = len(h_in)
        prop_modes.n_h_out = len(h_out)

        # Reshuffle the modes so that we first have electrons, then holes
        if num_modes:
            wf = prop_modes.wave_functions
            wf[:, :num_modes] = wf[:, e_in + h_in]
            wf[:, num_modes:] = wf[:, e_out + h_out]

            smodes = stab_modes.vecs
            smodes[:, :num_modes] = smodes[:, e_in + h_in]
            smodes[:, num_modes:2*num_modes] = smodes[:, e_out + h_out]

            smodes = stab_modes.vecslmbdainv
            smodes[:, :num_modes] = smodes[:, e_in + h_in]
            smodes[:, num_modes:2*num_modes] = smodes[:, e_out + h_out]

        if energy == 0:
            # For E=0 we can make the scattering matrix particle-hole symmetric
            # Take the electrons, and apply the particle-hole operation on
            # them to get holes!

            ph_matrix = np.zeros((wf_size, wf_size))
            for i in range(0, wf_size, num_orbs):
                ph_matrix[i:i+num_orbs, i:i+num_orbs] = self.P_matrix

            wf = prop_modes.wave_functions
            wf[:, num_modes/2:num_modes] = np.dot(ph_matrix,
                                                  wf[:, :num_modes/2].conj())
            wf[:, num_modes + num_modes/2:] = np.dot(ph_matrix,
                            wf[:, num_modes:num_modes + num_modes/2].conj())

            smodes = stab_modes.vecs
            smodes[:, num_modes/2:num_modes] = -np.dot(ph_matrix,
                                        smodes[:, :num_modes/2].conj())
            smodes[:, num_modes + num_modes/2:2 * num_modes] = -np.dot(
                ph_matrix, smodes[:, num_modes:num_modes + num_modes/2].conj())

            smodes = stab_modes.vecslmbdainv
            smodes[:, num_modes/2:num_modes] = np.dot(ph_matrix,
                                            smodes[:, :num_modes/2].conj())
            smodes[:, num_modes + num_modes/2:2 * num_modes] = np.dot(
                ph_matrix, smodes[:, num_modes:num_modes + num_modes/2].conj())

        return prop_modes, stab_modes


def make_ph_lead(sys, lead_num, P_matrix):
    """Makes the lead lead_num in sys particle-hole symmetric, with
    distinct electrons and holes.  The particle-hole symmetry P =
    P_matrix K is used for this.

    Note: Only works for leads that are not superconducting. Be
    careful to give the correct P_matrix, otherwise the result will be
    wrong!"""

    sys.leads[lead_num] = PHModesLead(sys.leads[0], P_matrix)


def conductance(smatrix, lead_num):
    """Calculate the Andreev conductance in lead lead_num
    """

    S = smatrix.submatrix(lead_num, lead_num)
    N_e = smatrix.lead_info[lead_num].n_e_in

    r_ee = S[:N_e, :N_e]
    r_he = S[:N_e, N_e:]

    return (N_e - np.dot(r_ee, r_ee.T.conj()).trace() +
            np.dot(r_he, r_he.T.conj()).trace() ).real
