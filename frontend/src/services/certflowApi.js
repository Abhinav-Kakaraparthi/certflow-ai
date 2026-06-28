const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "https://certflow-ai-api.onrender.com/api";
  
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

export function getEnterpriseSummary() {
  return request("/enterprise/summary");
}

export function getEnterpriseCaseSnapshot(caseId) {
  return request(`/enterprise/cases/${caseId}/snapshot`);
}

export function getEnterpriseUsers() {
  return request("/enterprise/users");
}

export function getEvidenceRecords() {
  return request("/enterprise/evidence");
}

export function getAuditEvents() {
  return request("/enterprise/audit-events");
}

export async function getDocumentsForCase(caseId) {
  const response = await fetch(`${API_BASE_URL}/documents/case/${caseId}`);

  if (!response.ok) {
    throw new Error(`Unable to load documents for case ${caseId}`);
  }

  return response.json();
}

export async function getWorkspaceDocument(documentId) {
  const response = await fetch(`${API_BASE_URL}/documents/${documentId}`);

  if (!response.ok) {
    throw new Error(`Unable to load document ${documentId}`);
  }

  return response.json();
}

export async function updateDocumentSection(documentId, payload) {
  const response = await fetch(`${API_BASE_URL}/documents/${documentId}/sections`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Unable to update document ${documentId}`);
  }

  return response.json();
}

export async function createWorkspaceDocument(payload) {
  const response = await fetch(`${API_BASE_URL}/documents`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Unable to create workspace document");
  }

  return response.json();
}


