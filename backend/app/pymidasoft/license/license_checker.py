from fastapi import Request, HTTPException
import httpx
import json


class LicenseChecker:
    def __init__(self, plugin_name: str, license_server_url: str):
        self.plugin_name = plugin_name
        self.license_server_url = license_server_url

    def is_need_check(self, request: Request) -> bool:
        # TODO: Sessions
        return True

    def set_last_check_result(self, request: Request, available: bool, error: str = None):
        # TODO: Sessions
        pass

    def get_last_check_result(self, request: Request):
        # TODO: Sessions
        pass

    async def send_request(self, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.license_server_url, json=data, follow_redirects=True)
            return json.loads(response.text)

    async def check(self, request: Request):
        if self.is_need_check(request):
            jwt = request.headers.get("X-License-JWT")
            if jwt is None:
                jwt = "empty"
            fp = request.headers.get("X-License-FP")
            if fp is None:
                fp = "empty"
            x_forwarded_for = request.headers.get("x-forwarded-for")
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(",")[0].strip()
            else:
                client_ip = request.client.host

            data = {
                "app": self.plugin_name,
                "jwt": jwt,
                "fp": fp,
                "ip": client_ip,
            }

            try:
                response_data = await self.send_request(data)
                available = response_data.get("available", False)
                error = response_data.get("error", None)
            except Exception:
                self.set_last_check_result(request, False, "License server request error")
                raise HTTPException(status_code=500, detail="License server request error")

            self.set_last_check_result(request, available, error)

            if not available:
                raise HTTPException(status_code=403, detail=error or "Unauthorized access")
        else:
            # TODO: Sessions
            self.get_last_check_result(request)


class FakeLicenseChecker:
    def check(self, _: Request):
        return True


def create_license_checker(name: str, url: str, debug: bool) -> LicenseChecker | FakeLicenseChecker:
    if debug:
        return FakeLicenseChecker()
    return LicenseChecker(name, url)
