from jinja2 import Environment, FileSystemLoader


def get_templates_env(templates_dir):
    return Environment(loader=FileSystemLoader(templates_dir), autoescape=(["html", "xml"]))
