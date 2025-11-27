"""
Copyright (c) 2015 and later, Jayson Paulose. All rights reserved.

This script computes properties of the Kagome lattice model introduced
in the paper

"Topological boundary modes in isostatic lattices"
C.L. Kane and T. Lubensky
Nature Physics 10, 39 (2014)
arXiv:1308.0554

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import numpy as np
import plotly.graph_objects as go
from numpy.linalg import norm
from scipy import linalg as la

hex2dbasis = (np.array([1.0, 0]), np.array([0.5, np.sqrt(3.0) / 2.0]))
hex2dbonds = [((0, 0), (1, 0)), ((0, 0), (0, 1)), ((0, 0), (-1, 1))]
klbasisbonds = [
    ((0, 1), (0, 0)),
    ((1, 2), (0, 0)),
    ((2, 0), (0, 0)),
    ((1, 2), (1, 0)),
    ((2, 0), (-1, 1)),
    ((0, 1), (0, -1)),
]


def not_same(bond1, bond2):
    if bond1.p1 == bond2.p1 and bond1.p2 == bond2.p2:
        return False
    if bond1.p2 == bond2.p1 and bond1.p1 == bond2.p2:
        return False
    return True


class Bond:
    def __init__(self, p1, p2, color="r", k=1.0, l0=1.0):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.k = k
        self.l0 = l0

    def __str__(self):
        return "{%d, %d, %1.4f, %1.4f, %s}" % (
            self.p1,
            self.p2,
            self.k,
            self.l0,
            self.color,
        )

    def __repr__(self):
        return self.__str__()


class Mesh:
    def __init__(self, dim=2, L=None):
        self.Points = []
        self.Bonds = []
        self.N = 0
        self.nbrinfo = []
        self.L = L
        self.dim = dim
        self.dislocations = []
        if self.L is None:
            self.L = np.zeros(dim)
        if len(self.L) != dim:
            print("error: box lengths must be of correct dimension")

    def points(self):
        return np.array(self.Points)

    def bonds(self):
        return np.array([[bd.p1, bd.p2] for bd in self.Bonds])

    def add_point(self, point):
        self.Points.append(point)
        self.nbrinfo.append(dict([]))
        self.N += 1

    def append_bond(self, bond):
        self.Bonds.append(bond)

    def add_bond(self, p1, p2=None, color="r", k=1.0, l0=1.0):
        if p2 is None:
            self.append_bond(p1, k=k, l0=l0)
        else:
            self.append_bond(Bond(p1, p2, color, k=k, l0=l0))

        if len(color) == 2:
            self.nbrinfo[p1][color[1]] = p2
            self.nbrinfo[p2][color[0]] = p1

    def dr(self, p1, p2=None):
        if p2 is None:
            p2 = p1.p2
            p1 = p1.p1
        dx = self.Points[p2] - self.Points[p1]
        for i in range(self.dim):
            dx[i] = (
                dx[i]
                if abs(dx[i]) < 0.5 * self.L[i]
                else dx[i] - abs(dx[i] + 0.5 * self.L[i]) + abs(dx[i] - 0.5 * self.L[i])
            )
        return dx


def klbasis(x1, x2, x3, z=0):
    """Calculates the *s* vectors in the Kane-Lubensky parametrization (*Nat Phys 2014*) of the
    deformed kagome lattices.

    :param x1,x2,x3,z: The four parameters used by Kane and Lubensky in their parametrization.
    :returns: List of the three vectors *s1,s2,s3* as defined in Fig. 2a of the paper.
    """
    a1, a2, a3 = [
        np.array([np.cos(2 * np.pi * p / 3.0), np.sin(2 * np.pi * p / 3.0)])
        for p in range(3)
    ]
    y1 = z / 3.0 + x3 - x2
    y2 = z / 3.0 + x1 - x3
    s1 = x1 * (a3 - a2) + y1 * a1
    s2 = x2 * (a1 - a3) + y2 * a2
    return s2, np.array([0.0, 0.0]), -s1  # return xvec30, xvec41, xvec52


def klbasispoints(x1, x2, x3, z=0):
    """Calculate the positions of the three points in the unit cell of the deformed kagome
    lattice under the Kane-Lubensky parametrization.

    :param x1,x2,x3,z: Four parameters used in the Kane-Lubensky parametrization.
    :returns: List of three position vectors *d3,d1,d2* of the basis points in the unit cell as
        defined in Fig. 2a of the paper.
    """
    xvec30, xvec41, xvec52 = klbasis(x1, x2, x3, z)
    x1, x2, x3 = np.vstack(
        (np.cos(np.pi / 3 * np.arange(3)), np.sin(np.pi / 3 * np.arange(3)))
    ).T
    p1 = x1 / 2.0 + xvec30
    p2 = (x1 + x2) / 2.0 + xvec52
    p3 = x2 / 2.0 + xvec41
    return [p1, p2, p3]


def vis2d(
    mesh,
    draw_points=False,
    eigenfunction=None,
    ecolors="r",
    offset=np.array([0.0, 0.0]),
    colormap="jet",
    lw=1,
    quiverwidth=None,
    bondcolor=(0.3, 0.3, 0.3, 1.0),
    pad=1,
    **kwargs,
):
    """Visualize a mesh using Plotly (bonds + displacement arrows)."""

    pts = mesh.points() + offset
    lenmode = 2 * len(pts)

    cutoff = mesh.lx / 2 if mesh.lx < mesh.ly else mesh.ly / 2

    x_lines = []
    y_lines = []
    for bd in mesh.Bonds:
        if norm(pts[bd.p1] - pts[bd.p2]) < cutoff:
            x_lines.extend([pts[bd.p1][0], pts[bd.p2][0], None])
            y_lines.extend([pts[bd.p1][1], pts[bd.p2][1], None])

    x_arrows = []
    y_arrows = []
    if eigenfunction is not None:
        disp = eigenfunction[:lenmode].reshape(len(pts), 2)
        disp *= kwargs.get("scale", 1)
        for pt, d in zip(pts, disp):
            x_arrows.extend([pt[0], pt[0] + d[0], None])
            y_arrows.extend([pt[1], pt[1] + d[1], None])

    def _rgba(color):
        if isinstance(color, tuple) and len(color) == 4:
            r, g, b, a = color
            return f"rgba({r * 255},{g * 255},{b * 255},{a})"
        if isinstance(color, str):
            return {"r": "red", "g": "green", "b": "blue"}.get(color, color)
        return color

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_lines,
            y=y_lines,
            mode="lines",
            line=dict(color=_rgba(bondcolor), width=lw),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_arrows,
            y=y_arrows,
            mode="lines",
            line=dict(color=_rgba(ecolors), width=2),
            showlegend=False,
        )
    )
    xmin, xmax = pts[:, 0].min() - pad, pts[:, 0].max() + pad
    ymin, ymax = pts[:, 1].min() - pad, pts[:, 1].max() + pad
    fig.update_layout(
        xaxis=dict(
            visible=False,
            range=[xmin, xmax],
            scaleanchor="y",
            scaleratio=1,
            fixedrange=True,
            autorange=False,
        ),
        yaxis=dict(
            visible=False,
            range=[ymin, ymax],
            fixedrange=True,
            autorange=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=120,
    )
    return fig


def periodicize(mesh, L, eps=0.101231):
    mesh += np.ones_like(L) * eps
    L = np.array(L)
    for pt in mesh:
        wrap = np.round((pt - L / 2) / L)
        pt -= wrap * L
    mesh -= np.ones_like(L) * eps


def makeLattice(
    a, basis, bondlist, n, rectangle=True, periodic=True, boundaryshift=None
):
    """
    Tile a unit cell to get a lattice. General dimensions
    a: list of primitive lattice vectors (length gives dimension)
    basis: set of point positions for a lattice
    bondlist: adjacency list connecting points across respective boundaries
    n: repeating units in each dimension
    """
    dim = len(a)

    if basis is None:
        basis = [np.zeros(dim, dtype=float)]

    if boundaryshift is not None:
        boundaryshift = np.array(boundaryshift)

    def idx(latticept, basisidx):
        internalidx = sum([latticept[i] * np.prod(n[i + 1 :]) for i in range(dim)])
        return int(internalidx + basisidx * np.prod(n))

    # totalsize = np.prod(n) * len(basis)  # unused; removed to satisfy ruff
    mesh = Mesh(dim, L=10000 * np.ones(dim))

    slices = tuple([slice(0, ni) for ni in n])
    grid = np.mgrid[slices]
    lattice = np.sum([a[i] * grid[i].ravel()[:, None] for i in range(dim)], axis=0)
    # print lattice.shape
    if rectangle:
        dx = np.max(np.abs(np.array(a)), axis=0)
        L = dx * np.array(n)
        periodicize(lattice, L)
        mesh.L = L
    allpts = np.vstack([lattice + b for b in basis])
    for p in allpts:
        mesh.add_point(p)

    aidx = np.eye(dim, dtype=int)
    latticeidx = np.sum(
        [aidx[i] * grid[i].ravel()[:, None] for i in range(dim)], axis=0
    )
    for lpt in latticeidx:
        for bond, delta in bondlist:
            secondpt = lpt + delta
            if not periodic and not rectangle:
                if np.all((0 <= secondpt) & (secondpt < n)):
                    mesh.add_bond(idx(lpt, bond[0]), idx(secondpt, bond[1]))
            else:
                secondptwrap = np.mod(secondpt, n)
                whichborder = secondptwrap != secondpt
                if np.any(whichborder) and boundaryshift is not None:
                    bsd = boundaryshift * np.sign(delta)[:, None]
                    secondptwrap = secondptwrap + np.sum(bsd[whichborder], axis=0)
                idx1 = idx(lpt, bond[0])
                idx2 = idx(np.mod(secondptwrap, n), bond[1])
                if periodic:
                    mesh.add_bond(idx1, idx2)
                else:
                    dx = np.abs(mesh.Points[idx1] - mesh.Points[idx2])
                    if np.all(dx < mesh.L / 2):
                        mesh.add_bond(idx1, idx2)

    return mesh


def kagome2d(lx, ly, x, rect=True, periodic=True):
    boundaryshift = None
    if rect:
        boundaryshift = [[0, 0], [ly / 2, 0]]
    lattice = makeLattice(
        hex2dbasis,
        klbasispoints(*x),
        klbasisbonds,
        (lx, ly),
        rectangle=rect,
        boundaryshift=boundaryshift,
        periodic=periodic,
    )
    return to2dlattice(lattice)


def to2dlattice(mesh):
    mesh.lx = mesh.L[0]
    mesh.ly = mesh.L[1]
    return mesh


def replacepoints(mesh1, mesh2, x1frac=0.33, x2frac=0.66):
    """
    replace points in mesh1 with points from mesh2 for x between x1 and x2
    """
    for i, pt in enumerate(mesh1.Points):
        if x1frac * mesh1.L[0] < pt[0] < x2frac * mesh2.L[0]:
            mesh1.Points[i] = mesh2.Points[i]
    return mesh1


def dwallslab(x1, x2, lx=16, ly=6, dwall1=0.25, dwall2=0.75):
    mesh1 = kagome2d(lx, ly, x1, rect=True)
    mesh2 = kagome2d(lx, ly, x2, rect=True)

    replacepoints(mesh1, mesh2, dwall1, dwall2)
    return mesh1


##################################
# Rigidity matrix and eigenmodes #
##################################


def rigiditymatrix(mesh):
    r = []
    pts = mesh.points()
    bds = mesh.Bonds
    dim = len(pts[0])
    for bd in bds:
        row = np.zeros(dim * mesh.N)
        dp = mesh.dr(bd.p2, bd.p1)
        dp = dp / la.norm(dp)
        for i in range(dim):
            row[dim * bd.p1 + i] = dp[i]
            row[dim * bd.p2 + i] = -dp[i]
        r.append(row)
    return np.matrix(r)


def dynamicalmatrix(mesh):
    r = rigiditymatrix(mesh)
    return np.dot(r.T, r)


def modes(mesh):
    eigval, eigvec = la.eigh(dynamicalmatrix(mesh))
    eigvec = np.array(eigvec).T

    sortedargs = np.argsort(np.real(eigval))
    return np.real(eigval)[sortedargs], np.real(eigvec)[sortedargs]


def showlocalizedmode(mesh, modenumber=2):
    ee, ev = modes(mesh)
    return vis2d(mesh, eigenfunction=ev[modenumber], scale=2)
