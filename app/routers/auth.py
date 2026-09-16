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

from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.schemas.user import (
    UserCreate,
    UserResponse
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


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

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


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