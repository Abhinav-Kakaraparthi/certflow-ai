import os

import uvicorn

port = int(os.environ.get("PORT", "8001"))

print(f"Starting CertFlow AI API on 0.0.0.0:{port}")

uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=port,
    log_level="info",
)
