{%- extends 'no_code.tpl' -%}

{% block header %}
{{ super() }}
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
{%- endblock header %}

{% block body %}
{{ super() }}
<script src="https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.5.10/iframeResizer.contentWindow.js" type="text/javascript" async></script>
<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML' type="text/javascript" async></script>
{%- endblock body %}
