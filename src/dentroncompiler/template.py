import os

from jinja2 import Environment, FileSystemLoader

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
TEMPLATE_ROOT = os.path.join(CURRENT_PATH, "templates")
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_ROOT))


def load_template_by_name(template_name: str) -> str:
    """
    Load a template file by its name.
    
    Args:
        template_name (str): The name of the template file.
        
    Returns:
        str: The content of the template file.
    """
    if template_name.endswith(".jinja"):
        template_name = template_name[:-6]
    if template_name.endswith(".html"):
        template_name = template_name[:-5]
    t_name = None
    for name in (template_name, 
                 template_name + ".jinja", 
                 template_name + ".html", 
                 template_name + ".html.jinja"):
        if os.path.exists(os.path.join(TEMPLATE_ROOT, name)):
            t_name = name
            break
    if t_name is None:
        raise FileNotFoundError(f"Template {template_name} not found.")
    
    template = JINJA_ENV.get_template(t_name)
    return template
