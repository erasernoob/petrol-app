# api/routes/hydro.py
from fastapi import APIRouter
from api.entity.DTO import HydroDTO
from service.Hydro.main import process_hydro_data

# 创建 APIRouter 实例
router = APIRouter()

@router.post("/hydro")
async def get_hydro_params(data: HydroDTO):
    if data:
        return await process_hydro_data

