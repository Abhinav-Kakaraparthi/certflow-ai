const API_BASE_URL =
  import.meta.env.VITE_CERTFLOW_API_URL || "http://127.0.0.1:8001/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getCertificationCases() {
  return request("/cases");
}

export function runCertificationCase(caseId) {
  return request(`/uipath/cases/${caseId}/start`, {
    method: "POST",
  });
}

export function runWorkflowCase(caseId) {
  return request(`/workflow/cases/${caseId}/run`, {
    method: "POST",
  });
}

export function submitHumanReview(caseId, reviewPayload) {
  return request(`/uipath/cases/${caseId}/human-review`, {
    method: "POST",
    body: JSON.stringify(reviewPayload),
  });
}
