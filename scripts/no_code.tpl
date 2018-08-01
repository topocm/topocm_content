{%- extends 'basic.tpl' -%}

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
