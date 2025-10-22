import os
import importlib
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse


def register_routes(app: FastAPI, routes_dir: str = "routes"):
    """
    Next.js-style file-based routing. Automatically register both HTML pages 
    and API routes from the routes directory.
    
    HTML Files:
        routes/index.html -> GET /
        routes/privacy.html -> GET /privacy
        routes/about.html -> GET /about
        routes/docs/api.html -> GET /docs/api
    
    Python Files (with router):
        routes/whatsapp.py -> includes router at /webhook/whatsapp
        routes/health.py -> includes router at /health
        routes/api/users.py -> includes router
    """
    here = Path(__file__).parent.parent
    routes_path = here / routes_dir
    
    if not routes_path.exists():
        return
    
    # Register HTML files
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
    
    # Register Python API routes
    for py_file in routes_path.rglob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        relative_path = py_file.relative_to(routes_path)
        module_parts = [routes_dir] + list(relative_path.parent.parts) + [py_file.stem]
        module_name = ".".join(module_parts)
        
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                app.include_router(module.router)
        except Exception as e:
            print(f"Failed to load route module {module_name}: {e}")

