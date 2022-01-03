from main import add_routes
from fastapi import FastAPI

web_app = FastAPI()
add_routes(web_app)
