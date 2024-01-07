from . import (
    admin_handlers,
    city_handlers,
    currency_handlers,
    email_verify_handler,
    task_handlers,
    common_handlers,
)
from .callbacks import task_callbacks


routers = [
    common_handlers.dropstate_router,
    admin_handlers.router,
    city_handlers.router,
    currency_handlers.router,
    email_verify_handler.router,
    task_handlers.router,
    task_callbacks.router,
    common_handlers.router,
]
