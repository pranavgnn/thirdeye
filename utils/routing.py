import os
import importlib
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse


def register_routes(app: FastAPI, routes_dir: str = "routes"):
    here = Path(__file__).parent.parent
    routes_path = here / routes_dir
    
    if not routes_path.exists():
        return
    
    for html_file in routes_path.rglob("*.html"):
        relative_path = html_file.relative_to(routes_path)
        
        if relative_path.name == "index.html":
            route = "/" if relative_path.parent == Path(".") else f"/{relative_path.parent}"
        else:
            route = f"/{relative_path.with_suffix('')}"
        
        route = route.replace("\\", "/")
        
        def create_route_handler(file_path: Path):
            async def route_handler():
                return FileResponse(str(file_path), media_type="text/html")
            return route_handler
        
        app.get(route)(create_route_handler(html_file))
    
    for py_file in routes_path.rglob("*.py"):
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue

        relative_path = py_file.relative_to(routes_path)
        module_parts = [routes_dir] + list(relative_path.parent.parts) + [py_file.stem]
        module_name = ".".join(module_parts)

        prefix = "/" + str(relative_path.with_suffix("")).replace("\\", "/")

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                app.include_router(module.router, prefix=prefix)
        except Exception as e:
            print(f"Failed to load route module {module_name}: {e}")

