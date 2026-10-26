# StockPulse — Presentation Video (MP4)

> **Submission Requirement**: Presentation video (MP4) — MANDATORY  
> **Student**: Tanishq Singh  
> **Project**: StockPulse — Cloud-Native Warehouse & Inventory Management Platform  
> **Video Duration**: ~2 Minutes (Full Project Walkthrough)  

---

## 🎥 Video Access Link

The high-definition presentation video is hosted on Google Drive:

👉 **[Watch Presentation Video on Google Drive](https://drive.google.com/drive/u/0/folders/1T26bSPI4WeARpH5yKefgLMhzfZff7D9r)**

**Direct Folder URL**: `https://drive.google.com/drive/u/0/folders/1T26bSPI4WeARpH5yKefgLMhzfZff7D9r`

---

## 📋 What the Video Covers

1. **[0:00 – 0:25] Application Overview & What Was Built**:
   - Live React 18 dashboard (`http://localhost:3000`)
   - Inventory tracking, automated low-stock threshold alerts, and real-time stockout prevention
   - 3-tier architecture: Python 3.12 FastAPI + React 18 + PostgreSQL 16
2. **[0:25 – 0:50] Local Containerization & Automated Testing**:
   - `docker compose ps` showing running services with healthchecks
   - Non-root least-privilege security (UID 10001 & UID 101)
   - Pytest test suite: 11 unit & integration tests passing in 0.08s
3. **[0:50 – 1:20] GitHub Actions CI/CD & DevSecOps**:
   - 5 green pipeline stages (Test, Build, Security Scan, Package Push, Deploy)
   - Aqua Security Trivy container CVE vulnerability scan passing
   - GitHub Container Registry (GHCR) integration
4. **[1:20 – 1:45] AWS Cloud Infrastructure & Free Credits Verification**:
   - Terraform Infrastructure as Code in AWS Sydney (`ap-southeast-2`)
   - Managed AWS EKS cluster (`stockpulse-eks-cluster`) in `Active` status
   - Verification of AWS $100 student promotional credits utilization & clean teardown
5. **[1:45 – 2:05] Kubernetes Orchestration & Wrap-Up**:
   - Production Helm chart deployment with self-healing probes
   - Prometheus metrics telemetry at `/metrics`
   - 100% completion of all 10 DevOps Capstone grading modules

---

## 📊 Accompanying Presentation Slides

The presentation slides are located right here in the `demo/` folder:
- **Browser-Viewable PDF**: [`StockPulse_Presentation.pdf`](./StockPulse_Presentation.pdf)
- **PowerPoint Deck**: [`StockPulse_Presentation.pptx`](./StockPulse_Presentation.pptx)
