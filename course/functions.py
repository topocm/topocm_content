import collections
import itertools
import math
from copy import copy
from types import SimpleNamespace

import kwant
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

if tuple(int(i) for i in np.__version__.split(".")[:3]) <= (1, 8, 0):
    raise RuntimeError("numpy >= (1, 8, 0) is required")

__all__ = [
    "spectrum",
    "hamiltonian_array",
    "h_k",
    "pauli",
    "line_plot",
    "area_plot",
    "slider_plot",
    "combine_plots",
    "add_reference_lines",
    "set_default_plotly_template",
]


def set_default_plotly_template():
    """Register a simple default Plotly template for the course."""
    template_name = "topocm"
    if template_name not in pio.templates:
        pio.templates[template_name] = go.layout.Template(
            layout=go.Layout(
                template="plotly_white",
                font=dict(family="Helvetica", size=13),
                margin=dict(l=70, r=40, t=40, b=110),
                colorway=["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#8c564b"],
                legend=dict(orientation="h", y=-0.2, x=0, font=dict(size=12)),
            )
        )
    pio.templates.default = template_name


def _axis_config(label=None, ticks=None, limits=None):
    label = _validate_plot_text(label, where="axis title")
    if isinstance(ticks, np.ndarray):
        ticks = ticks.tolist()
    axis = {}
    if label is not None:
        axis["title"] = {"text": label}
    if ticks is not None:
        if isinstance(ticks, (int, float)):
            axis["nticks"] = int(ticks)
        elif ticks and isinstance(ticks[0], (tuple, list)):
            vals, texts = zip(*ticks)
            axis.update(tickmode="array", tickvals=list(vals), ticktext=list(texts))
        else:
            axis.update(tickmode="array", tickvals=list(ticks))
    if limits is not None:
        axis["range"] = list(limits)
    return axis


def _copy_axis_settings(source_axis):
    keys = [
        "range",
        "tickmode",
        "tickvals",
        "ticktext",
        "dtick",
        "tickformat",
        "title",
        "showline",
        "linecolor",
        "ticks",
    ]
    return {
        k: getattr(source_axis, k, None) for k in keys if getattr(source_axis, k, None)
    }


def _enforce_equal_aspect(fig, xaxis="x", yaxis="y"):
    fig.update_layout(
        **{
            f"{xaxis}axis": dict(scaleanchor=yaxis, scaleratio=1, constrain="domain"),
            f"{yaxis}axis": dict(constrain="domain"),
        }
    )


def add_reference_lines(fig, x=None, y=None, **style):
    """Add vertical and/or horizontal reference lines to a figure."""
    line_defaults = dict(line_width=1.4, line_dash="dash", line_color="#444")
    line_style = {**line_defaults, **style}
    if y is not None:
        fig.add_hline(y=y, **line_style)
    if x is not None:
        fig.add_vline(x=x, **line_style)
    return fig


def line_plot(
    x,
    ys,
    *,
    labels=None,
    x_label=None,
    y_label=None,
    x_ticks=None,
    y_ticks=None,
    x_range=None,
    y_range=None,
    title=None,
    show_legend=False,
    add_zero_line=False,
    color="#1f77b4",
    maintain_aspect=False,
):
    """Plot one or many lines sharing the same x-axis."""
    title = _validate_plot_text(title, where="title")
    fig = go.Figure()
    ys = np.array(ys)
    if ys.ndim == 1:
        ys = ys[:, None]
    labels = labels or [f"band {i}" for i in range(ys.shape[1])]
    labels = [_validate_plot_text(label, where="trace name") for label in labels]
    if isinstance(color, (list, tuple)):
        colors = list(color)
    else:
        colors = None
    legend_visible = show_legend and ys.shape[1] > 1
    for idx in range(ys.shape[1]):
        trace_color = colors[idx % len(colors)] if colors else color
        fig.add_scatter(
            x=x,
            y=ys[:, idx],
            mode="lines",
            name=labels[idx],
            line=dict(color=trace_color),
            showlegend=legend_visible,
        )
    if add_zero_line:
        add_reference_lines(fig, y=0, line_color="#888", line_dash="dot")
    fig.update_layout(
        title=title,
        showlegend=legend_visible,
        xaxis=_axis_config(x_label, x_ticks, x_range),
        yaxis=_axis_config(y_label, y_ticks, y_range),
    )
    if maintain_aspect:
        _enforce_equal_aspect(fig)
    return fig


def area_plot(
    x,
    y,
    *,
    baseline=0,
    x_label=None,
    y_label=None,
    x_ticks=None,
    y_ticks=None,
    y_range=None,
    title=None,
    fill_opacity=0.35,
    line_color=None,
    maintain_aspect=False,
):
    """Create a filled area plot with an outline."""
    title = _validate_plot_text(title, where="title")
    fig = go.Figure()
    line_color = line_color or "#1f77b4"
    fig.add_scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(color=line_color, width=2),
        fill="tozeroy",
        fillcolor=f"rgba(31,119,180,{fill_opacity})",
        name=title or "",
        showlegend=False,
    )
    if baseline != 0:
        add_reference_lines(fig, y=baseline, line_color="#888", line_dash="dot")
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=_axis_config(x_label, x_ticks, None),
        yaxis=_axis_config(y_label, y_ticks, y_range),
    )
    if maintain_aspect:
        _enforce_equal_aspect(fig)
    return fig


def combine_plots(figures, *, cols=2, shared_x=False, shared_y=False, titles=None):
    """Arrange multiple plotly figures into a grid."""
    set_default_plotly_template()
    cols = max(1, int(cols))
    rows = math.ceil(len(figures) / cols)
    height = max(420, 380 * rows)
    subplot_titles = titles or [
        getattr(fig.layout.title, "text", "") for fig in figures
    ]
    subplot_titles = [
        _validate_plot_text(t, where="subplot title") for t in subplot_titles
    ]
    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=shared_x,
        shared_yaxes=shared_y,
        subplot_titles=subplot_titles,
        vertical_spacing=0.25,
    )
    for idx, src in enumerate(figures):
        r, c = divmod(idx, cols)
        r += 1
        c += 1
        for trace in src.data:
            fig.add_trace(trace, row=r, col=c)
        # Copy shapes (like reference lines) to the subplot
        if hasattr(src.layout, "shapes") and src.layout.shapes:
            axis_idx = idx + 1
            xref = "x" if axis_idx == 1 else f"x{axis_idx}"
            yref = "y" if axis_idx == 1 else f"y{axis_idx}"
            xdomain = "x domain" if axis_idx == 1 else f"x{axis_idx} domain"
            ydomain = "y domain" if axis_idx == 1 else f"y{axis_idx} domain"
            for shape in src.layout.shapes:
                # Create a copy of the shape and adjust it for the subplot
                shape_dict = shape.to_plotly_json()
                # Update xref and yref to target the correct subplot
                if "xref" in shape_dict:
                    if shape_dict["xref"] in ("x", "x1"):
                        shape_dict["xref"] = xref
                    elif shape_dict["xref"] in ("paper", "x domain"):
                        shape_dict["xref"] = xdomain
                if "yref" in shape_dict:
                    if shape_dict["yref"] in ("y", "y1"):
                        shape_dict["yref"] = yref
                    elif shape_dict["yref"] in ("paper", "y domain"):
                        shape_dict["yref"] = ydomain
                fig.add_shape(**shape_dict)
        if hasattr(src.layout, "xaxis"):
            fig.update_xaxes(**_copy_axis_settings(src.layout.xaxis), row=r, col=c)
        if hasattr(src.layout, "yaxis"):
            fig.update_yaxes(**_copy_axis_settings(src.layout.yaxis), row=r, col=c)
    template_margin = pio.templates[
        pio.templates.default
    ].layout.margin.to_plotly_json()
    # Only add bottom padding for multi-row layouts
    if rows == 1:
        template_margin["b"] = template_margin.get("b", 0)
    else:
        template_margin["b"] = template_margin.get("b", 0) + 30
    fig.update_layout(
        template=pio.templates.default, height=height, margin=template_margin
    )
    return fig


def _validate_plot_text(text, *, where="text"):
    """Ensure text either has no '$' or is fully wrapped in a single math block."""
    if not isinstance(text, str):
        return text
    if "$" in text and not (text.startswith("$") and text.endswith("$")):
        raise ValueError(
            f"{where} must be fully math-wrapped or contain no '$': {text}"
        )
    return text


def slider_plot(figures, *, label="value", initial=None, play=False):
    """Create a slider that switches between a set of pre-built figures."""
    set_default_plotly_template()
    items = list(figures.items())
    if not items:
        raise ValueError("No figures were provided for the slider.")
    if initial is None:
        initial = items[0][0]

    def _format_slider_value(value):
        if isinstance(value, (int, np.integer)):
            return str(int(value))
        try:
            val = float(value)
        except (TypeError, ValueError):
            return str(value)
        if np.isfinite(val):
            return f"{val:.3g}"
        return str(value)

    base_value, base_fig = next((v, f) for v, f in items if v == initial)

    def _frame_layout(fig):
        title = getattr(fig.layout, "title", None)
        text = getattr(title, "text", title)
        layout = {"title": {"text": text}} if text else {}
        if getattr(fig.layout, "shapes", None):
            layout["shapes"] = [s.to_plotly_json() for s in fig.layout.shapes]
        return layout

    frames = [
        go.Frame(name=str(v), data=f.data, layout=_frame_layout(f)) for v, f in items
    ]
    steps = [
        {
            "args": [
                [str(v)],
                {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"},
            ],
            "label": _format_slider_value(v),
            "method": "animate",
        }
        for v, _ in items
    ]
    label_text = str(label)
    if "$" in label_text:
        raise ValueError(
            "Slider labels should not contain LaTeX; use plain or Unicode text."
        )
    slider = {
        "active": [v for v, _ in items].index(base_value),
        "currentvalue": {"prefix": f"{label_text}: "},
        "steps": steps,
    }
    slider["pad"] = {"t": 56, "b": 16}
    slider["y"] = -0.15
    updatemenus = []
    if play:
        updatemenus.append(
            {
                "type": "buttons",
                "showactive": False,
                "y": -0.15,
                "x": 1.05,
                "xanchor": "right",
                "yanchor": "top",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 300, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                    }
                ],
            }
        )
    fig = go.Figure(data=base_fig.data, layout=base_fig.layout, frames=frames)
    template_margin = pio.templates[
        pio.templates.default
    ].layout.margin.to_plotly_json()
    template_margin["b"] = template_margin.get("b", 0) + 30
    fig.update_layout(
        sliders=[slider],
        updatemenus=updatemenus,
        template=pio.templates.default,
        margin=template_margin,
    )
    return fig


pauli = SimpleNamespace(
    s0=np.array([[1.0, 0.0], [0.0, 1.0]]),
    sx=np.array([[0.0, 1.0], [1.0, 0.0]]),
    sy=np.array([[0.0, -1j], [1j, 0.0]]),
    sz=np.array([[1.0, 0.0], [0.0, -1.0]]),
)

pauli.s0s0 = np.kron(pauli.s0, pauli.s0)
pauli.s0sx = np.kron(pauli.s0, pauli.sx)
pauli.s0sy = np.kron(pauli.s0, pauli.sy)
pauli.s0sz = np.kron(pauli.s0, pauli.sz)
pauli.sxs0 = np.kron(pauli.sx, pauli.s0)
pauli.sxsx = np.kron(pauli.sx, pauli.sx)
pauli.sxsy = np.kron(pauli.sx, pauli.sy)
pauli.sxsz = np.kron(pauli.sx, pauli.sz)
pauli.sys0 = np.kron(pauli.sy, pauli.s0)
pauli.sysx = np.kron(pauli.sy, pauli.sx)
pauli.sysy = np.kron(pauli.sy, pauli.sy)
pauli.sysz = np.kron(pauli.sy, pauli.sz)
pauli.szs0 = np.kron(pauli.sz, pauli.s0)
pauli.szsx = np.kron(pauli.sz, pauli.sx)
pauli.szsy = np.kron(pauli.sz, pauli.sy)
pauli.szsz = np.kron(pauli.sz, pauli.sz)


def spectrum(
    syst,
    p=None,
    k_x=None,
    k_y=None,
    k_z=None,
    title=None,
    xdim=None,
    ydim=None,
    zdim=None,
    xticks=None,
    yticks=None,
    zticks=None,
    xlims=None,
    ylims=None,
    zlims=None,
    num_bands=None,
    return_energies=False,
    add_zero_line=False,
):
    """Plot the spectrum of a system using Plotly."""
    set_default_plotly_template()
    if p is None:
        p = dict()
    dimensionality = syst.symmetry.num_directions
    k = [k_x, k_y, k_z]
    k = [(np.linspace(-np.pi, np.pi, 101) if i is None else i) for i in k]
    k = [(i if j < dimensionality else 0) for (j, i) in enumerate(k)]
    k_x, k_y, k_z = k

    hamiltonians, variables = hamiltonian_array(syst, p, k_x, k_y, k_z, True)
    if len(variables) in (1, 2):
        energies = np.linalg.eigvalsh(hamiltonians)

    if len(variables) == 0:
        raise ValueError("A 0D plot requested")

    if return_energies:
        return energies

    if len(variables) == 1:
        x_var, xs = variables[0]
        xdim = xdim or (
            r"${}$".format(x_var) if x_var in "k_x k_y k_z".split() else x_var
        )
        ydim = ydim or r"$E$"
        fig = line_plot(
            xs,
            energies,
            x_label=xdim,
            y_label=ydim,
            x_ticks=xticks,
            y_ticks=yticks,
            x_range=tuple(xlims) if xlims is not None else None,
            y_range=tuple(ylims) if ylims is not None else None,
            title=title(p) if callable(title) else title,
            show_legend=False,
            add_zero_line=add_zero_line,
        )
        return fig

    if len(variables) == 2:
        pi_ticks = [(-np.pi, r"$-\pi$"), (0, "$0$"), (np.pi, r"$\pi$")]
        xticks = (
            xticks
            if xticks is not None
            else (pi_ticks if variables[0][0] in "k_x k_y k_z".split() else None)
        )
        yticks = (
            yticks
            if yticks is not None
            else (pi_ticks if variables[1][0] in "k_x k_y k_z".split() else None)
        )

        xdim = xdim or (
            r"${}$".format(variables[0][0])
            if variables[0][0] in "k_x k_y k_z".split()
            else variables[0][0]
        )
        ydim = ydim or (
            r"${}$".format(variables[1][0])
            if variables[1][0] in "k_x k_y k_z".split()
            else variables[1][0]
        )
        zdim = zdim or r"$E$"

        if xlims is None:
            xlims = np.round([min(variables[0][1]), max(variables[0][1])], 2)
        if ylims is None:
            ylims = np.round([min(variables[1][1]), max(variables[1][1])], 2)
        if zlims is None:
            zlims = (None, None)

        kwargs = {
            "x": np.linspace(*xlims, energies.shape[1]),
            "y": np.linspace(*ylims, energies.shape[0]),
        }
        start, stop = (
            (0, energies.shape[-1])
            if num_bands is None
            else (
                energies.shape[-1] // 2 - num_bands // 2,
                energies.shape[-1] // 2 + num_bands // 2,
            )
        )
        fig = go.Figure()
        for idx in range(start, stop):
            fig.add_surface(
                z=energies[:, :, idx],
                showscale=idx == start,
                colorscale="RdBu",
                opacity=0.85,
                **kwargs,
            )

        fig.update_layout(
            title=title(p) if callable(title) else title,
            scene=dict(
                xaxis=_axis_config(xdim, xticks, xlims),
                yaxis=_axis_config(ydim, yticks, ylims),
                zaxis=_axis_config(zdim, zticks, zlims),
            ),
            template=pio.templates.default,
        )
        return fig

    raise ValueError("Cannot make 4D plots.")


def h_k(syst, p, momentum):
    """Function that returns the Hamiltonian of a kwant 1D system as a momentum."""
    return hamiltonian_array(syst, p, momentum)[0]


def hamiltonian_array(syst, params=None, k_x=0, k_y=0, k_z=0, return_grid=False):
    """Evaluate the Hamiltonian of a system over a grid of parameters."""
    # Prevent accidental mutation of input
    params = copy(params)

    try:
        space_dimensionality = syst.symmetry.periods.shape[-1]
    except AttributeError:
        space_dimensionality = 0
    dimensionality = syst.symmetry.num_directions

    if dimensionality == 0:
        syst = syst.finalized()

        def momentum_to_lattice(k):
            return {}

    else:
        if len(syst.symmetry.periods) == 1:

            def momentum_to_lattice(k):
                if any(k[dimensionality:]):
                    raise ValueError("Dispersion is 1D, but more momenta are provided.")
                return {"k_x": k[0]}

        else:
            B = np.array(syst.symmetry.periods).T
            A = B @ np.linalg.inv(B.T @ B)

            def momentum_to_lattice(k):
                lstsq = np.linalg.lstsq(A, k[:space_dimensionality], rcond=-1)
                k, residuals = lstsq[:2]
                if np.any(abs(residuals) > 1e-7):
                    raise RuntimeError(
                        "Requested momentum doesn't correspond to any lattice momentum."
                    )
                return dict(zip(["k_x", "k_y", "k_z"], list(k)))

        syst = kwant.wraparound.wraparound(syst).finalized()

    changing = dict()
    for key, value in params.items():
        if isinstance(value, collections.abc.Iterable):
            changing[key] = value

    for key, value in [("k_x", k_x), ("k_y", k_y), ("k_z", k_z)]:
        if key in changing:
            raise RuntimeError(
                "One of the system parameters is {}, "
                "which is reserved for momentum. "
                "Please rename it.".format(key)
            )
        if isinstance(value, collections.abc.Iterable):
            changing[key] = value

    def hamiltonian(**values):
        k = [values.pop("k_x", k_x), values.pop("k_y", k_y), values.pop("k_z", k_z)]
        params.update(values)
        k = momentum_to_lattice(k)
        system_params = {**params, **k}
        return syst.hamiltonian_submatrix(params=system_params, sparse=False)

    names, values = zip(*sorted(changing.items())) if changing else ([], [])

    hamiltonians = (
        [hamiltonian(**dict(zip(names, value))) for value in itertools.product(*values)]
        if changing
        else [hamiltonian(k_x=k_x, k_y=k_y, k_z=k_z)]
    )
    size = list(hamiltonians[0].shape)

    hamiltonians = np.array(hamiltonians).reshape(
        [len(value) for value in values] + size
    )

    if return_grid:
        return hamiltonians, list(zip(names, values))
    else:
        return hamiltonians
