from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)

from app.database.connection import (
    get_db
)

from app.dependencies.auth import (
    get_current_user
)

from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    Auth0LoginRequest
)

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.services.auth0_service import (
    verify_auth0_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# NORMAL REGISTER
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    # Check email
    existing_email = db.query(
        User
    ).filter(
        User.email == user_data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Check username
    existing_username = db.query(
        User
    ).filter(
        User.username == user_data.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Hash password
    hashed_password = hash_password(
        user_data.password
    )

    # Create local user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        provider="local"
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


# ==========================================
# NORMAL LOGIN
# ==========================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(
        User
    ).filter(
        User.email == login_data.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Social users do not have a local password
    if user.password is None:

        raise HTTPException(
            status_code=401,
            detail=(
                "This account uses social login. "
                "Please continue with Google or Facebook."
            )
        )

    password_valid = verify_password(
        login_data.password,
        user.password
    )

    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================
# AUTH0 LOGIN
# ==========================================

@router.post(
    "/auth0",
    response_model=TokenResponse
)
def auth0_login(
    auth0_data: Auth0LoginRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------
    # Verify Auth0 token
    # --------------------------------------

    try:

        payload = verify_auth0_token(
            auth0_data.access_token
        )

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Auth0 token"
        )

    # --------------------------------------
    # Get Auth0 user information
    # --------------------------------------

    auth0_id = payload.get(
        "sub"
    )

    email = payload.get(
        "email"
    )

    name = payload.get(
        "name"
    )

    if not auth0_id:

        raise HTTPException(
            status_code=400,
            detail="Auth0 user ID is missing"
        )

    if not email:

        raise HTTPException(
            status_code=400,
            detail="Email is missing from Auth0 profile"
        )

    # --------------------------------------
    # Determine provider
    # --------------------------------------

    if auth0_id.startswith(
        "google-oauth2|"
    ):

        provider = "google"

    elif auth0_id.startswith(
        "facebook|"
    ):

        provider = "facebook"

    else:

        provider = "auth0"

    # --------------------------------------
    # Find user by Auth0 ID
    # --------------------------------------

    user = db.query(
        User
    ).filter(
        User.auth0_id == auth0_id
    ).first()

    # --------------------------------------
    # If user doesn't exist,
    # check email
    # --------------------------------------

    if not user:

        user = db.query(
            User
        ).filter(
            User.email == email
        ).first()

    # --------------------------------------
    # Create new social user
    # --------------------------------------

    if not user:

        username = name or email.split("@")[0]

        # Make username unique
        original_username = username
        counter = 1

        while db.query(
            User
        ).filter(
            User.username == username
        ).first():

            username = (
                f"{original_username}{counter}"
            )

            counter += 1

        user = User(
            username=username,
            email=email,
            password=None,
            provider=provider,
            auth0_id=auth0_id
        )

        db.add(user)

        db.commit()

        db.refresh(user)

    # --------------------------------------
    # Existing user
    # --------------------------------------

    else:

        # Link Auth0 account if not already linked
        if not user.auth0_id:

            user.auth0_id = auth0_id

            user.provider = provider

            db.commit()

            db.refresh(user)

    # --------------------------------------
    # Create application JWT
    # --------------------------------------

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================
# GET CURRENT USER PROFILE
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user