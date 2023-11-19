from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from .v1 import router as v1_router
from core import get_db
from services import user_service
from schemas import UserRead

router = APIRouter(prefix="/api")


@v1_router.get("/ip")
async def get_ip(request: Request):
    return request.client.host


@v1_router.get("/whoami", dependencies=[Depends(HTTPBearer())],
            response_model=UserRead,
            summary="Get user info")
async def get_whoami(*,
                    db: Session = Depends(get_db),
                    Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        return user_service.get_by_id(db, user_id)


router.include_router(v1_router)