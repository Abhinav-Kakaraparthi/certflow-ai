import { Plane, ShieldCheck } from "lucide-react";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">
          <Plane size={22} />
        </div>
        <div>
          <p className="eyebrow">UiPath AgentHack</p>
          <h1>CertFlow AI</h1>
        </div>
      </div>

      <nav className="nav">
        <a className="active">Command Center</a>
        <a>Certification Cases</a>
        <a>Agent Orchestration</a>
        <a>Human Review</a>
        <a>Audit Trail</a>
      </nav>

      <div className="sidebar-card">
        <ShieldCheck size={22} />
        <p>Governed aerospace certification workflow with human-in-the-loop control.</p>
      </div>
    </aside>
  );
}

export default Sidebar;
