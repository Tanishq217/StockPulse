#!/usr/bin/env python3
"""
Generate StockPulse Executive Master Presentation (.pptx)
Strictly adheres to instructor guidelines:
- High-level, bold, executive template readable by a non-technical person
- Punchy bullet points (no 4-5 line blocks)
- Clear coverage of Tech Stack, What was built, Why built this way, Alternatives considered, and Output
- 4 Mandatory Proof of Concept Screenshots highlighted prominently
- Full alignment with all 10 DevOps Capstone modules
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette (High-Contrast Executive Slate & Gold)
COLOR_BG = RGBColor(11, 15, 25)            # #0B0F19 Dark Space Navy
COLOR_CARD = RGBColor(20, 27, 45)          # #141B2D Deep Card Background
COLOR_BORDER = RGBColor(45, 55, 75)        # #2D374B Card Border
COLOR_CYAN = RGBColor(56, 189, 248)        # #38BDF8 Accent Cyan
COLOR_GREEN = RGBColor(52, 211, 153)       # #34D399 Accent Emerald
COLOR_GOLD = RGBColor(250, 204, 21)        # #FACC15 Accent Gold (Mandatory Badge)
COLOR_WHITE = RGBColor(255, 255, 255)      # Pure White Text
COLOR_MUTED = RGBColor(156, 163, 175)      # Slate Gray Text

def create_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    screenshots_dir = os.path.abspath("docs/screenshots")

    def add_base_slide(header_text, category_badge="DEVOPS CAPSTONE", is_mandatory=False):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

        # Category / Mandatory Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.0), Inches(0.35))
        tf = badge_box.text_frame
        p = tf.paragraphs[0]
        if is_mandatory:
            p.text = f"★ MANDATORY PROOF OF CONCEPT  |  {category_badge.upper()}"
            p.font.color.rgb = COLOR_GOLD
        else:
            p.text = category_badge.upper()
            p.font.color.rgb = COLOR_CYAN
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True

        # Header Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.75))
        tf2 = title_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = header_text
        p2.font.name = "Arial"
        p2.font.size = Pt(26)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_WHITE

        # Footer divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

        # Footer metadata
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.96), Inches(11.733), Inches(0.35))
        tf3 = footer_box.text_frame
        p3 = tf3.paragraphs[0]
        p3.text = "StockPulse • Cloud-Native Warehouse & Inventory Management Platform • Tanishq Singh"
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_MUTED

        return slide

    def add_card(slide, left, top, width, height, title, bullets, accent_color=COLOR_CYAN, title_size=17, bullet_size=13):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), height - Inches(0.36))
        tf = tx_box.text_frame
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(title_size)
        p_title.font.bold = True
        p_title.font.color.rgb = accent_color
        p_title.space_after = Pt(8)

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"•  {b}"
            p.font.name = "Arial"
            p.font.size = Pt(bullet_size)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(6)

    def add_image_safely(slide, img_filename, left, top, width, height):
        img_path = os.path.join(screenshots_dir, img_filename)
        if os.path.exists(img_path):
            border = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left - Inches(0.04), top - Inches(0.04), width + Inches(0.08), height + Inches(0.08))
            border.fill.solid()
            border.fill.fore_color.rgb = COLOR_BORDER
            border.line.fill.background()
            slide.shapes.add_picture(img_path, left, top, width, height)
        else:
            print(f"Warning: {img_filename} not found.")

    # ==========================================
    # SLIDE 1: EXECUTIVE TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG
    bg1.line.fill.background()

    # Outer decorative card
    dec_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    dec_card.fill.solid()
    dec_card.fill.fore_color.rgb = COLOR_CARD
    dec_card.line.color.rgb = COLOR_BORDER
    dec_card.line.width = Pt(2.0)

    t_box = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "DEVOPS FINAL CAPSTONE PROJECT  |  TARGET GRADE: 100 / 100"
    p_badge.font.name = "Arial"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_GOLD
    p_badge.space_after = Pt(14)

    p_main = tf1.add_paragraph()
    p_main.text = "STOCKPULSE"
    p_main.font.name = "Arial"
    p_main.font.size = Pt(54)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_CYAN
    p_main.space_after = Pt(10)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Cloud-Native Real-Time Warehouse & Inventory Management Platform"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(22)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_WHITE
    p_sub.space_after = Pt(24)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Presenter: Tanishq Singh   |   Repository: github.com/Tanishq217/StockPulse"
    p_meta.font.name = "Arial"
    p_meta.font.size = Pt(14)
    p_meta.font.color.rgb = COLOR_GREEN
    p_meta.space_after = Pt(10)

    p_tech = tf1.add_paragraph()
    p_tech.text = "Stack: Python 3.12 • FastAPI • React 18 • PostgreSQL 16 • Docker • Kubernetes • Helm • AWS EKS • Trivy"
    p_tech.font.name = "Arial"
    p_tech.font.size = Pt(13)
    p_tech.font.color.rgb = COLOR_MUTED

    # ==========================================
    # SLIDE 2: WHAT WE BUILT (EXECUTIVE PROBLEM & SOLUTION)
    # ==========================================
    s2 = add_base_slide("What We Built: Real-Time Warehouse Command Center", "01. PROJECT OVERVIEW")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.64), Inches(4.8),
             "The Real-World Problem",
             [
                 "Traditional warehouses track stock on paper or slow legacy spreadsheets.",
                 "Causes costly stockouts, double-allocated orders, and dispatch delays.",
                 "No instant alerts when high-demand goods fall below safety limits."
             ], accent_color=COLOR_GOLD)

    add_card(s2, Inches(4.84), Inches(1.6), Inches(3.64), Inches(4.8),
             "The StockPulse Solution",
             [
                 "Live digital warehouse dashboard tracking stock in real time.",
                 "Automated safety threshold warnings prevent unexpected shortages.",
                 "Strict transaction safety blocks race conditions on concurrent orders.",
                 "Interactive REST API for instant warehouse barcode scanner integration."
             ], accent_color=COLOR_CYAN)

    add_card(s2, Inches(8.88), Inches(1.6), Inches(3.64), Inches(4.8),
             "Cloud-Native Delivery",
             [
                 "100% containerized with Docker multi-stage builds.",
                 "Self-healing Kubernetes cluster automatically restarts crashed services.",
                 "Zero-touch CI/CD pipeline tests, scans, and deploys every commit."
             ], accent_color=COLOR_GREEN)

    # ==========================================
    # SLIDE 3: HOW IT WORKS (3-TIER ARCHITECTURE)
    # ==========================================
    s3 = add_base_slide("How It Works: 3-Tier Microservice Flow", "02. SYSTEM DESIGN")
    add_card(s3, Inches(0.8), Inches(1.6), Inches(3.64), Inches(4.8),
             "Tier 1: Web Interface",
             [
                 "React 18 Single Page Application with Tailwind CSS.",
                 "Served via hardened Nginx Alpine as non-root (UID 101).",
                 "Real-time stock indicators, restock forms, and search.",
                 "Responsive layout optimized for warehouse tablet computers."
             ], accent_color=COLOR_CYAN)

    add_card(s3, Inches(4.84), Inches(1.6), Inches(3.64), Inches(4.8),
             "Tier 2: Business Logic API",
             [
                 "Python 3.12 & FastAPI asynchronous ASGI server.",
                 "Strict Pydantic v2 schemas validate all stock entries.",
                 "Built-in health probes (/health) and Prometheus metrics (/metrics).",
                 "Executes safely as non-root user (UID 10001)."
             ], accent_color=COLOR_GREEN)

    add_card(s3, Inches(8.88), Inches(1.6), Inches(3.64), Inches(4.8),
             "Tier 3: Database & State",
             [
                 "PostgreSQL 16 relational database engine.",
                 "ACID transactions guarantee exact inventory counts.",
                 "Alembic automated migrations handle database schema.",
                 "Persistent Volumes ensure data survives container restarts."
             ], accent_color=COLOR_GOLD)

    # ==========================================
    # SLIDE 4: MANDATORY PROOF 1: REPOSITORY STRUCTURE
    # ==========================================
    s4 = add_base_slide("Proof of Concept 1: Codebase & Repository Structure", "03. REPOSITORY & CODE QUALITY", is_mandatory=True)
    add_card(s4, Inches(0.8), Inches(1.6), Inches(4.5), Inches(4.8),
             "Modular Project Layout",
             [
                 "Clean separation of frontend, backend, and infrastructure code.",
                 "Automated Pytest suite: 11 unit & integration tests passing.",
                 "Infrastructure as Code: Complete Helm chart and Terraform modules.",
                 "Production documentation: Architecture, Runbooks, and Rubric guide."
             ], accent_color=COLOR_CYAN)
    add_image_safely(s4, "codebase-structure.png", Inches(5.6), Inches(1.6), Inches(6.9), Inches(4.8))

    # ==========================================
    # SLIDE 5: TECH STACK AT A GLANCE
    # ==========================================
    s5 = add_base_slide("Technology Stack: Cloud-Native & Production-Grade", "04. TECHNOLOGIES USED")
    add_card(s5, Inches(0.8), Inches(1.6), Inches(2.7), Inches(4.8),
             "Application Tier",
             [
                 "Python 3.12: High-speed async runtime.",
                 "FastAPI: Modern async REST API.",
                 "React 18: Responsive dashboard UI.",
                 "Vite: Lightning-fast frontend build."
             ], accent_color=COLOR_CYAN)

    add_card(s5, Inches(3.75), Inches(1.6), Inches(2.7), Inches(4.8),
             "Data & Storage",
             [
                 "PostgreSQL 16: Relational ACID DB.",
                 "SQLAlchemy 2: Safe async ORM.",
                 "Alembic: Schema migration tracking.",
                 "EBS gp3: Persistent storage."
             ], accent_color=COLOR_GREEN)

    add_card(s5, Inches(6.7), Inches(1.6), Inches(2.7), Inches(4.8),
             "DevOps & Cloud",
             [
                 "Docker: Multi-stage non-root containers.",
                 "Kubernetes: Self-healing orchestration.",
                 "Helm: Chart package management.",
                 "AWS EKS: Cloud managed cluster."
             ], accent_color=COLOR_GOLD)

    add_card(s5, Inches(9.65), Inches(1.6), Inches(2.7), Inches(4.8),
             "Security & Telemetry",
             [
                 "GitHub Actions: 5-stage CI/CD.",
                 "Trivy: Automated CVE scan.",
                 "Prometheus: Latency & RPS metrics.",
                 "Terraform: Modular AWS IaC."
             ], accent_color=COLOR_CYAN)

    # ==========================================
    # SLIDE 6: MANDATORY PROOF 2: DOCKER COMPOSE MANUAL RUN
    # ==========================================
    s6 = add_base_slide("Proof of Concept 2: Local Docker Compose Manual Run", "05. CONTAINER ORCHESTRATION", is_mandatory=True)
    add_card(s6, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "Single-Command Launch",
             [
                 "docker compose up -d builds and runs the entire 3-tier platform.",
                 "Automatic Healthcheck: Backend waits for PostgreSQL readiness.",
                 "Isolated bridge network with internal DNS service discovery.",
                 "Security compliance: Containers run as non-root UIDs 10001 and 101."
             ], accent_color=COLOR_CYAN)
    add_image_safely(s6, "docker-compose-ps.png", Inches(5.4), Inches(1.6), Inches(7.1), Inches(2.3))
    add_image_safely(s6, "m4-nonroot.png", Inches(5.4), Inches(4.1), Inches(7.1), Inches(2.3))

    # ==========================================
    # SLIDE 7: WHY WE BUILT IT THIS WAY
    # ==========================================
    s7 = add_base_slide("Why We Built It This Way: Reliability & Safety First", "06. DESIGN RATIONALE")
    add_card(s7, Inches(0.8), Inches(1.6), Inches(3.64), Inches(4.8),
             "High Availability & Self-Healing",
             [
                 "Kubernetes liveness probes detect deadlocks and restart pods instantly.",
                 "Readiness probes ensure zero traffic is sent to initializing containers.",
                 "Zero downtime rolling updates during application deployments."
             ], accent_color=COLOR_GREEN)

    add_card(s7, Inches(4.84), Inches(1.6), Inches(3.64), Inches(4.8),
             "Zero Inventory Desynchronization",
             [
                 "Warehouse systems cannot afford phantom stock deduction bugs.",
                 "PostgreSQL row locking prevents race conditions under high concurrent orders.",
                 "Strict relational integrity ensures every SKU maps to a real item."
             ], accent_color=COLOR_CYAN)

    add_card(s7, Inches(8.88), Inches(1.6), Inches(3.64), Inches(4.8),
             "Defense in Depth Security",
             [
                 "Containers execute as non-root users to block privilege escalations.",
                 "Aqua Security Trivy automated scans gate every container image release.",
                 "Zero hardcoded secrets; dynamic environment variable injection."
             ], accent_color=COLOR_GOLD)

    # ==========================================
    # SLIDE 8: ALTERNATIVES CONSIDERED (TEACHER REQUIREMENT)
    # ==========================================
    s8 = add_base_slide("Alternatives Considered: Architectural Trade-Offs", "07. ENGINEERING DECISIONS")
    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.25),
             "1. Kubernetes vs. AWS ECS / Docker Swarm",
             [
                 "Chose Kubernetes: Declarative self-healing, HPA autoscaling, open standard.",
                 "Alternative Rejected: AWS ECS locks to Amazon; Swarm lacks autoscaling tooling."
             ], accent_color=COLOR_CYAN)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.25),
             "2. FastAPI vs. Django / Flask",
             [
                 "Chose FastAPI: High-speed async ASGI, Pydantic validation, auto Swagger docs.",
                 "Alternative Rejected: Django is too heavy for microservices; Flask lacks async."
             ], accent_color=COLOR_GREEN)

    add_card(s8, Inches(0.8), Inches(4.15), Inches(5.6), Inches(2.25),
             "3. PostgreSQL vs. MongoDB",
             [
                 "Chose PostgreSQL: Strict ACID transactions ensure stock balances never desync.",
                 "Alternative Rejected: MongoDB eventual consistency risks race-condition phantom sales."
             ], accent_color=COLOR_GOLD)

    add_card(s8, Inches(6.8), Inches(4.15), Inches(5.6), Inches(2.25),
             "4. GitHub Actions vs. Jenkins",
             [
                 "Chose GitHub Actions: Serverless cloud runners, native GHCR, zero server upkeep.",
                 "Alternative Rejected: Jenkins requires maintaining dedicated master/worker VMs."
             ], accent_color=COLOR_CYAN)

    # ==========================================
    # SLIDE 9: MANDATORY PROOF 3: CI/CD PIPELINE AUTOMATION
    # ==========================================
    s9 = add_base_slide("Proof of Concept 3: Automated CI/CD Pipeline", "08. CONTINUOUS INTEGRATION & DELIVERY", is_mandatory=True)
    add_card(s9, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "5 Automated Quality Gates",
             [
                 "Triggered automatically on every push and pull request to main.",
                 "1. Test: Pytest executes 11 unit & integration tests.",
                 "2. Build: Multi-stage Docker build for backend and frontend.",
                 "3. Security: Trivy scans container images for CVE vulnerabilities.",
                 "4. Registry: Publishes tagged images to GitHub Packages (GHCR).",
                 "5. Deploy: Verifies automated rollout on Kubernetes cluster."
             ], accent_color=COLOR_GREEN)
    add_image_safely(s9, "github-actions-cicd.png", Inches(5.4), Inches(1.6), Inches(7.1), Inches(2.3))
    add_image_safely(s9, "m6-trivy-scan.png", Inches(5.4), Inches(4.1), Inches(7.1), Inches(2.3))

    # ==========================================
    # SLIDE 10: MANDATORY PROOF 4: LOCAL KUBERNETES DEPLOYMENT
    # ==========================================
    s10 = add_base_slide("Proof of Concept 4: Local Kubernetes Deployment", "09. KUBERNETES ORCHESTRATION", is_mandatory=True)
    add_card(s10, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "Helm Package & Cluster State",
             [
                 "Packaged via production-ready Helm chart (helm/stockpulse).",
                 "Deployments: 2 backend and 2 frontend pods with load-balancing.",
                 "PostgreSQL: Single StatefulSet with Persistent Volume Claim.",
                 "Active verification: All pods, services, and deployments running healthy."
             ], accent_color=COLOR_CYAN)
    add_image_safely(s10, "k8s-deployment-local.png", Inches(5.4), Inches(1.6), Inches(7.1), Inches(4.8))

    # ==========================================
    # SLIDE 11: CLOUD DEPLOYMENT: AWS EKS & VPC (SYDNEY)
    # ==========================================
    s11 = add_base_slide("Production Cloud Deployment: AWS EKS (Sydney)", "10. INFRASTRUCTURE AS CODE")
    add_card(s11, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "Terraform AWS Infrastructure",
             [
                 "Region: AWS Sydney (ap-southeast-2).",
                 "Modular IaC: Custom VPC, public/private subnets, Internet Gateway.",
                 "EKS Cluster: stockpulse-eks-cluster provisioned and verified ACTIVE.",
                 "Strict Cost Control: Cleanly destroyed via terraform destroy to preserve $100 credit."
             ], accent_color=COLOR_GOLD)
    add_image_safely(s11, "aws-eks-console.png", Inches(5.4), Inches(1.6), Inches(7.1), Inches(2.3))
    add_image_safely(s11, "aws-vpc-console.png", Inches(5.4), Inches(4.1), Inches(7.1), Inches(2.3))

    # ==========================================
    # SLIDE 12: APPLICATION OUTPUT: DASHBOARD & MOBILE
    # ==========================================
    s12 = add_base_slide("Application Output: Live Dashboard & Responsive Mobile", "11. APPLICATION RESULTS")
    add_card(s12, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "Warehouse Operator UX",
             [
                 "Desktop Command Center: Real-time stock levels, SKU lookups, and restocking modal.",
                 "Visual Badges: Instant color-coded alerts for Low Stock and Critical items.",
                 "Mobile Ready: Fully responsive down to 375px (iPhone SE) for handheld barcode scanners."
             ], accent_color=COLOR_CYAN)
    add_image_safely(s12, "frontend-dashboard.png", Inches(5.4), Inches(1.6), Inches(4.5), Inches(4.8))
    add_image_safely(s12, "m1-mobile-view.png", Inches(10.1), Inches(1.6), Inches(2.4), Inches(4.8))

    # ==========================================
    # SLIDE 13: OBSERVABILITY & METRICS
    # ==========================================
    s13 = add_base_slide("Observability: Prometheus Telemetry & Probes", "12. MONITORING & TELEMETRY")
    add_card(s13, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "System Telemetry & Health",
             [
                 "Prometheus /metrics endpoint exposes live request rates, latency, and status codes.",
                 "Liveness Probe (/health): Actively verifies database connection and app uptime.",
                 "Grafana Dashboards: Visual panels configured to monitor RPS and cluster resources."
             ], accent_color=COLOR_GREEN)
    add_image_safely(s13, "m9-metrics-curl.png", Inches(5.4), Inches(1.6), Inches(7.1), Inches(4.8))

    # ==========================================
    # SLIDE 14: RESILIENCE & CHAOS TROUBLESHOOTING
    # ==========================================
    s14 = add_base_slide("Troubleshooting & Resilience: Chaos Engineering Lab", "13. FAILURE DIAGNOSIS & RECOVERY")
    add_card(s14, Inches(0.8), Inches(1.6), Inches(4.3), Inches(4.8),
             "Production Failure Runbook",
             [
                 "Scenario: Broken image tag injected via troubleshooting/broken-image.yaml.",
                 "Diagnostic: kubectl describe pod identifies ImagePullBackOff and root-cause event.",
                 "Resilience: Existing pods continue serving traffic with zero service disruption.",
                 "Proven playbook for rapid incident resolution in high-stakes environments."
             ], accent_color=COLOR_GOLD)
    add_image_safely(s14, "m9-troubleshooting.png", Inches(5.4), Inches(1.6), Inches(7.1), Inches(4.8))

    # ==========================================
    # SLIDE 15: SUMMARY & 100/100 GRADING RUBRIC PARITY
    # ==========================================
    s15 = add_base_slide("Project Summary: Complete 10-Module Rubric Parity", "14. GRADING SCORECARD")
    add_card(s15, Inches(0.8), Inches(1.6), Inches(2.7), Inches(4.8),
             "App & Quality",
             [
                 "M1: 3-Tier FastAPI/React.",
                 "M2: 11 Pytest tests pass.",
                 "M3: Conventional Git commits.",
                 "Full Swagger & OpenAPI."
             ], accent_color=COLOR_GREEN)

    add_card(s15, Inches(3.75), Inches(1.6), Inches(2.7), Inches(4.8),
             "Containerization",
             [
                 "M4: Multi-stage Docker.",
                 "Non-root UIDs 10001 & 101.",
                 "Docker Compose healthchecks.",
                 "ACID Postgres storage."
             ], accent_color=COLOR_CYAN)

    add_card(s15, Inches(6.7), Inches(1.6), Inches(2.7), Inches(4.8),
             "Pipeline & Security",
             [
                 "M5: 5-Stage GitHub Actions.",
                 "M6: Trivy DevSecOps scan.",
                 "M7: Terraform AWS EKS.",
                 "Sydney region verified."
             ], accent_color=COLOR_GOLD)

    add_card(s15, Inches(9.65), Inches(1.6), Inches(2.7), Inches(4.8),
             "Orchestration & Ops",
             [
                 "M8: Kubernetes Helm chart.",
                 "M9: Prometheus telemetry.",
                 "M10: Troubleshooting lab.",
                 "Score Target: 100 / 100."
             ], accent_color=COLOR_GREEN)

    # Save presentation
    os.makedirs("docs/presentation", exist_ok=True)
    deck_path_root = "StockPulse_Presentation.pptx"
    deck_path_docs = "docs/presentation/StockPulse_Presentation.pptx"

    prs.save(deck_path_root)
    prs.save(deck_path_docs)
    print(f"Presentation successfully created at {deck_path_root} and {deck_path_docs}!")

if __name__ == "__main__":
    create_deck()
