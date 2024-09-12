from fastapi import APIRouter, Request
from utils.excute_fun import excute_fun
import json
api_router = APIRouter()

@api_router.post("/execute")
async def execute(request: Request):
    body = await request.body()
    body_str = body.decode('utf-8')
    user_input = json.loads(body_str)["user_input"]
    return excute_fun(user_input)
