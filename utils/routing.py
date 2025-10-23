import importlib
from pathlib import Path
from fastapi import FastAPI


def register_routes(app: FastAPI, routes_dir: str = "routes", base_prefix: str | None = None):
    here = Path(__file__).parent.parent
    routes_path = here / routes_dir
    
    if not routes_path.exists():
        return
    
    for py_file in routes_path.rglob("*.py"):
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue

        relative_path = py_file.relative_to(routes_path)
        module_parts = [routes_dir] + list(relative_path.parent.parts) + [py_file.stem]
        module_name = ".".join(module_parts)

        path_str = str(relative_path.with_suffix("")).replace("\\", "/")

        if base_prefix:
            if path_str.startswith("api/"):
                path_str = path_str[4:]
            prefix = base_prefix.rstrip("/") + "/" + path_str
        else:
            prefix = "/" + path_str

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                app.include_router(module.router, prefix=prefix)
        except Exception as e:
            print(f"Failed to load route module {module_name}: {e}")
