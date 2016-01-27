{% extends 'basic.tpl' %}

{% block in_prompt -%}
{%- endblock in_prompt %}

{% block input_group -%}
{% endblock input_group %}

{% block input %}
{%- endblock input %}

{% block output %}
{{ super() }}
{% endblock output %}

{% block markdowncell scoped %}
<div>
{{ cell.source  | markdown2html | strip_files_prefix }}
</div>
{%- endblock markdowncell %}
