"""A package for computing Pfaffians"""


import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
import math
import cmath


def householder_real(x):
    """(v, tau, alpha) = householder_real(x)

    Compute a Householder transformation such that
    (1-tau v v^T) x = alpha e_1
    where x and v a real vectors, tau is 0 or 2, and
    alpha a real number (e_1 is the first unit vector)
    """

    assert x.shape[0] > 0

    sigma = x[1:] @ x[1:]

    if sigma == 0:
        return (np.zeros(x.shape[0]), 0, x[0])
    else:
        norm_x = math.sqrt(x[0]**2+sigma)

        v = x.copy()

        # depending on whether x[0] is positive or negatvie
        # choose the sign
        if x[0] <= 0:
            v[0] -= norm_x
            alpha = +norm_x
        else:
            v[0] += norm_x
            alpha = -norm_x

        v /= np.linalg.norm(v)

        return (v, 2, alpha)


def householder_complex(x):
    """(v, tau, alpha) = householder_real(x)

    Compute a Householder transformation such that
    (1-tau v v^T) x = alpha e_1
    where x and v a complex vectors, tau is 0 or 2, and
    alpha a complex number (e_1 is the first unit vector)
    """
    assert x.shape[0] > 0

    sigma = np.conj(x[1:]) @ x[1:]

    if sigma == 0:
        return (np.zeros(x.shape[0]), 0, x[0])
    else:
        norm_x = cmath.sqrt(x[0].conjugate()*x[0]+sigma)

        v = x.copy()

        phase = cmath.exp(1j*math.atan2(x[0].imag, x[0].real))

        v[0] += phase*norm_x

        v /= np.linalg.norm(v)

    return (v, 2, -phase*norm_x)


def skew_tridiagonalize(A, overwrite_a=False, calc_q=True):
    """ T, Q = skew_tridiagonalize(A, overwrite_a, calc_q=True)

    or

    T = skew_tridiagonalize(A, overwrite_a, calc_q=False)

    Bring a real or complex skew-symmetric matrix (A=-A^T) into
    tridiagonal form T (with zero diagonal) with a orthogonal
    (real case) or unitary (complex case) matrix U such that
    A = Q T Q^T
    (Note that Q^T and *not* Q^dagger also in the complex case)

    A is overwritten if overwrite_a=True (default: False), and
    Q only calculated if calc_q=True (default: True)
    """

    # Check if matrix is square
    assert A.shape[0] == A.shape[1] > 0
    # Check if it's skew-symmetric
    assert abs((A+A.T).max()) < 1e-14

    n = A.shape[0]
    A = np.asarray(A)  # the slice views work only properly for arrays

    # Check if we have a complex data type
    if np.issubdtype(A.dtype, np.complexfloating):
        householder = householder_complex
    elif not np.issubdtype(A.dtype, np.number):
        raise TypeError("pfaffian() can only work on numeric input")
    else:
        householder = householder_real

    if not overwrite_a:
        A = A.copy()

    if calc_q:
        Q = np.eye(A.shape[0], dtype=A.dtype)

    for i in range(A.shape[0]-2):
        # Find a Householder vector to eliminate the i-th column
        v, tau, alpha = householder(A[i+1:, i])
        A[i+1, i] = alpha
        A[i, i+1] = -alpha
        A[i+2:, i] = 0
        A[i, i+2:] = 0

        # Update the matrix block A(i+1:N,i+1:N)
        w = tau * A[i+1:, i+1:] @ v.conj()
        A[i+1:, i+1:] += np.outer(v, w)-np.outer(w, v)

        if calc_q:
            # Accumulate the individual Householder reflections
            # Accumulate them in the form P_1*P_2*..., which is
            # (..*P_2*P_1)^dagger
            y = tau * Q[:, i+1:] @ v
            Q[:, i+1:] -= np.outer(y, v.conj())

    if calc_q:
        return (np.asmatrix(A), np.asmatrix(Q))
    else:
        return np.asmatrix(A)


def skew_LTL(A, overwrite_a=False, calc_L=True, calc_P=True):
    """ T, L, P = skew_LTL(A, overwrite_a, calc_q=True)

    Bring a real or complex skew-symmetric matrix (A=-A^T) into
    tridiagonal form T (with zero diagonal) with a lower unit
    triangular matrix L such that
    P A P^T= L T L^T

    A is overwritten if overwrite_a=True (default: False),
    L and P only calculated if calc_L=True or calc_P=True,
    respectively (default: True).
    """

    # Check if matrix is square
    assert A.shape[0] == A.shape[1] > 0
    # Check if it's skew-symmetric
    assert abs((A+A.T).max()) < 1e-14

    n = A.shape[0]
    A = np.asarray(A)  # the slice views work only properly for arrays

    if not overwrite_a:
        A = A.copy()

    if calc_L:
        L = np.eye(n, dtype=A.dtype)

    if calc_P:
        Pv = np.arange(n)

    for k in range(n-2):
        # First, find the largest entry in A[k+1:,k] and
        # permute it to A[k+1,k]
        kp = k+1+np.abs(A[k+1:, k]).argmax()

        # Check if we need to pivot
        if kp != k+1:
            # interchange rows k+1 and kp
            temp = A[k+1, k:].copy()
            A[k+1, k:] = A[kp, k:]
            A[kp, k:] = temp

            # Then interchange columns k+1 and kp
            temp = A[k:, k+1].copy()
            A[k:, k+1] = A[k:, kp]
            A[k:, kp] = temp

            if calc_L:
                # permute L accordingly
                temp = L[k+1, 1:k+1].copy()
                L[k+1, 1:k+1] = L[kp, 1:k+1]
                L[kp, 1:k+1] = temp

            if calc_P:
                # accumulate the permutation matrix
                temp = Pv[k+1]
                Pv[k+1] = Pv[kp]
                Pv[kp] = temp

        # Now form the Gauss vector
        if A[k+1, k] != 0.0:
            tau = A[k+2:, k].copy()
            tau /= A[k+1, k]

            # clear eliminated row and column
            A[k+2:, k] = 0.0
            A[k, k+2:] = 0.0

            # Update the matrix block A(k+2:,k+2)
            A[k+2:, k+2:] += np.outer(tau, A[k+2:, k+1])
            A[k+2:, k+2:] -= np.outer(A[k+2:, k+1], tau)

            if calc_L:
                L[k+2:, k+1] = tau

    if calc_P:
        # form the permutation matrix as a sparse matrix
        P = sp.csr_matrix((np.ones(n), (np.arange(n), Pv)))

    if calc_L:
        if calc_P:
            return (np.asmatrix(A), np.asmatrix(L), P)
        else:
            return (np.asmatrix(A), np.asmatrix(L))
    else:
        if calc_P:
            return (np.asmatrix(A), P)
        else:
            return np.asmatrix(A)


def pfaffian(A, overwrite_a=False, method='P'):
    """ pfaffian(A, overwrite_a=False, method='P')

    Compute the Pfaffian of a real or complex skew-symmetric
    matrix A (A=-A^T). If overwrite_a=True, the matrix A
    is overwritten in the process. This function uses
    either the Parlett-Reid algorithm (method='P', default),
    or the Householder tridiagonalization (method='H')
    """
    # Check if matrix is square
    assert A.shape[0] == A.shape[1] > 0
    # Check if it's skew-symmetric
    assert abs((A+A.T).max()) < 1e-14, abs((A+A.T).max())
    # Check that the method variable is appropriately set
    assert method == 'P' or method == 'H'

    if method == 'P':
        return pfaffian_LTL(A, overwrite_a)
    else:
        return pfaffian_householder(A, overwrite_a)


def pfaffian_LTL(A, overwrite_a=False):
    """ pfaffian_LTL(A, overwrite_a=False)

    Compute the Pfaffian of a real or complex skew-symmetric
    matrix A (A=-A^T). If overwrite_a=True, the matrix A
    is overwritten in the process. This function uses
    the Parlett-Reid algorithm.
    """
    # Check if matrix is square
    assert A.shape[0] == A.shape[1] > 0
    # Check if it's skew-symmetric
    assert abs((A+A.T).max()) < 1e-14

    n = A.shape[0]
    A = np.asarray(A)  # the slice views work only properly for arrays

    # Quick return if possible
    if n % 2 == 1:
        return 0

    if not overwrite_a:
        A = A.copy()

    pfaffian_val = 1.0

    for k in range(0, n-1, 2):
        # First, find the largest entry in A[k+1:,k] and
        # permute it to A[k+1,k]
        kp = k+1+np.abs(A[k+1:, k]).argmax()

        # Check if we need to pivot
        if kp != k+1:
            # interchange rows k+1 and kp
            temp = A[k+1, k:].copy()
            A[k+1, k:] = A[kp, k:]
            A[kp, k:] = temp

            # Then interchange columns k+1 and kp
            temp = A[k:, k+1].copy()
            A[k:, k+1] = A[k:, kp]
            A[k:, kp] = temp

            # every interchange corresponds to a "-" in det(P)
            pfaffian_val *= -1

        # Now form the Gauss vector
        if A[k+1, k] != 0.0:
            tau = A[k, k+2:].copy()
            tau /= A[k, k+1]

            pfaffian_val *= A[k, k+1]

            if k+2 < n:
                # Update the matrix block A(k+2:,k+2)
                A[k+2:, k+2:] += np.outer(tau, A[k+2:, k+1])
                A[k+2:, k+2:] -= np.outer(A[k+2:, k+1], tau)
        else:
            # if we encounter a zero on the super/subdiagonal, the
            # Pfaffian is 0
            return 0.0

    return pfaffian_val


def pfaffian_householder(A, overwrite_a=False):
    """ pfaffian(A, overwrite_a=False)

    Compute the Pfaffian of a real or complex skew-symmetric
    matrix A (A=-A^T). If overwrite_a=True, the matrix A
    is overwritten in the process. This function uses the
    Householder tridiagonalization.

    Note that the function pfaffian_schur() can also be used in the
    real case. That function does not make use of the skew-symmetry
    and is only slightly slower than pfaffian_householder().
    """

    # Check if matrix is square
    assert A.shape[0] == A.shape[1] > 0
    # Check if it's skew-symmetric
    assert abs((A+A.T).max()) < 1e-14

    n = A.shape[0]

    # Quick return if possible
    if n % 2 == 1:
        return 0

    # Check if we have a complex data type
    if np.issubdtype(A.dtype, np.complexfloating):
        householder = householder_complex
    elif not np.issubdtype(A.dtype, np.number):
        raise TypeError("pfaffian() can only work on numeric input")
    else:
        householder = householder_real

    A = np.asarray(A)  # the slice views work only properly for arrays

    if not overwrite_a:
        A = A.copy()

    pfaffian_val = 1.

    for i in range(A.shape[0]-2):
        # Find a Householder vector to eliminate the i-th column
        v, tau, alpha = householder(A[i+1:, i])
        A[i+1, i] = alpha
        A[i, i+1] = -alpha
        A[i+2:, i] = 0
        A[i, i+2:] = 0

        # Update the matrix block A(i+1:N,i+1:N)
        w = tau * A[i+1:, i+1:] @ v.conj()
        A[i+1:, i+1:] += np.outer(v, w) - np.outer(w, v)

        if tau != 0:
            pfaffian_val *= 1-tau
        if i % 2 == 0:
            pfaffian_val *= -alpha

    pfaffian_val *= A[n-2, n-1]

    return pfaffian_val


def pfaffian_schur(A, overwrite_a=False):
    """Calculate Pfaffian of a real antisymmetric matrix using
    the Schur decomposition. (Hessenberg would in principle be faster,
    but scipy-0.8 messed up the performance for scipy.linalg.hessenberg()).

    This function does not make use of the skew-symmetry of the matrix A,
    but uses a LAPACK routine that is coded in FORTRAN and hence faster
    than python. As a consequence, pfaffian_schur is only slightly slower
    than pfaffian().
    """

    assert np.issubdtype(A.dtype, np.number) and not np.issubdtype(
        A.dtype, np.complexfloating)

    assert A.shape[0] == A.shape[1] > 0

    assert abs(A + A.T).max() < 1e-14

    # Quick return if possible
    if A.shape[0] % 2 == 1:
        return 0

    (t, z) = la.schur(A, output='real', overwrite_a=overwrite_a)
    l = np.diag(t, 1)
    return np.prod(l[::2]) * la.det(z)
