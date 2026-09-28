from pydantic import BaseModel, EmailStr


# ==========================================
# NORMAL LOGIN
# ==========================================

class LoginRequest(BaseModel):

    email: EmailStr

    password: str


# ==========================================
# NORMAL / JWT RESPONSE
# ==========================================

class TokenResponse(BaseModel):

    access_token: str

    token_type: str


# ==========================================
# AUTH0 LOGIN
# ==========================================

class Auth0LoginRequest(BaseModel):

    access_token: str