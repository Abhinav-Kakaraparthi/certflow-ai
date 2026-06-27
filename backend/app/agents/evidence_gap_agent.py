from app.models.certification import AgentFinding, DesignChangeRequest, RiskLevel


class EvidenceGapAgent:
    name = "Evidence Gap Agent"

    def analyze(self, case: DesignChangeRequest) -> AgentFinding:
        missing_documents = [
            document.document_name
            for document in case.documents
            if not document.is_available
        ]

        if not missing_documents:
            return AgentFinding(
                agent_name=self.name,
                summary="All listed certification evidence is available.",
                risk_level=RiskLevel.LOW,
                findings=["No missing documents detected."],
                recommended_next_step="Proceed to certification engineer review or approval.",
            )

        risk_level = RiskLevel.HIGH if len(missing_documents) >= 3 else RiskLevel.MEDIUM

        return AgentFinding(
            agent_name=self.name,
            summary="Missing certification evidence was detected.",
            risk_level=risk_level,
            findings=[f"Missing evidence: {name}" for name in missing_documents],
            recommended_next_step="Request missing evidence before certification approval.",
        )
