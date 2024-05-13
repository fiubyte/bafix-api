from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db, drop_db, seed_db
from .routers import auth, service_categories, services, users
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up BA Fix API")
    drop_db()
    init_db()
    seed_db()
    yield

    drop_db()
    print("Shutting down BA Fix API")


app = FastAPI(
    title="BA Fix API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(service_categories.router)
app.include_router(services.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/service/{service_id}")
def redirect_to_web(service_id: str):
    return RedirectResponse(f"https://bafix-web.vercel.app/{service_id}")

@app.get("/.well-known/assetlinks.json")
def read_root():
    return [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.fiubyte.bafix",
            "sha256_cert_fingerprints":
                ["5B:EE:77:69:FF:84:0B:F1:F4:D6:0A:9C:C6:E6:06:A2:27:DA:20:DC:61:0A:0A:BB:9B:53:3A:40:21:4F:52:64"]
        }
    }]

    # return """
    # [{
    #   "relation": ["delegate_permission/common.handle_all_urls"],
    #   "target": {
    #     "namespace": "android_app",
    #     "package_name": "com.fiubyte.bafix",
    #     "sha256_cert_fingerprints":
    #     ["5B:EE:77:69:FF:84:0B:F1:F4:D6:0A:9C:C6:E6:06:A2:27:DA:20:DC:61:0A:0A:BB:9B:53:3A:40:21:4F:52:64"]
    #   }
    # }]
    # """