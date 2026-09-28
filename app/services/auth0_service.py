import requests

from jose import jwt, JWTError

from app.core.config import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID
)


# ==========================================
# AUTH0 CONFIGURATION
# ==========================================

AUTH0_ISSUER = (
    f"https://{AUTH0_DOMAIN}/"
)

AUTH0_JWKS_URL = (
    f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
)


# ==========================================
# GET AUTH0 PUBLIC SIGNING KEYS
# ==========================================

def get_auth0_jwks():

    try:

        response = requests.get(
            AUTH0_JWKS_URL,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        raise ValueError(
            "Unable to retrieve Auth0 signing keys"
        ) from error


# ==========================================
# VERIFY AUTH0 ID TOKEN
# ==========================================

def verify_auth0_token(
    token: str
):

    try:

        # --------------------------------------
        # Read token header
        # --------------------------------------

        unverified_header = (
            jwt.get_unverified_header(token)
        )

        token_kid = unverified_header.get(
            "kid"
        )

        if not token_kid:

            raise ValueError(
                "Token key ID is missing"
            )


        # --------------------------------------
        # Get Auth0 public keys
        # --------------------------------------

        jwks = get_auth0_jwks()

        rsa_key = None


        for key in jwks.get("keys", []):

            if key.get("kid") == token_kid:

                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

                break


        if rsa_key is None:

            raise ValueError(
                "Auth0 signing key not found"
            )


        # --------------------------------------
        # Verify Auth0 ID token
        # --------------------------------------

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=AUTH0_CLIENT_ID,
            issuer=AUTH0_ISSUER
        )


        return payload


    except (
        JWTError,
        ValueError,
        KeyError
    ) as error:

        raise ValueError(
            "Invalid Auth0 token"
        ) from error