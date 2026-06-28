import json
from pathlib import Path
from typing import List, Optional

from app.models.enterprise import (
    AuditEvent,
    EnterpriseCaseSnapshot,
    EnterpriseUser,
    EvidenceRecord,
)


BACKEND_ROOT = Path(__file__).resolve().parents[2]
DEMO_DATA_ROOT = BACKEND_ROOT / "demo-data"


def _load_json_file(file_name: str) -> list[dict]:
    file_path = DEMO_DATA_ROOT / file_name
    with file_path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_users() -> List[EnterpriseUser]:
    return [EnterpriseUser(**item) for item in _load_json_file("users.json")]


def load_evidence_records() -> List[EvidenceRecord]:
    return [EvidenceRecord(**item) for item in _load_json_file("evidence_registry.json")]


def load_audit_events() -> List[AuditEvent]:
    return [AuditEvent(**item) for item in _load_json_file("audit_events.json")]


def get_user_by_id(user_id: Optional[str]) -> Optional[EnterpriseUser]:
    if not user_id:
        return None

    for user in load_users():
        if user.user_id == user_id:
            return user

    return None


def get_case_enterprise_snapshot(case_id: str) -> EnterpriseCaseSnapshot:
    evidence_records = [
        record for record in load_evidence_records()
        if record.case_id == case_id
    ]

    audit_events = [
        event for event in load_audit_events()
        if event.case_id == case_id
    ]

    owner_id = evidence_records[0].assigned_reviewer if evidence_records else None
    owner = get_user_by_id(owner_id)

    missing_evidence_count = len([
        record for record in evidence_records
        if record.status == "missing"
    ])

    blocked_evidence_count = len([
        record for record in evidence_records
        if record.status == "blocked"
    ])

    latest_action = audit_events[-1] if audit_events else None

    return EnterpriseCaseSnapshot(
        case_id=case_id,
        owner=owner,
        evidence_records=evidence_records,
        audit_events=audit_events,
        missing_evidence_count=missing_evidence_count,
        blocked_evidence_count=blocked_evidence_count,
        latest_action=latest_action,
    )


def get_enterprise_summary() -> dict:
    users = load_users()
    evidence_records = load_evidence_records()
    audit_events = load_audit_events()

    active_cases = sorted({record.case_id for record in evidence_records})
    missing_count = len([record for record in evidence_records if record.status == "missing"])
    blocked_count = len([record for record in evidence_records if record.status == "blocked"])
    accepted_count = len([record for record in evidence_records if record.status == "accepted"])

    team_workload = {}
    for record in evidence_records:
        reviewer = get_user_by_id(record.assigned_reviewer)
        team = reviewer.team if reviewer else "Unassigned"
        team_workload[team] = team_workload.get(team, 0) + 1

    role_counts = {}
    for user in users:
        role_counts[user.role] = role_counts.get(user.role, 0) + 1

    return {
        "active_cases": len(active_cases),
        "total_evidence_records": len(evidence_records),
        "missing_evidence": missing_count,
        "blocked_evidence": blocked_count,
        "accepted_evidence": accepted_count,
        "audit_events": len(audit_events),
        "team_workload": team_workload,
        "role_counts": role_counts,
    }
