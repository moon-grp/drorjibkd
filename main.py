from fastapi import FastAPI
from routes.superadmin.authsignup import supadmin
from routes.superadmin.signin import superAdmin
from routes.users.auth import aff
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(supadmin, prefix="/api/v1/admin")
app.include_router(superAdmin, prefix="/api/v1/admin")
app.include_router(aff, prefix="/api/v1/users")