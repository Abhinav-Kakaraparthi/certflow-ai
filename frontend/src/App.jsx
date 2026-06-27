import { useEffect, useState } from "react";
import { Activity } from "lucide-react";
import { getCertificationCases, runCertificationCase } from "./services/certflowApi";
import Sidebar from "./components/layout/Sidebar";
import HeroSection from "./components/dashboard/HeroSection";
import CaseQueue from "./components/dashboard/CaseQueue";
import AgentMap from "./components/dashboard/AgentMap";
import CaseDetailPanel from "./components/dashboard/CaseDetailPanel";
import HumanReviewPanel from "./components/dashboard/HumanReviewPanel";
import "./App.css";

function scoreFromRisk(risk) {
  if (risk === "low") return 92;
  if (risk === "medium") return 61;
  return 34;
}

function App() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState(null);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const rawCases = await getCertificationCases();

      const enrichedCases = await Promise.all(
        rawCases.map(async (caseItem) => {
          const result = await runCertificationCase(caseItem.case_id);

          return {
            id: caseItem.case_id,
            title: caseItem.title,
            area: caseItem.aircraft_area,
            component: caseItem.component,
            risk: result.overall_risk,
            status: result.case_status,
            action: result.next_uipath_action,
            score: scoreFromRisk(result.overall_risk),
            stage: result.maestro_stage,
            assignedRole: result.assigned_role,
            summary: result.agent_summary,
            missingDocuments: result.missing_documents,
            findings: result.agent_findings,
            aiReasoning: result.ai_reasoning,
          };
        })
      );

      setCases(enrichedCases);
      setSelectedCase(enrichedCases.find((item) => item.id === "CERT-003") || enrichedCases[0]);
    } catch {
      setError("Unable to connect to CertFlow backend. Confirm FastAPI is running on port 8001 or use the deployed Render API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const approvedCount = cases.filter((item) => item.action === "auto_approve_case").length;
  const evidenceGapCount = cases.filter((item) => item.missingDocuments?.length > 0).length;

  return (
    <main className="app-shell">
      <Sidebar />

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Aerospace Certification Case Management</p>
            <h2>Agentic compliance orchestration for certification engineers</h2>
          </div>
          <button className="primary-button" onClick={loadDashboard}>
            <Activity size={18} />
            {loading ? "Running..." : "Run Case Flow"}
          </button>
        </header>

        {error && <div className="error-banner">{error}</div>}

        <HeroSection
          approvedCount={approvedCount}
          evidenceGapCount={evidenceGapCount}
        />

        <section className="content-grid">
          <CaseQueue
            cases={cases}
            selectedCase={selectedCase}
            onSelectCase={setSelectedCase}
          />
          <AgentMap />
        </section>

        <CaseDetailPanel selectedCase={selectedCase} />
        <HumanReviewPanel selectedCase={selectedCase} />
      </section>
    </main>
  );
}

export default App;
