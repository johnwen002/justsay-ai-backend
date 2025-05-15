from fastapi import FastAPI

app = FastAPI()


from src.routes import *  # noqa
