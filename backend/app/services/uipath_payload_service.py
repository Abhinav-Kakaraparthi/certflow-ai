from app.models.certification import CertificationCaseResult, RiskLevel


def build_uipath_case_payload(result: CertificationCaseResult) -> dict:
    if result.missing_documents:
        next_action = "request_missing_evidence"
        stage = "Evidence Collection"
        task_title = "Request missing certification evidence"
        assigned_role = "Certification Engineer"
    elif result.overall_risk == RiskLevel.HIGH:
        next_action = "create_der_review_task"
        stage = "DER Review"
        task_title = "Review high-risk certification impact"
        assigned_role = "DER / Senior Certification Engineer"
    elif result.human_review_required:
        next_action = "create_human_review_task"
        stage = "Certification Review"
        task_title = "Review certification case"
        assigned_role = "Certification Engineer"
    else:
        next_action = "auto_approve_case"
        stage = "Case Closure"
        task_title = "Auto-approve low-risk certification case"
        assigned_role = "Automation"

    return {
        "case_id": result.case_id,
        "case_status": result.status.value,
        "overall_risk": result.overall_risk.value,
        "human_review_required": result.human_review_required,
        "missing_documents": result.missing_documents,
        "next_uipath_action": next_action,
        "maestro_stage": stage,
        "task_title": task_title,
        "assigned_role": assigned_role,
        "agent_summary": result.final_summary,
        "agent_findings": [
            {
                "agent_name": finding.agent_name,
                "summary": finding.summary,
                "risk_level": finding.risk_level.value,
                "findings": finding.findings,
                "recommended_next_step": finding.recommended_next_step,
            }
            for finding in result.findings
        ],
    }
