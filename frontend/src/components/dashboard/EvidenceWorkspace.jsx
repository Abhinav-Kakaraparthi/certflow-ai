import { useMemo, useState } from "react";
import { FilePenLine, GitBranch, PencilLine, Plus, Save } from "lucide-react";

function statusLabel(value) {
  return value?.replaceAll("_", " ") || "unknown";
}

function EvidenceWorkspace({
  documents = [],
  selectedDocument,
  onSelectDocument,
  onSaveSection,
  onCreateDocument,
}) {
  const [editingSectionId, setEditingSectionId] = useState(null);
  const [draftContent, setDraftContent] = useState("");
  const [newDocOpen, setNewDocOpen] = useState(false);
  const [newDoc, setNewDoc] = useState({
    title: "",
    artifact_type: "System Safety Assessment",
    required_review_role: "DER Reviewer",
    content_summary: "",
  });

  const completionSummary = useMemo(() => {
    const total = documents.length;
    const blocked = documents.filter((doc) => doc.status === "blocked").length;
    const needsAi = documents.filter((doc) =>
      ["needs_revision", "reviewed_with_concerns"].includes(doc.ai_review_status)
    ).length;

    return { total, blocked, needsAi };
  }, [documents]);

  function startEditing(section) {
    setEditingSectionId(section.section_id);
    setDraftContent(section.content);
  }

  async function saveSection(section) {
    await onSaveSection(selectedDocument.document_id, {
      section_id: section.section_id,
      editor_id: selectedDocument.current_editor_id || selectedDocument.owner_id,
      content: draftContent,
      status: "in_progress",
      edit_summary: `Updated ${section.title}`,
    });

    setEditingSectionId(null);
    setDraftContent("");
  }

  async function createDocument() {
    if (!newDoc.title.trim()) return;

    await onCreateDocument({
      case_id: selectedDocument?.case_id || "CERT-003",
      title: newDoc.title,
      artifact_type: newDoc.artifact_type,
      format: "structured_document",
      owner_id: "USR-004",
      created_by: "USR-003",
      required_review_role: newDoc.required_review_role,
      content_summary: newDoc.content_summary || "New certification artifact created inside CertFlow AI.",
    });

    setNewDoc({
      title: "",
      artifact_type: "System Safety Assessment",
      required_review_role: "DER Reviewer",
      content_summary: "",
    });
    setNewDocOpen(false);
  }

  return (
    <section className="evidence-workspace">
      <div className="workspace-hero">
        <div>
          <p className="eyebrow">Evidence Workspace</p>
          <h3>In-app certification document creation and review</h3>
          <p>
            Engineers, suppliers, team leads, and DER reviewers create and edit
            certification artifacts directly inside CertFlow AI. Every section,
            version, AI review status, and ownership change can be routed through
            UiPath.
          </p>
        </div>

        <button
          className="primary-button"
          type="button"
          onClick={() => setNewDocOpen((value) => !value)}
        >
          <Plus size={18} />
          New Artifact
        </button>
      </div>

      <div className="evidence-kpis">
        <div>
          <span>{completionSummary.total}</span>
          <p>Workspace artifacts</p>
        </div>
        <div>
          <span>{completionSummary.needsAi}</span>
          <p>Need AI review</p>
        </div>
        <div>
          <span>{completionSummary.blocked}</span>
          <p>Blocked artifacts</p>
        </div>
      </div>

      {newDocOpen && (
        <div className="new-document-card">
          <div>
            <label>Artifact title</label>
            <input
              value={newDoc.title}
              onChange={(event) =>
                setNewDoc({ ...newDoc, title: event.target.value })
              }
              placeholder="Example: DER Review Record"
            />
          </div>

          <div>
            <label>Artifact type</label>
            <select
              value={newDoc.artifact_type}
              onChange={(event) =>
                setNewDoc({ ...newDoc, artifact_type: event.target.value })
              }
            >
              <option>System Safety Assessment</option>
              <option>Software Verification Evidence</option>
              <option>Design Diagram</option>
              <option>DER Review Record</option>
              <option>Stress Analysis Report</option>
            </select>
          </div>

          <div>
            <label>Required reviewer</label>
            <select
              value={newDoc.required_review_role}
              onChange={(event) =>
                setNewDoc({ ...newDoc, required_review_role: event.target.value })
              }
            >
              <option>Certification Engineer</option>
              <option>Senior Certification Engineer</option>
              <option>DER Reviewer</option>
              <option>Certification Manager</option>
            </select>
          </div>

          <div className="wide-field">
            <label>Summary</label>
            <textarea
              value={newDoc.content_summary}
              onChange={(event) =>
                setNewDoc({ ...newDoc, content_summary: event.target.value })
              }
              placeholder="What evidence will this artifact capture?"
            />
          </div>

          <button className="primary-button" type="button" onClick={createDocument}>
            <Save size={18} />
            Create in workspace
          </button>
        </div>
      )}

      <div className="evidence-grid">
        <aside className="document-list">
          {documents.map((document) => (
            <button
              key={document.document_id}
              className={`document-card ${
                selectedDocument?.document_id === document.document_id ? "active" : ""
              }`}
              type="button"
              onClick={() => onSelectDocument(document)}
            >
              <div>
                <strong>{document.title}</strong>
                <span>{document.artifact_type}</span>
              </div>
              <div className="document-meta">
                <span>v{document.version}</span>
                <span>{statusLabel(document.status)}</span>
              </div>
            </button>
          ))}
        </aside>

        <article className="document-editor">
          {!selectedDocument ? (
            <div className="empty-document">
              <FilePenLine size={42} />
              <p>Select an artifact to edit.</p>
            </div>
          ) : (
            <>
              <div className="document-editor-header">
                <div>
                  <p className="eyebrow">{selectedDocument.artifact_type}</p>
                  <h3>{selectedDocument.title}</h3>
                  <p>{selectedDocument.content_summary}</p>
                </div>

                <div className="document-status-stack">
                  <span>{statusLabel(selectedDocument.status)}</span>
                  <span>{statusLabel(selectedDocument.ai_review_status)}</span>
                  <span>{selectedDocument.required_review_role}</span>
                </div>
              </div>

              <div className="version-strip">
                <span>
                  <GitBranch size={16} />
                  Version {selectedDocument.version}
                </span>
                <span>Format: {statusLabel(selectedDocument.format)}</span>
                <span>Last edited: {selectedDocument.last_edited_at}</span>
              </div>

              <div className="section-editor-list">
                {selectedDocument.sections.map((section) => (
                  <div className="section-editor-card" key={section.section_id}>
                    <div className="section-editor-header">
                      <div>
                        <h4>{section.title}</h4>
                        <span>{statusLabel(section.status)}</span>
                      </div>

                      {editingSectionId !== section.section_id && (
                        <button
                          className="secondary-button"
                          type="button"
                          onClick={() => startEditing(section)}
                        >
                          <PencilLine size={16} />
                          Edit Section
                        </button>
                      )}
                    </div>

                    {editingSectionId === section.section_id ? (
                      <>
                        <textarea
                          className="section-textarea"
                          value={draftContent}
                          onChange={(event) => setDraftContent(event.target.value)}
                        />

                        <div className="editor-actions">
                          <button
                            className="secondary-button"
                            type="button"
                            onClick={() => setEditingSectionId(null)}
                          >
                            Cancel
                          </button>
                          <button
                            className="primary-button"
                            type="button"
                            onClick={() => saveSection(section)}
                          >
                            <Save size={16} />
                            Save Section
                          </button>
                        </div>
                      </>
                    ) : (
                      <p>{section.content}</p>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}
        </article>
      </div>
    </section>
  );
}

export default EvidenceWorkspace;
