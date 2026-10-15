# StockPulse Troubleshooting Guide

This guide covers common operational and deployment issues encountered during local development, containerization, and Kubernetes cluster rollout.

---

## 1. Database Connectivity Issues
**Symptom**: `OperationalError: connection to server at '127.0.0.1', port 5432 failed`
- **Cause**: PostgreSQL is not yet ready when the backend starts.
- **Resolution**:
  - In Docker Compose, ensure `depends_on` uses `condition: service_healthy` with `pg_isready`.
  - In local development, start PostgreSQL and run `alembic upgrade head`.

---

## 2. Port Conflicts (Port 5432, 8000, 3000 in use)
**Symptom**: `Bind for 0.0.0.0:5432 failed: port is already allocated`
- **Resolution**:
  ```bash
  # Check which process is holding port 5432
  lsof -i :5432
  # Terminate conflicting process or change port in docker-compose.yml
  ```

---

## 3. Kubernetes Pods in `CrashLoopBackOff`
**Symptom**: Pod fails liveness or readiness probes.
- **Resolution**:
  ```bash
  kubectl logs -n stockpulse deployment/stockpulse-backend
  kubectl describe pod <pod-name> -n stockpulse
  ```
  Ensure the database service `stockpulse-postgres` is reachable within the namespace before the backend probe times out.

---

## 4. Trivy Scan Findings
**Symptom**: Trivy flags CVEs on base images.
- **Resolution**:
  - Use slim/alpine base images (`python:3.12-slim`, `node:22-alpine`, `nginx:alpine`).
  - Pass `--ignore-unfixed` to filter out vulnerabilities without an available upstream patch.
