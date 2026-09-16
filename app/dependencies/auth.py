from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import JWTError

from sqlalchemy.orm import Session

from app.core.security import (
    decode_access_token
)

from app.database.connection import (
    get_db
)

from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(
        get_db
    )
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token = credentials.credentials

    try:

        payload = decode_access_token(
            token
        )

        user_id = payload.get(
            "sub"
        )

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (
        JWTError,
        ValueError
    ):

        raise credentials_exception

    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()

    if user is None:

        raise credentials_exception

    return user