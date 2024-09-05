from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from admin.app.facility.endpoints import facility_router
from admin.app.app import chat_router
from admin.app.business.endpoints import business_router
from admin.app.auth.endpoints import auth_router
from admin.app.user.endpoints import user_router
from admin.app.app import session_router
from admin.app.app import business_user_router
from admin.app.app import add_exception_handlers
from admin.app.tools.rate_limiter import limiter


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://chat.brisbanegateway.com.au"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter

add_exception_handlers(app=app)
app.include_router(facility_router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(business_router)
app.include_router(business_user_router)
app.include_router(session_router)
