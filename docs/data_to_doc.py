def render_data(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    if app.builder.format != "html":
        return
    src = source[0]
    rendered = app.builder.templates.render_string(src, app.config.html_context)
    source[0] = rendered


def setup(app):
    app.connect("source-read", render_data)
