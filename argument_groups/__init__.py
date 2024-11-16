import importlib
import pkgutil

def load_argument_groups(parser):
    """Dynamically load and register argument groups from the `argument_groups` directory."""
    argument_group_dir = "argument_groups"
    for _, module_name, _ in pkgutil.iter_modules([argument_group_dir]):
        # Dynamically import the module
        module = importlib.import_module(f"{argument_group_dir}.{module_name}")
        # Check if the module has a `register_arguments` function
        if hasattr(module, "register_arguments"):
            # Call the `register_arguments` function with the parser
            module.register_arguments(parser)