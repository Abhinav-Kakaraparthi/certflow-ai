import { AlertTriangle, CheckCircle2, GitBranch } from "lucide-react";

function HeroSection({ approvedCount, evidenceGapCount }) {
  return (
    <section className="hero-grid">
      <div className="hero-card">
        <div className="hero-copy">
          <p className="eyebrow">Track 1 - UiPath Maestro Case</p>
          <h3>From design change to certification decision</h3>
          <p>
            CertFlow AI coordinates agents, evidence checks, human reviewers,
            and UiPath case actions so certification work remains traceable,
            governed, and reviewable.
          </p>
        </div>

        <div className="flow-strip">
          <span>Design Change</span>
          <GitBranch size={16} />
          <span>AI Review</span>
          <GitBranch size={16} />
          <span>Human Gate</span>
          <GitBranch size={16} />
          <span>Case Closure</span>
        </div>
      </div>

      <div className="metric-card approved">
        <CheckCircle2 size={26} />
        <p>Auto-approved</p>
        <strong>{approvedCount}</strong>
      </div>

      <div className="metric-card warning">
        <AlertTriangle size={26} />
        <p>Evidence gaps</p>
        <strong>{evidenceGapCount}</strong>
      </div>
    </section>
  );
}

export default HeroSection;
