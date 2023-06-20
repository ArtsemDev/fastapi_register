from pathlib import Path

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext


BASE_DIR = Path(__file__).resolve().parent.parent
templating = Jinja2Templates(directory=BASE_DIR / 'templates')
static = StaticFiles(directory=BASE_DIR / 'static')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
