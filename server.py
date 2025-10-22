from fastapi import FastAPI
from dotenv import load_dotenv
from utils.routing import register_routes

load_dotenv()

app = FastAPI()

register_routes(app, routes_dir="routes")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)