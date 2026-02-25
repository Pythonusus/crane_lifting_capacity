from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from .license_checker import LicenseChecker

def create_license_middleware(license_checker: LicenseChecker, excluded_routes:List[str] | None = None):
    async def license_middleware(request: Request, call_next):
        if excluded_routes is not None:
            if request.url.path in excluded_routes:
                return await call_next(request)

        try:
            await license_checker.check(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        response = await call_next(request)
        return response
    return license_middleware