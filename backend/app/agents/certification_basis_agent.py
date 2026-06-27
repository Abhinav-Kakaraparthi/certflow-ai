from app.models.certification import AgentFinding, DesignChangeRequest, RiskLevel


class CertificationBasisAgent:
    name = "Certification Basis Agent"

    def analyze(self, case: DesignChangeRequest) -> AgentFinding:
        affected_areas = []

        text = f"{case.aircraft_area} {case.component} {case.change_summary}".lower()
        missing_count = sum(1 for document in case.documents if not document.is_available)

        has_structural_signal = any(
            keyword in text
            for keyword in ["bracket", "frame", "structural", "load path"]
        )
        has_avionics_signal = any(
            keyword in text
            for keyword in ["avionics", "controller", "software", "electrical interface"]
        )
        has_material_signal = any(
            keyword in text
            for keyword in ["material", "composite"]
        )

        if "seat" in text:
            affected_areas.append("Cabin interior compliance")

        if has_structural_signal:
            affected_areas.extend([
                "Seat strength and occupant safety",
                "Structural substantiation",
            ])

        if has_material_signal:
            affected_areas.extend([
                "Material equivalency",
                "Flammability compliance",
            ])

        if has_avionics_signal:
            affected_areas.extend([
                "System safety assessment",
                "Electrical interface compatibility",
                "Software verification evidence",
            ])

        if not affected_areas:
            affected_areas.append("General certification impact review")

        if has_avionics_signal or missing_count >= 3:
            risk_level = RiskLevel.HIGH
        elif has_structural_signal or missing_count > 0:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW

        return AgentFinding(
            agent_name=self.name,
            summary="Identified certification areas that may be affected by the design change.",
            risk_level=risk_level,
            findings=affected_areas,
            recommended_next_step="Confirm certification basis with the responsible certification engineer.",
        )
