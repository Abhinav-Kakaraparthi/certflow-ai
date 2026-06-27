import json
from pathlib import Path
from typing import List

from app.models.certification import DesignChangeRequest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASE_DATA_PATH = PROJECT_ROOT / "demo-data" / "certification_cases.json"


def load_certification_cases() -> List[DesignChangeRequest]:
    with CASE_DATA_PATH.open("r", encoding="utf-8") as file:
        raw_cases = json.load(file)

    return [DesignChangeRequest(**case) for case in raw_cases]


def get_certification_case(case_id: str) -> DesignChangeRequest:
    cases = load_certification_cases()

    for case in cases:
        if case.case_id == case_id:
            return case

    raise ValueError(f"Certification case not found: {case_id}")
