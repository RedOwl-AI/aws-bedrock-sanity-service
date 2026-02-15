from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", status_code=200)
def health():
    """Health check endpoint. Returns 200 OK."""
    return {"status": "ok"}
