{%- extends 'display_priority.tpl' -%}

{% block header %}
{{ super() }}
<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<link rel="stylesheet" href="/static/hv_widgets_settings.css">
<link rel="stylesheet" href="/static/notebook.css">

<script src="https://code.jquery.com/jquery-2.1.4.min.js" type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.20/require.min.js" type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js" type="text/javascript"></script>
<script src="/static/widgets.js" type="text/javascript"></script>
<script src="/static/mplwidgets.js" type="text/javascript"></script>
{%- endblock header %}

{% block codecell %}
<div class="cell border-box-sizing code_cell rendered">
{{ super() }}
</div>
{%- endblock codecell %}

{% block input_group -%}
{% endblock input_group %}

{% block output_group %}
<div class="output">
{{ super() }}
</div>
{% endblock output_group %}

{% block in_prompt -%}
{%- endblock in_prompt %}

{% block empty_in_prompt -%}
{%- endblock empty_in_prompt %}

{# 
  output_prompt doesn't do anything in HTML,
  because there is a prompt div in each output area (see output block)
#}
{% block output_prompt %}
{% endblock output_prompt %}

{% block input %}
<div class="inner_cell">
    <div class="input_area">
{{ cell.source | highlight_code(metadata=cell.metadata) }}
</div>
</div>
{%- endblock input %}

{% block output %}
<div>
{{ super() }}
</div>
{% endblock output %}

{% block markdowncell scoped %}
<div>
{{ cell.source  | markdown2html | strip_files_prefix }}
</div>
{%- endblock markdowncell %}

{% block unknowncell scoped %}
unknown type  {{ cell.type }}
{% endblock unknowncell %}

{% block execute_result -%}
{%- set extra_class="output_execute_result" -%}
{% block data_priority scoped %}
{{ super() }}
{% endblock %}
{%- set extra_class="" -%}
{%- endblock execute_result %}

{% block stream_stdout -%}
<div class="output_subarea output_stream output_stdout output_text">
<pre>
{{- output.text | ansi2html -}}
</pre>
</div>
{%- endblock stream_stdout %}

{% block stream_stderr -%}
<div class="output_subarea output_stream output_stderr output_text">
<pre>
{{- output.text | ansi2html -}}
</pre>
</div>
{%- endblock stream_stderr %}

{% block data_svg scoped -%}
<div class="output_svg output_subarea {{extra_class}}">
{%- if output.svg_filename %}
<img src="{{output.svg_filename | posix_path}}"
{%- else %}
{{ output.data['image/svg+xml'] }}
{%- endif %}
</div>
{%- endblock data_svg %}

{% block data_html scoped -%}
<div class="output_html rendered_html output_subarea {{extra_class}}">
{{ output.data['text/html'] }}
</div>
{%- endblock data_html %}

{% block data_markdown scoped -%}
<div class="output_markdown rendered_html output_subarea {{extra_class}}">
{{ output.data['text/markdown'] | markdown2html }}
</div>
{%- endblock data_markdown %}

{% block data_png scoped %}
<div class="output_png output_subarea {{extra_class}}">
{%- if 'image/png' in output.metadata.get('filenames', {}) %}
<img src="{{output.metadata.filenames['image/png'] | posix_path}}"
{%- else %}
<img src="data:image/png;base64,{{ output.data['image/png'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/png') -%}
{%- if width is not none %}
width={{width}}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/png') -%}
{%- if height is not none %}
height={{height}}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/png') -%}
class="unconfined"
{%- endif %}
>
</div>
{%- endblock data_png %}

{% block data_jpg scoped %}
<div class="output_jpeg output_subarea {{extra_class}}">
{%- if 'image/jpeg' in output.metadata.get('filenames', {}) %}
<img src="{{output.metadata.filenames['image/jpeg'] | posix_path}}"
{%- else %}
<img src="data:image/jpeg;base64,{{ output.data['image/jpeg'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/jpeg') -%}
{%- if width is not none %}
width={{width}}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/jpeg') -%}
{%- if height is not none %}
height={{height}}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/jpeg') -%}
class="unconfined"
{%- endif %}
>
</div>
{%- endblock data_jpg %}

{% block data_latex scoped %}
<div class="output_latex output_subarea {{extra_class}}">
{{ output.data['text/latex'] }}
</div>
{%- endblock data_latex %}

{% block error -%}
<div class="output_subarea output_text output_error">
<pre>
{{- super() -}}
</pre>
</div>
{%- endblock error %}

{%- block traceback_line %}
{{ line | ansi2html }}
{%- endblock traceback_line %}

{%- block data_text scoped %}
<div class="output_text output_subarea {{extra_class}}">
<pre>
{{- output.data['text/plain'] | ansi2html -}}
</pre>
</div>
{%- endblock -%}

{%- block data_javascript scoped %}
{% set div_id = uuid4() %}
<div id="{{ div_id }}"></div>
<div class="output_subarea output_javascript {{extra_class}}">
<script async type="text/javascript">
var element = $('#{{ div_id }}');
{{ output.data['application/javascript'] }}
</script>
</div>
{%- endblock -%}
