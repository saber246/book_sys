import uvicorn
from fastapi import FastAPI
from routers import app_router
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(app_router)

register_tortoise(app, config = TORTOISE_ORM)

@app.get("/")
async def hello():
    return f"Hello, FastAPI! {TORTOISE_ORM['connections']['default']['credentials']['database']}"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port = 9090)