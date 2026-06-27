function CaseDetailPanel({ selectedCase }) {
  if (!selectedCase) {
    return null;
  }

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
