function CaseDetailPanel({ selectedCase }) {
  if (!selectedCase) {
    return null;
  }

  const ai = selectedCase.aiReasoning;

  return (
    <section className="detail-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Selected case intelligence</p>
          <h3>{selectedCase.id} - {selectedCase.stage}</h3>
        </div>
        <span className={`risk-pill ${selectedCase.risk}`}>
          Assigned to {selectedCase.assignedRole}
        </span>
      </div>

      <p className="case-summary">{selectedCase.summary}</p>

      {ai && (
        <div className="ai-reasoning-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Live AI certification reasoning</p>
              <h3>Gemini reasoning agent</h3>
            </div>
            <span className="risk-pill high">
              {Math.round((ai.confidence_score || 0) * 100)}% confidence
            </span>
          </div>

          <div className="ai-meta-grid">
            <div>
              <span>Model</span>
              <strong>{ai.ai_model}</strong>
            </div>
            <div>
              <span>Recommended escalation</span>
              <strong>{ai.recommended_escalation}</strong>
            </div>
          </div>

          <p className="case-summary">{ai.risk_explanation}</p>

          <div className="finding-grid">
            <div className="finding-card">
              <strong>AI certification concerns</strong>
              <ul>
                {ai.certification_concerns?.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="finding-card">
              <strong>Reviewer questions</strong>
              <ul>
                {ai.missing_evidence_questions?.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="audit-strip">
            <strong>Audit summary</strong>
            <p>{ai.audit_summary}</p>
          </div>
        </div>
      )}

      <div className="finding-grid">
        {selectedCase.findings.map((finding) => (
          <div className="finding-card" key={finding.agent_name}>
            <strong>{finding.agent_name}</strong>
            <p>{finding.summary}</p>
            <ul>
              {finding.findings.slice(0, 3).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}

export default CaseDetailPanel;
