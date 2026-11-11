from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import require_auth
from app.core.config import settings
from app.database.db import get_db
from app.database.models import AuditEvent
from app.adapters.vast import VastClient
from app.adapters.comfyui import ComfyClient

router = APIRouter(prefix="/api/v1", dependencies=[Depends(require_auth)])
vast = VastClient()
comfy = ComfyClient()

@router.get("/system/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok", "database": "connected", "environment": settings.app_env}

@router.get("/gpu/offers")
async def gpu_offers(max_price: float | None = None):
    ceiling = min(max_price or settings.vast_max_hourly_price, settings.vast_max_hourly_price)
    return await vast.search_offers({"order": [["dph_total", "asc"]], "type": "on-demand", "limit": 30, "rentable": {"eq": True}, "dph_total": {"lte": ceiling}})

@router.get("/gpu/instances")
async def gpu_instances():
    return await vast.list_instances()

@router.post("/gpu/instances/{offer_id}")
async def create_gpu_instance(offer_id: int, payload: dict, db: Session = Depends(get_db)):
    result = await vast.create_instance(offer_id, payload)
    db.add(AuditEvent(actor="admin", action="gpu.provision", resource=str(offer_id), detail="Provision request accepted"))
    db.commit()
    return result

@router.post("/gpu/instances/{instance_id}/stop")
async def stop_gpu_instance(instance_id: int):
    return await vast.stop_instance(instance_id)

@router.delete("/gpu/instances/{instance_id}")
async def destroy_gpu_instance(instance_id: int):
    return await vast.destroy_instance(instance_id)

@router.get("/comfy/status")
async def comfy_status():
    return await comfy.status()

@router.post("/comfy/prompt")
async def submit_comfy_prompt(payload: dict):
    workflow = payload.get("workflow")
    if not isinstance(workflow, dict) or not workflow:
        raise HTTPException(400, "workflow must be a non-empty API-format ComfyUI workflow")
    return await comfy.submit(workflow, str(payload.get("client_id", "ai-studio-hq")))

@router.get("/comfy/history/{prompt_id}")
async def comfy_history(prompt_id: str):
    return await comfy.history(prompt_id)
