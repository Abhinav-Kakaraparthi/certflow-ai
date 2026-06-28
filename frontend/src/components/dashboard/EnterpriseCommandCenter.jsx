function EnterpriseCommandCenter({ enterpriseSummary, caseSnapshot }) {
  if (!enterpriseSummary || !caseSnapshot) {
    return null;
  }

  const owner = caseSnapshot.owner;

  return (
    <section className="enterprise-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Enterprise certification command center</p>
          <h3>Role-based oversight, evidence ownership, and auditability</h3>
        </div>
        <span className="risk-pill high">
          {enterpriseSummary.blocked_evidence} blocked evidence item
        </span>
      </div>

      <div className="enterprise-kpi-grid">
        <div>
          <span>Active cases</span>
          <strong>{enterpriseSummary.active_cases}</strong>
        </div>
        <div>
          <span>Total evidence records</span>
          <strong>{enterpriseSummary.total_evidence_records}</strong>
        </div>
        <div>
          <span>Missing evidence</span>
          <strong>{enterpriseSummary.missing_evidence}</strong>
        </div>
        <div>
          <span>Audit events</span>
          <strong>{enterpriseSummary.audit_events}</strong>
        </div>
      </div>

      <div className="enterprise-grid">
        <div className="enterprise-card">
          <p className="eyebrow">Case owner</p>
          <h4>{owner?.name || "Unassigned"}</h4>
          <p>{owner?.role}</p>
          <span>{owner?.team}</span>
        </div>

        <div className="enterprise-card">
          <p className="eyebrow">Team workload</p>
          {Object.entries(enterpriseSummary.team_workload || {}).map(([team, count]) => (
            <div className="workload-row" key={team}>
              <span>{team}</span>
              <strong>{count}</strong>
            </div>
          ))}
        </div>

        <div className="enterprise-card">
          <p className="eyebrow">Role access model</p>
          {Object.entries(enterpriseSummary.role_counts || {}).map(([role, count]) => (
            <div className="workload-row" key={role}>
              <span>{role}</span>
              <strong>{count}</strong>
            </div>
          ))}
        </div>
      </div>

      <div className="enterprise-grid wide">
        <div className="enterprise-card">
          <p className="eyebrow">Evidence ownership</p>
          <div className="evidence-table">
            {caseSnapshot.evidence_records.map((record) => (
              <div className="evidence-row" key={record.evidence_id}>
                <div>
                  <strong>{record.evidence_type}</strong>
                  <span>{record.file_name}</span>
                </div>
                <span className={`evidence-status ${record.status}`}>
                  {record.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="enterprise-card">
          <p className="eyebrow">Audit trail</p>
          <div className="audit-timeline">
            {caseSnapshot.audit_events.map((event) => (
              <div className="audit-event" key={event.event_id}>
                <strong>{event.actor_role}</strong>
                <span>{event.action}</span>
                <p>{event.summary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default EnterpriseCommandCenter;
