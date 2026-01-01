from .routes import *
from fastapi import APIRouter
from .storage.file_storage import STORAGE_DIR
router = APIRouter(prefix="/management", tags=["Management"])

router.include_router(channels.router)
router.include_router(subscription.router)
router.include_router(videos.router)
router.include_router(playlists.router)
router.include_router(comments.router)
router.include_router(auth.router)