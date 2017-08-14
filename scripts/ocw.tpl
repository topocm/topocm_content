{%- extends 'no_code.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{% block header %}
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
{{ mathjax() }}

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

<style type="text/css">
   body { background: #F2F2F2 !important; }
</style>

</head>

<body>
{{ super() }}
<script src="https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.5.14/iframeResizer.contentWindow.js" type="text/javascript"></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML' type="text/javascript"></script>
</body>
{%- endblock header %}
