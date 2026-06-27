function formatStatus(status) {
  const labels = {
    approved: "Auto Approved",
    needs_more_evidence: "Needs Evidence",
    waiting_for_human: "Human Review",
    in_review: "In Review",
    rejected: "Rejected",
    new: "New",
  };

  return labels[status] || status;
}

function riskLabel(risk) {
  if (!risk) return "Unknown";
  return risk.charAt(0).toUpperCase() + risk.slice(1);
}

function CaseQueue({ cases, selectedCase, onSelectCase }) {
  return (
    <div className="panel large">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Live certification cases</p>
          <h3>Case intelligence queue</h3>
        </div>
        <span className="sync-badge">Live FastAPI + UiPath-ready payloads</span>
      </div>

      <div className="case-list">
        {cases.map((item) => (
          <button
            className={`case-row ${selectedCase?.id === item.id ? "selected" : ""}`}
            key={item.id}
            onClick={() => onSelectCase(item)}
          >
            <div className="case-main">
              <span className="case-id">{item.id}</span>
              <div>
                <h4>{item.title}</h4>
                <p>{item.area}</p>
              </div>
            </div>

            <div className={`risk-pill ${item.risk}`}>
              {riskLabel(item.risk)} Risk
            </div>

            <div className="score-block">
              <span>{item.score}%</span>
              <div className="score-track">
                <div style={{ width: `${item.score}%` }} />
              </div>
            </div>

            <div className="case-action">
              <strong>{formatStatus(item.status)}</strong>
              <p>{item.action}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default CaseQueue;
