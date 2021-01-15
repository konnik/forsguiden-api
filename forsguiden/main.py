import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import psycopg2.pool

from forsguiden.model import *
from forsguiden.db import Db
from forsguiden.db.postgres import PostgresDb, DbInfo
from forsguiden.db.inmemory import InMemoryDb

from forsguiden.dependencies import on_database
from forsguiden.routers.lan import router as lan_router
from forsguiden.routers.vattendrag import router as vattendrag_router
from forsguiden.routers.forsstracka import router as forsstracka_router

import dotenv

dotenv.load_dotenv()

app: FastAPI = FastAPI(
    title="Forsguiden API",
    description="Målet med Forsguiden API är att samla all information om sveriges forspaddlingsvatten och göra det tillgängligt i ett strukturerat, öppet och väldokumenterat format så att vem som helst ska kunna använda informationen för att bygga egna smarta webapplikationer och mobilappar.",
    version="0.1-UTRABETA",
)

app.include_router(lan_router)
app.include_router(vattendrag_router)
app.include_router(forsstracka_router)


# test av
from forsguiden.auth import *

AUTH0_DOMAIN = "forsguiden.eu.auth0.com"

jwks = get_jwks(AUTH0_DOMAIN)
autentiserad_anvandare = auth0_token_authenticator_builder(
    api_audience="https://forsguiden.se/api",
    auth0_domain=AUTH0_DOMAIN,
    algorithms=["RS256"],
    jwks=get_jwks(AUTH0_DOMAIN),
    oauth2_scheme=OAuth2AuthorizationCodeBearer(
        authorizationUrl="https://forsguiden.eu.auth0.com/authorize",
        tokenUrl="https://forsguiden.eu.auth0.com/oauth/token",
    ),
)


@app.exception_handler(AuthError)
def handle_auth_error(request: Request, ex: AuthError):
    return JSONResponse(status_code=ex.status_code, content=ex.error)


@app.get("/hemlig", dependencies=[Depends(autentiserad_anvandare)])
async def hemlig():
    return {"meddelande": "Superhemligt..."}


@app.on_event("startup")
async def startup():
    app.state.pool = psycopg2.pool.ThreadedConnectionPool(
        1, 20, os.environ["DATABASE_URL"]
    )


@app.on_event("shutdown")
async def shutdown():
    app.state.pool.closeall()
