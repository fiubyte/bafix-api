from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import create_db_and_tables, drop_db_and_tables, seed_db
from .routers import auth, service_categories, services, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up BA Fix API")
    create_db_and_tables()
    seed_db()
    yield

    drop_db_and_tables()
    print("Shutting down BA Fix API")


app = FastAPI(
    title="BA Fix API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(services.router, dependencies=[Depends(get_current_user())])
app.include_router(auth.router)
app.include_router(service_categories.router)
app.include_router(services.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
