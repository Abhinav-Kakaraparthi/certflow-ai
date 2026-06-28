from fastapi import APIRouter

from app.api import ai, cases, document_workspace, enterprise, uipath, workflow


router = APIRouter()

router.include_router(cases.router)
router.include_router(workflow.router)
router.include_router(uipath.router)
router.include_router(ai.router)
router.include_router(enterprise.router)
router.include_router(document_workspace.router)

