from app.models.human_review import HumanDecision, HumanReviewRequest, HumanReviewResult


def process_human_review(case_id: str, review: HumanReviewRequest) -> HumanReviewResult:
    if review.decision == HumanDecision.APPROVE:
        final_status = "approved"
        audit_message = (
            f"Case {case_id} was approved by {review.reviewer_role} "
            f"{review.reviewer_name} after human certification review."
        )
    elif review.decision == HumanDecision.REJECT:
        final_status = "rejected"
        audit_message = (
            f"Case {case_id} was rejected by {review.reviewer_role} "
            f"{review.reviewer_name} due to certification concerns."
        )
    else:
        final_status = "needs_more_evidence"
        audit_message = (
            f"Case {case_id} requires more evidence based on review by "
            f"{review.reviewer_role} {review.reviewer_name}."
        )

    return HumanReviewResult(
        case_id=case_id,
        reviewer_name=review.reviewer_name,
        reviewer_role=review.reviewer_role,
        decision=review.decision,
        final_case_status=final_status,
        comments=review.comments,
        audit_message=audit_message,
    )
