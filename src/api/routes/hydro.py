# api/routes/hydro.py
from fastapi import APIRouter
from api.entity.DTO import HydroDTO

# 创建 APIRouter 实例
router = APIRouter()

@router.post("/hydro")
async def get_hydro_params(data: HydroDTO):
    print(data)
    return {"message": "Hydro data received", "data": data}
