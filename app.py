from fastapi import FastAPI

from src.settings import static
from src.auth.views import router as auth_router
from src.handlers import login
# from src.models import Base


app = FastAPI(
    exception_handlers={
        401: login
    }
)
app.include_router(auth_router)
app.mount('/static', static, 'static')
# Base.metadata.create_all(Base.engine)
