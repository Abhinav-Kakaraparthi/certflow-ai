import { Plane, ShieldCheck } from "lucide-react";

const navItems = [
  { id: "command", label: "Command Center" },
  { id: "cases", label: "Certification Cases" },
  { id: "agents", label: "Agent Orchestration" },
  { id: "human_review", label: "Human Review" },
  { id: "audit", label: "Audit Trail" },
];

function Sidebar({ activeView = "command", onNavigate = () => {} }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <Plane size={34} />
        </div>
        <div>
          <p>UiPath AgentHack</p>
          <h1>CertFlow AI</h1>
        </div>
      </div>

      <nav className="nav-list">
        {navItems.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`nav-item ${activeView === item.id ? "active" : ""}`}
            onClick={() => onNavigate(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="trust-card">
        <ShieldCheck size={32} />
        <p>
          Governed aerospace certification workflow with role-based oversight,
          evidence ownership, and human-in-the-loop control.
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
