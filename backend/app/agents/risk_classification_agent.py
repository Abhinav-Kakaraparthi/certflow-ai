from app.models.certification import AgentFinding, DesignChangeRequest, RiskLevel


class RiskClassificationAgent:
    name = "Risk Classification Agent"

    def analyze(self, case: DesignChangeRequest) -> AgentFinding:
        text = f"{case.aircraft_area} {case.component} {case.change_summary}".lower()
        missing_count = sum(1 for document in case.documents if not document.is_available)

        findings = []

        if missing_count > 0:
            findings.append(f"{missing_count} required evidence item(s) are missing.")

        if "avionics" in text or "controller" in text or "software" in text:
            findings.append("Change affects avionics, control logic, or software behavior.")

        if "bracket" in text or "frame" in text or "structural" in text:
            findings.append("Change may affect structural load path or substantiation.")

        if "material" in text or "composite" in text:
            findings.append("Material change may require equivalency and flammability review.")

        if not findings:
            findings.append("No major certification risk signals detected.")

        if "avionics" in text or "controller" in text or missing_count >= 3:
            risk_level = RiskLevel.HIGH
            next_step = "Escalate to DER or senior certification engineer for human review."
        elif missing_count > 0 or "bracket" in text or "frame" in text:
            risk_level = RiskLevel.MEDIUM
            next_step = "Hold case until missing evidence is provided and reviewed."
        else:
            risk_level = RiskLevel.LOW
            next_step = "Proceed with standard certification approval workflow."

        return AgentFinding(
            agent_name=self.name,
            summary="Classified certification risk based on affected system, change type, and evidence completeness.",
            risk_level=risk_level,
            findings=findings,
            recommended_next_step=next_step,
        )
