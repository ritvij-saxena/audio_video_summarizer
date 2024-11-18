import os
import importlib
import inspect
import logging

from processors import BaseProcessor


class ProcessorRegistry:
    _registry = {}

    @classmethod
    def discover_processors(cls, processors_dir):
        """Dynamically discover and register processor classes."""
        for file in os.listdir(processors_dir):
            if file.endswith("_processor.py") and file != "__init__.py":
                module_name = f"processors.{file[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Register classes that inherit from BaseProcessor and are not abstract
                        if issubclass(obj, BaseProcessor) and not inspect.isabstract(obj):
                            arg_name = file[:-3].replace("_processor", "")
                            cls._registry[arg_name] = obj
                            logging.info(f"Registered processor: {arg_name} -> {obj}")
                except Exception as e:
                    logging.error(f"Error importing module {module_name}: {e}")

    @classmethod
    def get_processor(cls, arg_name):
        """Returns the processor class based on the argument name."""
        return cls._registry.get(arg_name)