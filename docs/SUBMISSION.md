# StockPulse — Submission & Verification Guide

> **Project**: StockPulse — Cloud-Native Real-Time Warehouse & Inventory Management Platform  
> **Student**: Tanishq Singh  
> **Repository**: [https://github.com/Tanishq217/StockPulse](https://github.com/Tanishq217/StockPulse)  
> **Live CI/CD**: [GitHub Actions Workflow](https://github.com/Tanishq217/StockPulse/actions)  
> **Demo Folder**: [`demo/`](../demo/) *(Video walkthrough link & presentation slide deck)*  
> **Presentation Video**: [Watch on Google Drive](https://drive.google.com/drive/u/0/folders/1T26bSPI4WeARpH5yKefgLMhzfZff7D9r) *(details in [`demo/VIDEO.md`](../demo/VIDEO.md))*  
> **Presentation Deck**: [View Browser PDF](../demo/StockPulse_Presentation.pdf)  \|  [Download PowerPoint (.pptx)](../demo/StockPulse_Presentation.pptx)  
> **Target Grade**: 100 / 100 (Full Rubric Coverage)

---

## 1. Quick Proof Checklist (Grading Rubric Parity)

| Rubric Module | Requirement | StockPulse Artifact / Evidence | Status |
|---|---|---|:---:|
| **M1: Application & Database** | 3-tier REST API + DB + UI + Seeds | FastAPI 3.12, React 18, PostgreSQL 16, OpenAPI docs | ✅ Complete |
| **M2: Testing & Code Quality** | Automated unit & integration tests | 11 pytest test cases passing, Pydantic validation | ✅ Complete |
| **M3: Git & Repository Hygiene** | Meaningful git history & docs | Comprehensive commits, professional branching, clean tree | ✅ Complete |
| **M4: Docker & Multi-Container** | Multi-stage Dockerfiles + Compose | Non-root containers, healthchecks, bridge network | ✅ Complete |
| **M5: CI/CD Pipeline** | Automated GitHub Actions workflow | 5 green jobs (Test, Build, Trivy scan, GHCR, Kind deploy) | ✅ Complete |
| **M6: DevSecOps & Scanning** | Security vulnerability scan | Trivy automated scan on both backend & frontend | ✅ Complete |
| **M7: Infrastructure as Code** | Terraform AWS EKS & VPC | Modular HCL, VPC, Subnets, IGW, EKS 1.31 in `ap-southeast-2` | ✅ Verified & Torn Down |
| **M8: Kubernetes Orchestration** | Helm chart, manifests, self-healing | Helm chart with backend, frontend, postgres, ingress, HPA | ✅ Complete |
| **M9: Observability & Metrics** | Prometheus metrics & Grafana | `/metrics` endpoint with Prometheus FastAPI Instrumentator | ✅ Complete |
| **M10: Troubleshooting & Resilience** | Chaos scenarios & failure runbook | Broken image & broken service test manifests with runbook | ✅ Complete |

---

## 2. Evidence Screenshots Catalog

All high-resolution verification screenshots are stored in [`docs/screenshots/`](./screenshots/):

| Screenshot File | Description | Purpose / Rubric Proof |
|---|---|---|
| `github-actions-cicd.png` | GitHub Actions CI/CD Pipeline | **Mandatory Proof**: 5 green jobs executing on push to `main` |
| `docker-compose-ps.png` | Docker Compose process health | **Mandatory Proof**: `stockpulse-backend`, `frontend`, `postgres` all healthy |
| `docker-compose-up.png` | Docker Compose manual `up` run | Multi-container stack starting with dependency ordering |
| `k8s-deployment-local.png` | Local Kubernetes deployment on Kind | **Mandatory Proof**: Pods, services, and deployments in `stockpulse` |
| `codebase-structure.png` | Codebase & Repository Structure | **Mandatory Proof**: Clean modular architecture and source tree |
| `frontend-dashboard.png` | React 18 Web UI Dashboard | Live inventory tracking, low-stock alerts, restock actions |
| `m1-mobile-view.png` | Mobile Responsive Dashboard (375px) | Handheld warehouse scanner & mobile viewport compatibility |
| `m1-psql-tables.png` | PostgreSQL Relational Schema | `inventory_items` and `alembic_version` schema verified |
| `m2-pytest.png` | Automated Unit & Integration Tests | 11 pytest test cases passing in 0.08s |
| `m3-commits.png` | Conventional Git History | Clean commit log with semantic commit conventions |
| `m4-nonroot.png` | Container Security / Non-Root UIDs | UIDs 10001 (backend) and 101 (frontend) verified |
| `m5-ghcr-packages.png` | GitHub Container Registry (GHCR) | Published Docker container packages on GitHub |
| `m6-trivy-scan.png` | DevSecOps Trivy Security Report | Container vulnerability scan report passing with zero blockers |
| `m7-init.png` | Terraform IaC Initialization | Terraform successfully initialized with AWS provider |
| `m8-helm-lint.png` | Helm Chart Linting & Validation | Helm chart lint passing with 0 errors |
| `m9-metrics-curl.png` | Prometheus Metrics Terminal Output | Raw `/metrics` telemetry scraping showing HTTP RPS and latency |
| `m9-troubleshooting.png` | Chaos Engineering Diagnostic Lab | Kubernetes `ImagePullBackOff` triage via `kubectl describe` |
| `api-docs-swagger.png` | Interactive OpenAPI / Swagger UI | `/docs` showing all 7 endpoints with schemas |
| `api-health.png` | Health & Liveness Probes | `GET /health` returning database and application status |
| `api-metrics.png` | Prometheus Metrics Endpoint | `GET /metrics` exporting latency, request count, and status codes |
| `api-get-inventory.png` | REST API Inventory Query | `GET /api/inventory` returning warehouse items JSON array |
| `api-post-inventory.png` | REST API Restock Transaction | `POST /api/inventory` creating a new item with validation |
| `aws-vpc-console.png` | AWS VPC Console in Sydney | Terraform-provisioned VPC, public/private subnets, routes |
| `aws-eks-console.png` | AWS EKS Console (`ACTIVE`) | EKS Cluster `stockpulse-eks-cluster` in `ap-southeast-2` |
| `aws-eks-cluster-details.png`| AWS EKS Cluster Details | EKS Version, Networking, and Node Group configuration |

---

## 3. How to Run & Verify Locally

### Option A: Docker Compose (Fastest — 30 Seconds)
```bash
# Clone and enter the repository
git clone https://github.com/Tanishq217/StockPulse.git
cd StockPulse

# Spin up Database, Backend, and Frontend
docker compose up -d --build

# Verify healthy status
docker compose ps

# Access endpoints:
# - Web Dashboard:  http://localhost:3000
# - Swagger Docs:    http://localhost:8000/docs
# - Health Probe:    http://localhost:8000/health
# - Metrics:         http://localhost:8000/metrics
```

### Option B: Local Kubernetes with Helm (Kind)
```bash
# Create local Kind cluster
kind create cluster --name stockpulse-local

# Install StockPulse using Helm
helm install stockpulse ./helm/stockpulse -n stockpulse --create-namespace

# Inspect pods, services, and deployments
kubectl get pods,svc,deploy -n stockpulse

# Port-forward frontend
kubectl port-forward svc/stockpulse-frontend 3000:80 -n stockpulse
```

### Option C: Run Unit & Integration Tests
```bash
cd backend
source .venv/bin/activate
pytest -v
```

---

## 4. Key Engineering Decisions & Trade-Offs

1. **FastAPI vs. Django / Flask**:
   - *Decision*: FastAPI (Python 3.12) with asynchronous ASGI.
   - *Rationale*: Native `async/await` enables high-throughput concurrent warehouse transactions. Pydantic v2 ensures strict schema validation and auto-generates live interactive OpenAPI documentation with zero boilerplate.
2. **PostgreSQL vs. MongoDB**:
   - *Decision*: PostgreSQL 16 relational database with SQLAlchemy 2.
   - *Rationale*: Warehouse inventory requires strict ACID transactions. Decrementing stock levels under concurrent orders cannot permit race conditions or phantom updates. Relational foreign key constraints preserve catalog integrity.
3. **Kubernetes & Helm vs. AWS ECS / Docker Swarm**:
   - *Decision*: Kubernetes with Helm package management.
   - *Rationale*: Kubernetes provides vendor-neutral declarative orchestration, self-healing liveness/readiness probes, and horizontal pod autoscaling (HPA). Helm packages the entire application topology into reusable version-controlled charts.
4. **GitHub Actions vs. Jenkins**:
   - *Decision*: GitHub Actions native cloud runners.
   - *Rationale*: Zero-maintenance serverless CI/CD eliminates fragile self-hosted controller servers, runs security scans directly on pull requests, and pushes container images to GitHub Packages (GHCR).
5. **Terraform vs. AWS CloudFormation**:
   - *Decision*: Terraform with modular HashiCorp Configuration Language (HCL).
   - *Rationale*: Multi-cloud compatibility, clear execution plans (`terraform plan`), and clean resource destruction (`terraform destroy`) preventing unwanted cloud billing charges.

---

## 5. Troubleshooting Demonstrations

StockPulse includes pre-built failure manifests to test cluster resilience:
- `troubleshooting/broken-image.yaml`: Triggers `ImagePullBackOff` for diagnosing invalid image registries.
- `troubleshooting/broken-service.yaml`: Demonstrates label selector mismatches (`Selector: app=wrong-label`) and endpoint troubleshooting.
- `scripts/load-test.sh`: Generates concurrent HTTP load to test HPA autoscaling.
