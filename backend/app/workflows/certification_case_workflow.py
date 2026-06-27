from typing import List

from app.agents.certification_basis_agent import CertificationBasisAgent
from app.agents.evidence_gap_agent import EvidenceGapAgent
from app.agents.risk_classification_agent import RiskClassificationAgent
from app.models.certification import (
    AgentFinding,
    CaseStatus,
    CertificationCaseResult,
    DesignChangeRequest,
    RiskLevel,
)


class CertificationCaseWorkflow:
    def __init__(self):
        self.agents = [
            CertificationBasisAgent(),
            EvidenceGapAgent(),
            RiskClassificationAgent(),
        ]

    def run(self, case: DesignChangeRequest) -> CertificationCaseResult:
        findings = [agent.analyze(case) for agent in self.agents]
        missing_documents = self._get_missing_documents(case)
        overall_risk = self._get_overall_risk(findings)
        human_review_required = self._requires_human_review(
            overall_risk=overall_risk,
            missing_documents=missing_documents,
        )
        status = self._get_case_status(
            overall_risk=overall_risk,
            missing_documents=missing_documents,
            human_review_required=human_review_required,
        )

        return CertificationCaseResult(
            case_id=case.case_id,
            status=status,
            overall_risk=overall_risk,
            findings=findings,
            missing_documents=missing_documents,
            human_review_required=human_review_required,
            final_summary=self._build_final_summary(
                case=case,
                overall_risk=overall_risk,
                missing_documents=missing_documents,
                human_review_required=human_review_required,
            ),
        )

    def _get_missing_documents(self, case: DesignChangeRequest) -> List[str]:
        return [
            document.document_name
            for document in case.documents
            if not document.is_available
        ]

    def _get_overall_risk(self, findings: List[AgentFinding]) -> RiskLevel:
        risk_rank = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
        }

        return max(findings, key=lambda finding: risk_rank[finding.risk_level]).risk_level

    def _requires_human_review(
        self,
        overall_risk: RiskLevel,
        missing_documents: List[str],
    ) -> bool:
        return overall_risk in {RiskLevel.MEDIUM, RiskLevel.HIGH} or bool(missing_documents)

    def _get_case_status(
        self,
        overall_risk: RiskLevel,
        missing_documents: List[str],
        human_review_required: bool,
    ) -> CaseStatus:
        if missing_documents:
            return CaseStatus.NEEDS_MORE_EVIDENCE

        if human_review_required:
            return CaseStatus.WAITING_FOR_HUMAN

        if overall_risk == RiskLevel.LOW:
            return CaseStatus.APPROVED

        return CaseStatus.IN_REVIEW

    def _build_final_summary(
        self,
        case: DesignChangeRequest,
        overall_risk: RiskLevel,
        missing_documents: List[str],
        human_review_required: bool,
    ) -> str:
        if missing_documents:
            return (
                f"Case {case.case_id} requires additional certification evidence before approval. "
                f"Missing documents: {', '.join(missing_documents)}. "
                f"Overall risk is {overall_risk.value}."
            )

        if human_review_required:
            return (
                f"Case {case.case_id} requires human certification review before approval. "
                f"Overall risk is {overall_risk.value} due to certification impact signals."
            )

        return (
            f"Case {case.case_id} has complete evidence and low certification risk. "
            "The case can proceed through the standard approval workflow."
        )
