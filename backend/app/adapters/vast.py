import httpx
from fastapi import HTTPException
from app.core.config import settings

class VastClient:
    def __init__(self):
        self.base = settings.vast_api_base.rstrip("/")
        self.headers = {"Authorization": f"Bearer {settings.vast_api_key}"} if settings.vast_api_key else {}

    def _ready(self):
        if not settings.vast_api_key:
            raise HTTPException(503, "Vast.ai API key is not configured")

    async def _request(self, method: str, path: str, **kwargs):
        self._ready()
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.request(method, f"{self.base}{path}", headers=self.headers, **kwargs)
        if response.is_error:
            raise HTTPException(response.status_code, f"Vast.ai request failed: {response.text[:500]}")
        return response.json() if response.content else {}

    async def search_offers(self, filters: dict):
        return await self._request("POST", "/bundles/", json=filters)

    async def list_instances(self):
        return await self._request("GET", "/instances/")

    async def create_instance(self, offer_id: int, payload: dict):
        if not settings.vast_provisioning_enabled:
            raise HTTPException(403, "GPU provisioning is disabled by configuration")
        price = float(payload.get("price", 0) or 0)
        if price > settings.vast_max_hourly_price:
            raise HTTPException(400, "Requested hourly price exceeds configured safety limit")
        return await self._request("PUT", f"/asks/{offer_id}/", json=payload)

    async def stop_instance(self, instance_id: int):
        return await self._request("PUT", f"/instances/{instance_id}/", json={"state": "stopped"})

    async def destroy_instance(self, instance_id: int):
        return await self._request("DELETE", f"/instances/{instance_id}/")
