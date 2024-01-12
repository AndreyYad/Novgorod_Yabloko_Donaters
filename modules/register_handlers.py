from handlers.generic import register_generic_handlers
from handlers.callbacks import register_callbacks
from handlers.admin import register_admin_handlers

async def register_handlers():
    await register_generic_handlers()
    await register_callbacks()
    await register_admin_handlers()