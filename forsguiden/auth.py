import json
from urllib.request import urlopen
from jose import jwt
from typing import Dict
from fastapi import Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import List

# lånat från: https://github.com/tiangolo/fastapi/issues/840


class AuthError(Exception):
    """ Error handling object """

    def __init__(self, error: Dict[str, str], status_code: int):
        self.error = error
        self.status_code = status_code


def get_jwks(auth0_domain: str):
    json_url = urlopen(f"https://{auth0_domain}/.well-known/jwks.json")
    return json.loads(json_url.read())


def auth0_token_authenticator_builder(
    oauth2_scheme: OAuth2AuthorizationCodeBearer,
    auth0_domain: str,
    api_audience: str,
    algorithms: List[str],
    jwks: dict,
):
    def auth0_token_authentication(token: str = Security(oauth2_scheme)):
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = None
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if not rsa_key:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to find appropriate key",
                },
                401,
            )

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=algorithms,
                audience=api_audience,
                issuer=f"https://{auth0_domain}/",
            )
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "token is expired"}, 401
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer",
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                401,
            )

        return payload

    return auth0_token_authentication


def scope_verifier_builder(
    oauth2_scheme: OAuth2AuthorizationCodeBearer, required_scope
):
    def scope_verifier(token: str = Security(oauth2_scheme)):
        unverified_claims = jwt.get_unverified_claims(token)
        if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
        raise AuthError(
            {
                "code": "no_required_permissions",
                "description": "user does not have the required permissions",
            },
            403,
        )

    return scope_verifier