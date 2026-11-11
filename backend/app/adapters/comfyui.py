import httpx
from fastapi import HTTPException
from app.core.config import settings

class ComfyClient:
    async def request(self, method: str, path: str, **kwargs):
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.request(method, settings.comfyui_base_url.rstrip("/") + path, **kwargs)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise HTTPException(502, f"ComfyUI is unavailable: {exc}") from exc
        return response.json() if response.content else {}

    async def status(self):
        stats, queue = await self.request("GET", "/system_stats"), await self.request("GET", "/queue")
        return {"system": stats, "queue": queue}

    async def submit(self, workflow: dict, client_id: str):
        return await self.request("POST", "/prompt", json={"prompt": workflow, "client_id": client_id})

    async def history(self, prompt_id: str):
        return await self.request("GET", f"/history/{prompt_id}")
