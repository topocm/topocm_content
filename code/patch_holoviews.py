import param

from holoviews.core.util import *
from holoviews.plotting.mpl.chart3d import *
from holoviews.plotting.mpl.element import *

def patch_core_util():
    import holoviews.core.util


    def max_extents(extents, zrange=False):
        """
        Computes the maximal extent in 2D and 3D space from
        list of 4-tuples or 6-tuples. If zrange is enabled
        all extents are converted to 6-tuples to comput
        x-, y- and z-limits.
        """
        if zrange:
            num = 6
            inds = [(0, 3), (1, 4), (2, 5)]
            extents = [e if len(e) == 6 else (e[0], e[1], None,
                                              e[2], e[3], None)
                       for e in extents]
        else:
            num = 4
            inds = [(0, 2), (1, 3)]
        arr = list(zip(*extents)) if extents else []
        extents = [np.NaN] * num
        if len(arr) == 0:
            return extents
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
            for lidx, uidx in inds:
                lower = [v for v in arr[lidx] if v is not None]
                upper = [v for v in arr[uidx] if v is not None]
                if lower and isinstance(lower[0], np.datetime64):
                    extents[lidx] = np.min(lower)
                elif lower:
                    extents[lidx] = np.nanmin(lower)
                if upper and isinstance(upper[0], np.datetime64):
                    extents[uidx] = np.max(upper)
                elif upper:
                    extents[uidx] = np.nanmax(upper)
        return tuple(extents)

    holoviews.core.util.max_extents = max_extents


def patch_plotting_util():
    import holoviews.plotting.bokeh.util
    import holoviews.plotting.util
    holoviews.plotting.util.map_colors = holoviews.plotting.bokeh.util.map_colors


def patch_mpl_chart3d():
    import holoviews.plotting.mpl.chart3d

    import matplotlib.cm as cm
    from holoviews.plotting.util import map_colors

    holoviews.plotting.mpl.chart3d.cm = cm
    holoviews.plotting.mpl.chart3d.map_colors = map_colors
    
    def _finalize_axis(self, key, **kwargs):
        """
        Extends the ElementPlot _finalize_axis method to set appropriate
        labels, and axes options for 3D Plots.
        """
        axis = self.handles['axis']
        self.handles['fig'].set_frameon(False)
        axis.grid(self.show_grid)
        axis.view_init(elev=self.elevation, azim=self.azimuth)
        axis.dist = self.distance

        if self.xaxis is None:
            axis.w_xaxis.line.set_lw(0.)
            axis.w_xaxis.label.set_text('')
        if self.yaxis is None:
            axis.w_yaxis.line.set_lw(0.)
            axis.w_yaxis.label.set_text('')
        if self.zaxis is None:
            axis.w_zaxis.line.set_lw(0.)
            axis.w_zaxis.label.set_text('')
        if self.disable_axes:
            axis.set_axis_off()

        axis.set_axis_bgcolor(self.bgcolor)
        return super(Plot3D, self)._finalize_axis(key, **kwargs)

    holoviews.plotting.mpl.chart3d.Plot3D._finalize_axis = _finalize_axis

    def update_frame(self, *args, **kwargs):
        super(Plot3D, self).update_frame(*args, **kwargs)

    holoviews.plotting.mpl.chart3d.Plot3D.update_frame = update_frame
    
    def initialize_plot(self, ranges=None):
        axis = self.handles['axis']
        points = self.hmap.last
        ranges = self.compute_ranges(self.hmap, self.keys[-1], ranges)
        ranges = match_spec(points, ranges)
        key = self.keys[-1]
        xs, ys, zs = (points.dimension_values(i) for i in range(3))

        style = self.style[self.cyclic_index]
        cdim = points.get_dimension(self.color_index)
        if cdim and 'cmap' in style:
            cs = points.dimension_values(self.color_index)
            style['c'] = cs
            if 'clim' not in style:
                clims = ranges[cdim.name]
                style.update(vmin=clims[0], vmax=clims[1])
        if points.get_dimension(self.size_index):
            style['s'] = self._compute_size(points, style)

        scatterplot = axis.scatter(xs, ys, zs, zorder=self.zorder, **style)

        self.handles['axis'].add_collection(scatterplot)
        self.handles['artist'] = scatterplot

        return self._finalize_axis(key, ranges=ranges)

    holoviews.plotting.mpl.chart3d.Scatter3DPlot.initialize_plot = initialize_plot

    def update_handles(self, axis, points, key, ranges=None):
        artist = self.handles['artist']
        artist._offsets3d = tuple(points[d] for d in points.dimensions())
        cdim = points.get_dimension(self.color_index)
        style = self.style[self.cyclic_index]
        if cdim and 'cmap' in style:
            cs = points.dimension_values(self.color_index)
            clim = style['clim'] if 'clim' in style else ranges[cdim.name]
            cmap = cm.get_cmap(style['cmap'])
            artist._facecolor3d = map_colors(cs, clim, cmap, False)
        if points.get_dimension(self.size_index):
            artist.set_sizes(self._compute_size(points, style))

    holoviews.plotting.mpl.chart3d.Scatter3DPlot.update_handles = update_handles

    def update_handles(self, axis, element, key, ranges=None):
        if 'artist' in self.handles:
            self.handles['axis'].collections.remove(self.handles['artist'])
        mat = element.data
        rn, cn = mat.shape
        l, b, zmin, r, t, zmax = self.get_extents(element, ranges)
        r, c = np.mgrid[l:r:(r-l)/float(rn), b:t:(t-b)/float(cn)]

        style_opts = self.style[self.cyclic_index]

        if self.plot_type == "wireframe":
            self.handles['artist'] = self.handles['axis'].plot_wireframe(r, c, mat, **style_opts)
        elif self.plot_type == "surface":
            style_opts['vmin'] = zmin
            style_opts['vmax'] = zmax
            self.handles['artist'] = self.handles['axis'].plot_surface(r, c, mat, **style_opts)
        elif self.plot_type == "contour":
            self.handles['artist'] = self.handles['axis'].contour3D(r, c, mat, **style_opts)

    holoviews.plotting.mpl.chart3d.SurfacePlot.update_handles = update_handles

    def update_handles(self, axis, element, key, ranges=None):
        if 'artist' in self.handles:
            self.handles['axis'].collections.remove(self.handles['artist'])
        style_opts = self.style[self.cyclic_index]
        dims = element.dimensions(label=True)
        vrange = ranges[dims[2]]
        x, y, z = [element.dimension_values(d) for d in dims]
        artist = axis.plot_trisurf(x, y, z, vmax=vrange[1],
                                   vmin=vrange[0], **style_opts)
        self.handles['artist'] = artist

    holoviews.plotting.mpl.chart3d.TrisurfacePlot.update_handles = update_handles


def patch_mpl_element():
    import holoviews.plotting.mpl.element

    def _finalize_axis(self, key, title=None, ranges=None, xticks=None, yticks=None,
                       zticks=None, xlabel=None, ylabel=None, zlabel=None):
        """
        Applies all the axis settings before the axis or figure is returned.
        Only plots with zorder 0 get to apply their settings.

        When the number of the frame is supplied as n, this method looks
        up and computes the appropriate title, axis labels and axis bounds.
        """
        element = self._get_frame(key)
        self.current_frame = element
        axis = self.handles['axis']
        if self.bgcolor:
            axis.set_axis_bgcolor(self.bgcolor)

        subplots = list(self.subplots.values()) if self.subplots else []
        if self.zorder == 0 and key is not None:
            title = None if self.zorder > 0 else self._format_title(key)
            suppress = any(sp.hmap.type in self._suppressed for sp in [self] + subplots
                           if isinstance(sp.hmap, HoloMap))
            if element is not None and not suppress:
                xlabel, ylabel, zlabel = self._axis_labels(element, subplots, xlabel, ylabel, zlabel)
                if self.invert_axes:
                    xlabel, ylabel = ylabel, xlabel

                self._finalize_limits(axis, element, subplots, ranges)

                # Tick formatting
                xdim, ydim = element.get_dimension(0), element.get_dimension(1)
                xformat, yformat = None, None
                if xdim is None:
                    pass
                elif xdim.value_format:
                    xformat = xdim.value_format
                elif xdim.type in xdim.type_formatters:
                    xformat = xdim.type_formatters[xdim.type]
                if xformat:
                    axis.xaxis.set_major_formatter(wrap_formatter(xformat))

                if ydim is None:
                    pass
                elif ydim.value_format:
                    yformat = ydim.value_format
                elif ydim.type in ydim.type_formatters:
                    yformat = ydim.type_formatters[ydim.type]
                if yformat:
                    axis.yaxis.set_major_formatter(wrap_formatter(yformat))

            if self.zorder == 0 and not subplots:
                legend = axis.get_legend()
                if legend: legend.set_visible(self.show_legend)

                axis.get_xaxis().grid(self.show_grid)
                axis.get_yaxis().grid(self.show_grid)

            if xlabel and self.xaxis: axis.set_xlabel(xlabel, **self._fontsize('xlabel'))
            if ylabel and self.yaxis: axis.set_ylabel(ylabel, **self._fontsize('ylabel'))
            if zlabel and self.zaxis: axis.set_zlabel(zlabel, **self._fontsize('ylabel'))

            self._apply_aspect(axis)
            self._subplot_label(axis)
            if self.apply_ticks:
                self._finalize_ticks(axis, element, xticks, yticks, zticks)


            if self.show_title and title is not None:
                if 'title' in self.handles:
                    self.handles['title'].set_text(title)
                else:
                    self.handles['title'] = axis.set_title(title,
                                                           **self._fontsize('title'))
        # Always called to ensure log and inverted axes are applied
        self._finalize_axes(axis)
        if not self.overlaid and not self.drawn:
            self._finalize_artist(key)

        for hook in self.finalize_hooks:
            try:
                hook(self, element)
            except Exception as e:
                self.warning("Plotting hook %r could not be applied:\n\n %s" % (hook, e))

        return super(ElementPlot, self)._finalize_axis(key)

    holoviews.plotting.mpl.element.ElementPlot._finalize_axis = _finalize_axis

    def update_frame(self, key, ranges=None, element=None):
        axis = self.handles['axis']
        if element is None:
            element = self._get_frame(key)
        else:
            self.current_frame = element
            self.current_key = key

        if isinstance(self.hmap, DynamicMap):
            range_obj = element
            items = element.items()
        else:
            range_obj = self.hmap
            items = element.items()
        ranges = self.compute_ranges(range_obj, key, ranges)

        for k, subplot in self.subplots.items():
            el = element.get(k, None)
            if isinstance(self.hmap, DynamicMap):
                idx = dynamic_update(self, subplot, k, element, items)
                if idx is not None:
                    _, el = items.pop(idx)
            subplot.update_frame(key, ranges, el)

        if isinstance(self.hmap, DynamicMap) and items:
            raise Exception("Some Elements returned by the dynamic callback "
                            "were not initialized correctly and could not be "
                            "rendered.")

        if self.show_legend:
            self._adjust_legend(element, axis)

        self._finalize_axis(key, ranges=ranges)

    holoviews.plotting.mpl.element.OverlayPlot.update_frame = update_frame


def patch_all():
    with param.logging_level('error'):
        patch_core_util()
        patch_plotting_util()
        patch_mpl_chart3d()
        patch_mpl_element()

