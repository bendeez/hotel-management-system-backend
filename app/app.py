from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.facility.endpoints import facility_router
from app.chat.endpoints import chat_router
from app.business.endpoints import business_router
from app.auth.endpoints import auth_router
from app.user.endpoints import user_router
from app.exception_handlers import add_exception_handlers


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://chat.brisbanegateway.com.au"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app=app)
app.include_router(facility_router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(business_router)
