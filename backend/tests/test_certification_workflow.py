from app.services.case_data_service import get_certification_case, load_certification_cases
from app.workflows.certification_case_workflow import CertificationCaseWorkflow


def test_demo_cases_load_successfully():
    cases = load_certification_cases()

    assert len(cases) == 3
    assert cases[0].case_id == "CERT-001"


def test_clean_case_is_auto_approved():
    case = get_certification_case("CERT-001")
    result = CertificationCaseWorkflow().run(case)

    assert result.case_id == "CERT-001"
    assert result.status.value == "approved"
    assert result.overall_risk.value == "low"
    assert result.human_review_required is False


def test_structural_case_requests_more_evidence():
    case = get_certification_case("CERT-002")
    result = CertificationCaseWorkflow().run(case)

    assert result.case_id == "CERT-002"
    assert result.status.value == "needs_more_evidence"
    assert result.overall_risk.value == "medium"
    assert result.human_review_required is True
    assert "Stress Analysis Report" in result.missing_documents
    assert "Test Report" in result.missing_documents


def test_avionics_case_is_high_risk():
    case = get_certification_case("CERT-003")
    result = CertificationCaseWorkflow().run(case)

    assert result.case_id == "CERT-003"
    assert result.status.value == "needs_more_evidence"
    assert result.overall_risk.value == "high"
    assert result.human_review_required is True
    assert "System Safety Assessment" in result.missing_documents
    assert "Software Verification Evidence" in result.missing_documents
    assert "DER Review Record" in result.missing_documents
