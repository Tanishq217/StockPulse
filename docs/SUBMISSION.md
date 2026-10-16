# StockPulse — Submission & Verification Guide

> **Project**: StockPulse — Cloud-Native Real-Time Warehouse & Inventory Management Platform  
> **Student**: Tanishq Singh  
> **Repository**: [https://github.com/Tanishq217/StockPulse](https://github.com/Tanishq217/StockPulse)  
> **Live CI/CD**: [GitHub Actions Workflow](https://github.com/Tanishq217/StockPulse/actions)  
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
| `github-actions-cicd.png` | GitHub Actions CI/CD Pipeline | **Mandatory**: 5 green jobs executing on push to `main` |
| `docker-compose-up.png` | Docker Compose manual `up` run | **Mandatory**: Multi-container stack starting with dependencies |
| `docker-compose-ps.png` | Docker Compose process health | Container status: `stockpulse-backend`, `frontend`, `db` all healthy |
| `k8s-deployment-local.png` | Local Kubernetes deployment on Kind | **Mandatory**: Pods, services, and deployments in `stockpulse` namespace |
| `codebase-structure.png` | Codebase & Repository Structure | **Mandatory**: Clean modular architecture and source tree |
| `frontend-dashboard.png` | React 18 Web UI Dashboard | Live inventory tracking, low-stock alerts, restock actions |
| `api-docs-swagger.png` | Interactive OpenAPI / Swagger UI | `/docs` showing all 7 endpoints with schemas |
| `api-health.png` | Health & Liveness Probes | `GET /health` returning `{"status": "healthy", "database": "connected"}` |
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
