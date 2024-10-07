from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.admin_app.facility.application.endpoints import facility_router
from apps.admin_app.chat.application.endpoints import chat_router
from apps.admin_app.business.application.endpoints import business_router
from apps.admin_app.auth.application.endpoints import auth_router
from apps.admin_app.user.application.endpoints import user_router
from apps.admin_app.session.application.endpoints import session_router
from apps.admin_app.business_user.application.endpoints import business_user_router
from apps.admin_app.exception_handlers import add_exception_handlers
from tools.application.rate_limiter import limiter


admin_app = FastAPI()
admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
admin_app.state.limiter = limiter

add_exception_handlers(app=admin_app)
admin_app.include_router(facility_router)
admin_app.include_router(chat_router)
admin_app.include_router(auth_router)
admin_app.include_router(user_router)
admin_app.include_router(business_router)
admin_app.include_router(business_user_router)
admin_app.include_router(session_router)
