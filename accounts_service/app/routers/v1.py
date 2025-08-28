from fastapi import APIRouter, status, HTTPException

router = APIRouter()


@router.post("/login")
def login(credentials: dict):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
