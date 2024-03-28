import uvicorn
from fastapi import FastAPI
from src.routes import contacts, auth, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ipaddress import ip_address
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import re

origins = [
    "http://localhost:3000"
    ]

banned_ips = [ip_address("192.168.1.1"), ip_address("192.168.1.2"), ip_address("127.0.0.1")]
ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]
user_agent_ban_list = [r"Gecko", r"Python-urllib"]

app = FastAPI()


# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
    response = await call_next(request)
    return response


# Funkcja pośrednicząca user_agent_ban_middleware sprawdza nagłówek "user-agent" w nadchodzących żądaniach pod kątem zgodności z listą zabronionych ciągów agentów użytkownika przechowywaną w user_agent_ban_list. 
@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')





@app.get("/")
def read_root():
    return {"message": "Hello in my application!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)