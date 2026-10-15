# StockPulse Capstone Presentation Deck Guide

Use this slide-by-slide structure to build your PowerPoint (`StockPulse_Final_Presentation.pptx`) for the capstone evaluation.

---

## Slide 1: Title & Executive Summary
- **Title**: StockPulse — Cloud-Native Warehouse & Inventory Management Platform
- **Subtitle**: End-to-End DevOps Automation, DevSecOps & Container Orchestration
- **Student Name & Course**: DevOps Final Capstone Project
- **Key Takeaway**: A 3-tier microservice travel from developer laptop to a secure, monitored Kubernetes cluster.

---

## Slide 2: The Problem & Solution (Non-Technical Friendly)
- **The Business Need**: Real-time warehouse inventory visibility, stockout prevention, and automated threshold alerts.
- **The DevOps Solution**: Automated testing, containerization, vulnerability scanning, and infrastructure as code to ensure 99.9% uptime and zero-downtime deployments.
- **Why this Architecture**:
  - FastAPI: High performance, native OpenAPI documentation, automatic validation.
  - PostgreSQL: Relational integrity, ACID transactions for financial inventory valuation.
  - React + Nginx: Fast client-side rendering with production-grade reverse proxying.

---

## Slide 3: Architecture & Tech Stack
- **Architecture Diagram**: (Include diagram from README.md)
- **Tech Stack Highlights**:
  - Backend: Python 3.12, FastAPI, SQLAlchemy, Alembic
  - Frontend: React 18, Vite, Nginx Alpine
  - Containerization: Docker, Docker Compose (named volume persistence)
  - Orchestration: Kubernetes, Helm, Kind
  - CI/CD & DevSecOps: GitHub Actions, Trivy Vulnerability Scanner, GHCR
  - Infrastructure as Code: Terraform (AWS VPC & EKS)
  - Observability: Prometheus & Grafana

---

## Slide 4: Required Screenshot 1 — Main Repository & Codebase
- **Screenshot**: Code editor / GitHub repository root showing:
  - `.github/workflows/`
  - `backend/`
  - `frontend/`
  - `helm/` & `ktest/`
  - `terraform/`
  - `monitoring/`
  - `docker-compose.yml`
- **Key Talking Point**: Modular, separation of concerns, infrastructure codified alongside application logic.

---

## Slide 5: Required Screenshot 2 — Docker Compose Execution
- **Screenshot**: Terminal output of `docker compose ps` showing:
  - `stockpulse-postgres` (healthy)
  - `stockpulse-backend` (healthy)
  - `stockpulse-frontend` (running)
- **Key Talking Point**: 1-command startup of the complete 3-tier stack with inter-service networking and volume persistence.

---

## Slide 6: Required Screenshot 3 — Kubernetes Local Deployment
- **Screenshot**: Terminal output of `kubectl get pods -n stockpulse` and `kubectl get svc -n stockpulse`
  - Shows 2 backend replicas + 2 frontend replicas running cleanly
- **Key Talking Point**: High availability with multiple pod replicas, health/readiness probes, and self-healing.

---

## Slide 7: Required Screenshot 4 — GitHub Actions CI/CD Pipeline
- **Screenshot**: GitHub Actions page showing green checkmarks across all 5 stages:
  1. Test (pytest + npm build)
  2. Build Docker Images
  3. Scan Images with Trivy (DevSecOps)
  4. Push to Container Registry
  5. Deploy to Kubernetes
- **Key Talking Point**: Complete DevSecOps quality gates preventing untested or insecure code from ever reaching production.

---

## Slide 8: Observability & Key Metrics
- **Prometheus**: Real-time metrics scraped every 10 seconds via `/metrics`.
- **Grafana**: Visualizing request rates, p95 latency, and HTTP status codes.
- **Cost Efficiency**: Local Kind cluster used for active development, zero AWS runaway costs.

---

## Slide 9: Conclusion & Key Learnings
- Complete automated delivery cycle implemented.
- Robust testing coverage (11 unit and integration tests).
- 100% compliant with the 10-module evaluation rubric.
