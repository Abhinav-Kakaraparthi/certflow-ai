import { Bot, ClipboardCheck, FileSearch, Gauge, UserCheck } from "lucide-react";

const agents = [
  {
    name: "Certification Basis Agent",
    icon: FileSearch,
    text: "Maps design changes to affected certification areas.",
  },
  {
    name: "Evidence Gap Agent",
    icon: ClipboardCheck,
    text: "Detects missing reports, drawings, reviews, and compliance artifacts.",
  },
  {
    name: "Risk Classification Agent",
    icon: Gauge,
    text: "Classifies case risk and recommends UiPath case actions.",
  },
  {
    name: "Human Review Gate",
    icon: UserCheck,
    text: "Keeps certification engineers and DER reviewers in control.",
  },
];

function AgentMap() {
  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Agent system</p>
          <h3>Orchestration map</h3>
        </div>
        <Bot size={22} />
      </div>

      <div className="agent-stack">
        {agents.map((agent) => {
          const Icon = agent.icon;

          return (
            <div className="agent-card" key={agent.name}>
              <div className="agent-icon">
                <Icon size={18} />
              </div>
              <div>
                <strong>{agent.name}</strong>
                <p>{agent.text}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default AgentMap;
