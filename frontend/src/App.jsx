import { useEffect, useState } from "react";
import { Activity } from "lucide-react";
import {
  getCertificationCases,
  getEnterpriseCaseSnapshot,
  getEnterpriseSummary,
  getDocumentsForCase,
  updateDocumentSection,
  createWorkspaceDocument,
  runCertificationCase,
} from "./services/certflowApi";
import Sidebar from "./components/layout/Sidebar";
import HeroSection from "./components/dashboard/HeroSection";
import CaseQueue from "./components/dashboard/CaseQueue";
import AgentMap from "./components/dashboard/AgentMap";
import CaseDetailPanel from "./components/dashboard/CaseDetailPanel";
import HumanReviewPanel from "./components/dashboard/HumanReviewPanel";
import EnterpriseCommandCenter from "./components/dashboard/EnterpriseCommandCenter";
import EvidenceWorkspace from "./components/dashboard/EvidenceWorkspace";
import "./App.css";

function scoreFromRisk(risk) {
  if (risk === "low") return 92;
  if (risk === "medium") return 61;
  return 34;
}

function AuditTrailView({ caseSnapshot }) {
  if (!caseSnapshot) {
    return <section className="detail-panel">No audit trail loaded.</section>;
  }

  return (
    <section className="detail-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Audit Trail</p>
          <h3>{caseSnapshot.case_id} decision history</h3>
        </div>
        <span className="risk-pill high">
          {caseSnapshot.audit_events.length} events
        </span>
      </div>

      <div className="audit-timeline">
        {caseSnapshot.audit_events.map((event) => (
          <div className="audit-event" key={event.event_id}>
            <strong>{event.actor_role}</strong>
            <span>{event.action}</span>
            <p>{event.summary}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function App() {
  const [activeView, setActiveView] = useState("command");
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState(null);
  const [enterpriseSummary, setEnterpriseSummary] = useState(null);
  const [caseSnapshot, setCaseSnapshot] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [error, setError] = useState("");

  async function loadEnterpriseSnapshot(caseId) {
    if (!caseId) return;

    try {
      const snapshot = await getEnterpriseCaseSnapshot(caseId);
      setCaseSnapshot(snapshot);
    } catch {
      setCaseSnapshot(null);
    }
  }

  async function loadDocuments(caseId) {
    if (!caseId) return;

    try {
      const workspaceDocuments = await getDocumentsForCase(caseId);
      setDocuments(workspaceDocuments);
      setSelectedDocument((currentDocument) => {
        return (
          workspaceDocuments.find(
            (document) => document.document_id === currentDocument?.document_id
          ) ||
          workspaceDocuments[0] ||
          null
        );
      });
    } catch {
      setDocuments([]);
      setSelectedDocument(null);
    }
  }

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [rawCases, summary] = await Promise.all([
        getCertificationCases(),
        getEnterpriseSummary(),
      ]);

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

      const defaultCase = enrichedCases.find((item) => item.id === "CERT-003") || enrichedCases[0];

      setEnterpriseSummary(summary);
      setCases(enrichedCases);
      setSelectedCase(defaultCase);
      await loadEnterpriseSnapshot(defaultCase?.id);
      await loadDocuments(defaultCase?.id);
    } catch {
      setError("Unable to connect to CertFlow backend. Confirm FastAPI is running on port 8001 or use the deployed Render API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    if (selectedCase?.id) {
      loadEnterpriseSnapshot(selectedCase.id);
      loadDocuments(selectedCase.id);
    }
  }, [selectedCase?.id]);

  async function handleSaveDocumentSection(documentId, payload) {
    const updatedDocument = await updateDocumentSection(documentId, payload);

    setDocuments((currentDocuments) =>
      currentDocuments.map((document) =>
        document.document_id === updatedDocument.document_id
          ? updatedDocument
          : document
      )
    );

    setSelectedDocument(updatedDocument);
    await loadEnterpriseSnapshot(updatedDocument.case_id);
  }

  async function handleCreateDocument(payload) {
    const createdDocument = await createWorkspaceDocument(payload);

    setDocuments((currentDocuments) => [...currentDocuments, createdDocument]);
    setSelectedDocument(createdDocument);
    await loadEnterpriseSnapshot(createdDocument.case_id);
  }

  const approvedCount = cases.filter((item) => item.action === "auto_approve_case").length;
  const evidenceGapCount = cases.filter((item) => item.missingDocuments?.length > 0).length;

  return (
    <main className="app-shell">
      <Sidebar activeView={activeView} onNavigate={setActiveView} />

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Aerospace Certification Case Management</p>
            <h2>Enterprise AI orchestration for certification leadership teams</h2>
          </div>
          <button className="primary-button" onClick={loadDashboard}>
            <Activity size={18} />
            {loading ? "Running..." : "Run Case Flow"}
          </button>
        </header>

        {error && <div className="error-banner">{error}</div>}

        {activeView === "command" && (
          <>
            <HeroSection
              approvedCount={approvedCount}
              evidenceGapCount={evidenceGapCount}
            />

            <EnterpriseCommandCenter
              enterpriseSummary={enterpriseSummary}
              caseSnapshot={caseSnapshot}
            />
          </>
        )}

        {activeView === "cases" && (
          <section className="case-page-layout">
            <CaseQueue
              cases={cases}
              selectedCase={selectedCase}
              onSelectCase={setSelectedCase}
            />
            <CaseDetailPanel selectedCase={selectedCase} />
          </section>
        )}

        {activeView === "agents" && (
          <>
            <AgentMap />
            <CaseDetailPanel selectedCase={selectedCase} />
          </>
        )}

        {activeView === "evidence" && (
          <EvidenceWorkspace
            documents={documents}
            selectedDocument={selectedDocument}
            onSelectDocument={setSelectedDocument}
            onSaveSection={handleSaveDocumentSection}
            onCreateDocument={handleCreateDocument}
          />
        )}

        {activeView === "human_review" && (
          <HumanReviewPanel selectedCase={selectedCase} />
        )}

        {activeView === "audit" && (
          <AuditTrailView caseSnapshot={caseSnapshot} />
        )}
      </section>
    </main>
  );
}

export default App;



