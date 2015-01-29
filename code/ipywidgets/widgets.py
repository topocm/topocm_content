import copy
import numpy as np


class StaticWidget(object):
    """Base Class for Static Widgets"""
    def __init__(self, name=None, divclass=None):
        self.name = name
        if divclass is None:
            self.divargs = ""
        else:
            self.divargs = 'class:"{0}"'.format(divclass)
    
    def __repr__(self):
        return self.html()
    
    def _repr_html_(self):
        return self.html()

    def copy(self):
        return copy.deepcopy(self)

    def renamed(self, name):
        if (self.name is not None) and (self.name != name):
            obj = self.copy()
        else:
            obj = self
        obj.name = name
        return obj


class RangeWidget(StaticWidget):
    """Range (slider) widget"""
    slider_html = ('<b>{name}:</b> <input type="range" name="{name}" '
                   'min="{range[0]}" max="{range[1]}" step="{range[2]}" '
                   'value="{default}" style="{style}" '
                   'oninput="interactUpdate(this.parentNode);" '
                   'onchange="interactUpdate(this.parentNode);">')
    def __init__(self, min, max, step=1, name=None,
                 default=None, width=350, divclass=None,
                 show_range=False):
        StaticWidget.__init__(self, name, divclass)
        self.datarange = (min, max, step)
        self.width = width
        self.show_range = show_range
        if default is None:
            self.default = min
        else:
            self.default = default
            
    def values(self):
        min, max, step = self.datarange
        return np.arange(min, max + step, step)
            
    def html(self):
        style = ""
        
        if self.width is not None:
            style += "width:{0}px".format(self.width)
            
        output = self.slider_html.format(name=self.name, range=self.datarange,
                                         default=self.default, style=style)
        if self.show_range:
            output = "{0} {1} {2}".format(self.datarange[0],
                                          output,
                                          self.datarange[1])
        return output

class DropDownWidget(StaticWidget):
    select_html = ('<b>{name}:</b> <select name="{name}" '
                      'onchange="interactUpdate(this.parentNode);"> '
                      '{options}'
                      '</select>'
        )
    option_html = ('<option value="{value}" '
                      '{selected}>{label}</option>')
    def __init__(self, values, name=None,
                 labels=None, default=None, divclass=None,
                 delimiter="      "
                 ):
        StaticWidget.__init__(self, name, divclass)
        self._values = values
        self.delimiter = delimiter
        if labels is None:
            labels = map(str, values)
        elif len(labels) != len(values):
            raise ValueError("length of labels must match length of values")
        self.labels = labels

        if default is None:
            self.default = values[0]
        elif default in values:
            self.default = default
        else:
            raise ValueError("if specified, default must be in values")

    def _single_option(self,label,value):
        if value == self.default:
            selected = ' selected '
        else:
            selected = ''
        return self.option_html.format(label=label,
                                       value=value,
                                       selected=selected)
    def values(self):
        return self._values
    def html(self):
        options = self.delimiter.join(
            [self._single_option(label,value)
             for (label,value) in zip(self.labels, self._values)]
        )
        return self.select_html.format(name=self.name,
                                       options=options)

class RadioWidget(StaticWidget):
    radio_html = ('<input type="radio" name="{name}" value="{value}" '
                  '{checked} '
                  'onchange="interactUpdate(this.parentNode);">')
    
    def __init__(self, values, name=None,
                 labels=None, default=None, divclass=None,
                 delimiter="      "):
        StaticWidget.__init__(self, name, divclass)
        self._values = values
        self.delimiter = delimiter
        
        if labels is None:
            labels = map(str, values)
        elif len(labels) != len(values):
            raise ValueError("length of labels must match length of values")
        self.labels = labels
        
        if default is None:
            self.default = values[0]
        elif default in values:
            self.default = default
        else:
            raise ValueError("if specified, default must be in values")
            
    def _single_radio(self, value):
        if value == self.default:
            checked = 'checked="checked"'
        else:
            checked = ''
        return self.radio_html.format(name=self.name, value=value,
                                      checked=checked)
    
    def values(self):
        return self._values
            
    def html(self):
        preface = '<b>{name}:</b> '.format(name=self.name)
        return  preface + self.delimiter.join(
            ["{0}: {1}".format(label, self._single_radio(value))
             for (label, value) in zip(self.labels, self._values)])
    
