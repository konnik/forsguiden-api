from typing import Any, Optional, List, Sequence
from forsguiden.auth import *


AUTH0_DOMAIN = "forsguiden.eu.auth0.com"
jwks = get_jwks(AUTH0_DOMAIN)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://forsguiden.eu.auth0.com/authorize",
    tokenUrl="https://forsguiden.eu.auth0.com/oauth/token",
    scopes={
        "lasa:hemlighet": "Läsa hemligheter.",
        "redigera:lan": "Skapa och redigera län.",
        "redigera:vattendrag": "Skapa och redigera vattendrag.",
        "redigera:forsstracka": "Skapa och redigera forssträckor.",
    },
)


def inloggad() -> Any:
    return auth0_token_authenticator_builder(
        auth0_domain=AUTH0_DOMAIN,
        api_audience="https://forsguiden.se/api",
        algorithms=["RS256"],
        jwks=jwks,
        oauth2_scheme=oauth2_scheme,
    )


def behorighet(scope: str) -> Any:
    return scope_verifier_builder(oauth2_scheme=oauth2_scheme, required_scope=scope)
