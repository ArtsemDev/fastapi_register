from starlette.requests import Request
from starlette.responses import RedirectResponse


async def login(request: Request, exception):
    return RedirectResponse('/login')
