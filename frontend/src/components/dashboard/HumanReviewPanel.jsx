import { useState } from "react";
import { CheckCircle2, Send, ShieldAlert, UserCheck } from "lucide-react";
import { submitHumanReview } from "../../services/certflowApi";

function HumanReviewPanel({ selectedCase }) {
  const [reviewerName, setReviewerName] = useState("Alex Morgan");
  const [reviewerRole, setReviewerRole] = useState("Senior Certification Engineer");
  const [decision, setDecision] = useState("request_more_evidence");
  const [comments, setComments] = useState(
    "System safety assessment and software verification evidence must be completed before DER review."
  );
  const [reviewResult, setReviewResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  if (!selectedCase) {
    return null;
  }

  const reviewRequired = selectedCase.action !== "auto_approve_case";

  async function handleSubmitReview(event) {
    event.preventDefault();

    try {
      setSubmitting(true);

      const result = await submitHumanReview(selectedCase.id, {
        reviewer_name: reviewerName,
        reviewer_role: reviewerRole,
        decision,
        comments,
      });

      setReviewResult(result);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="human-review-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Human-in-the-loop control</p>
          <h3>Certification engineer review gate</h3>
        </div>
        {reviewRequired ? <ShieldAlert size={22} /> : <CheckCircle2 size={22} />}
      </div>

      {!reviewRequired ? (
        <div className="review-approved-state">
          <CheckCircle2 size={24} />
          <div>
            <strong>No human escalation required</strong>
            <p>
              {selectedCase.id} is low risk with complete evidence and can proceed
              through the standard approval workflow.
            </p>
          </div>
        </div>
      ) : (
        <form className="review-form" onSubmit={handleSubmitReview}>
          <div className="review-grid">
            <label>
              Reviewer name
              <input
                value={reviewerName}
                onChange={(event) => setReviewerName(event.target.value)}
              />
            </label>

            <label>
              Reviewer role
              <input
                value={reviewerRole}
                onChange={(event) => setReviewerRole(event.target.value)}
              />
            </label>

            <label>
              Decision
              <select
                value={decision}
                onChange={(event) => setDecision(event.target.value)}
              >
                <option value="approve">Approve</option>
                <option value="reject">Reject</option>
                <option value="request_more_evidence">Request More Evidence</option>
              </select>
            </label>
          </div>

          <label>
            Certification review comments
            <textarea
              value={comments}
              onChange={(event) => setComments(event.target.value)}
              rows="4"
            />
          </label>

          <button className="review-button" type="submit">
            <Send size={17} />
            {submitting ? "Submitting Review..." : "Submit Human Review"}
          </button>
        </form>
      )}

      {reviewResult && (
        <div className="audit-result">
          <UserCheck size={22} />
          <div>
            <strong>Audit trail recorded</strong>
            <p>{reviewResult.audit_message}</p>
            <span>Final case status: {reviewResult.final_case_status}</span>
          </div>
        </div>
      )}
    </section>
  );
}

export default HumanReviewPanel;
