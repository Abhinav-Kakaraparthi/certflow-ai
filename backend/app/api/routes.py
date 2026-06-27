from fastapi import APIRouter

from app.api import ai, cases, uipath, workflow


router = APIRouter()

router.include_router(cases.router)
router.include_router(workflow.router)
router.include_router(uipath.router)
router.include_router(ai.router)
