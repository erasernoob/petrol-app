# api/routes/torque.py
from fastapi import Response
import io
from fastapi import APIRouter
import pandas as pd
from entity.DTO import TorqueDTO
from service.Hydro import Hydro

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
torque_cache = {}

    