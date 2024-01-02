from . import (
    city_handlers,
    currency_handlers,
    email_verify_handler,
    task_handlers,
    common_handlers
)


routers = [
    city_handlers.router,
    currency_handlers.router,
    email_verify_handler.router,
    task_handlers.router,
    common_handlers.router
    ]
