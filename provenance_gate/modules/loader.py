import importlib
from pathlib import Path
from modules.module_interface import VerificationModule


def load_modules():
    loaded = []
    modules_dir = Path(__file__).parent

    for py_file in modules_dir.glob("*_module.py"):
        if py_file.name in {"module_interface.py", "loader.py"}:
            continue

        module_name = f"modules.{py_file.stem}"
        mod = importlib.import_module(module_name)

        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)

            if (
                isinstance(attr, type)
                and issubclass(attr, VerificationModule)
                and attr is not VerificationModule
            ):
                loaded.append(attr())

    return loaded
