import { AlertTriangle, CheckCircle2, FileSearch, Route } from "lucide-react";

const decisionRules = {
  "CERT-001": {
    riskDrivers: [
      "Cabin interior component",
      "Material/latch update only",
      "No software or avionics control logic affected",
      "Required evidence is complete",
    ],
    evidenceRule:
      "Cabin material or latch changes require material certification, design change summary, and conformity evidence.",
    availableEvidence: [
      "Material Certification",
      "Design Change Summary",
      "Conformity Evidence",
    ],
    routingReason:
      "Because the component is non-critical cabin equipment and all required evidence is present, UiPath can route the case to auto approval.",
  },
  "CERT-002": {
    riskDrivers: [
      "Structural seat-frame component affected",
      "Geometry change may affect load paths and stress margins",
      "Stress and test evidence are missing",
      "Human review is required before certification closure",
    ],
    evidenceRule:
      "Seat frame structural changes require stress analysis, installation drawing, and test evidence.",
    availableEvidence: ["Installation Drawing"],
    routingReason:
      "Because structural evidence is incomplete, UiPath should route the case to evidence collection before approval.",
  },
  "CERT-003": {
    riskDrivers: [
      "Avionics bay system affected",
      "Controller replacement changes electrical interface behavior",
      "Software/control logic evidence is missing",
      "System safety assessment and DER review are required",
    ],
    evidenceRule:
      "Avionics controller changes require system safety assessment, software verification evidence, electrical interface design evidence, and DER review record.",
    availableEvidence: ["Electrical Interface Design Diagram"],
    routingReason:
      "Because the change affects avionics control behavior and critical safety evidence is missing, UiPath should route the case to AI evidence review and DER review.",
  },
};

function formatLabel(value) {
  return value?.replaceAll("_", " ") || "unknown";
}

function DecisionBasisPanel({ selectedCase }) {
  if (!selectedCase) {
    return null;
  }

  const rule = decisionRules[selectedCase.id] || {
    riskDrivers: [
      `${selectedCase.area} is affected`,
      `${selectedCase.component} was changed`,
      `Risk level is ${selectedCase.risk}`,
      "Evidence completeness was checked against the case evidence rule",
    ],
    evidenceRule:
      "Required evidence is selected from the affected aircraft area, component type, and design change category.",
    availableEvidence: [],
    routingReason:
      "UiPath routes the case based on risk level, missing evidence, and whether human review is required.",
  };

  const missingEvidence = selectedCase.missingDocuments || [];
  const hasMissingEvidence = missingEvidence.length > 0;

  return (
    <section className="decision-basis-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Decision Basis</p>
          <h3>Why this case is classified as {formatLabel(selectedCase.risk)} risk</h3>
        </div>

        <span className={`risk-pill ${selectedCase.risk}`}>
          {formatLabel(selectedCase.risk)} Risk
        </span>
      </div>

      <div className="decision-grid">
        <div className="decision-card">
          <div className="decision-card-title">
            <AlertTriangle size={18} />
            <h4>Risk drivers</h4>
          </div>

          <ul>
            {rule.riskDrivers.map((driver) => (
              <li key={driver}>{driver}</li>
            ))}
          </ul>
        </div>

        <div className="decision-card">
          <div className="decision-card-title">
            <FileSearch size={18} />
            <h4>Required evidence rule</h4>
          </div>

          <p>{rule.evidenceRule}</p>
        </div>

        <div className="decision-card">
          <div className="decision-card-title">
            <CheckCircle2 size={18} />
            <h4>Evidence completeness</h4>
          </div>

          <div className="evidence-comparison">
            <div>
              <strong>Available</strong>
              {rule.availableEvidence.length > 0 ? (
                <ul>
                  {rule.availableEvidence.map((evidence) => (
                    <li key={evidence}>{evidence}</li>
                  ))}
                </ul>
              ) : (
                <p>No evidence recorded yet.</p>
              )}
            </div>

            <div>
              <strong>{hasMissingEvidence ? "Missing" : "Missing"}</strong>
              {hasMissingEvidence ? (
                <ul>
                  {missingEvidence.map((evidence) => (
                    <li key={evidence}>{evidence}</li>
                  ))}
                </ul>
              ) : (
                <p>No missing evidence detected.</p>
              )}
            </div>
          </div>
        </div>

        <div className="decision-card">
          <div className="decision-card-title">
            <Route size={18} />
            <h4>UiPath routing basis</h4>
          </div>

          <p>{rule.routingReason}</p>

          <div className="routing-tags">
            <span>Stage: {selectedCase.stage}</span>
            <span>Action: {formatLabel(selectedCase.action)}</span>
            <span>Role: {selectedCase.assignedRole}</span>
          </div>
        </div>
      </div>
    </section>
  );
}

export default DecisionBasisPanel;
