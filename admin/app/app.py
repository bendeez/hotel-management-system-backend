from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.facility.application.endpoints import facility_router
from app.chat.application.endpoints import chat_router
from app.business.application.endpoints import business_router
from app.auth.application.endpoints import auth_router
from app.user.application.endpoints import user_router
from app.session.application.endpoints import session_router
from app.business_user.application.endpoints import business_user_router
from app.hotels.application.endpoints import hotels_router
from app.exception_handlers import add_exception_handlers
from app.tools.application.rate_limiter import limiter


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
app.include_router(hotels_router)
