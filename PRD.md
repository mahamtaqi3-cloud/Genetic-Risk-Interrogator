# Product Requirements Document (PRD): Genetic Risk Interrogator

## 1. Executive Summary

The **Genetic Risk Interrogator** is a clinical-grade web application designed to mitigate ancestral bias in Polygenic Risk Scores (PRS). Standard genomic risk models are predominantly trained on European cohorts, often resulting in inaccurate risk over-attribution for patients of diverse or mixed ancestral backgrounds. This application provides a multi-ancestry adjustment framework, combining global admixture fractions and environmental risk multipliers to deliver clinically actionable, equitable risk assessments paired with automated PDF report generation.

---

## 2. Problem Statement

* **Ancestral Bias in GWAS Datasets:** Over 80% of genome-wide association studies (GWAS) use data from individuals of European descent, skewing baseline risk models.
* **Clinical Risk Misinterpretation:** Applying a standard PRS to non-European or multi-ancestry patients can lead to false-positive alarms or misinformed clinical interventions.
* **Lack of Contextual Multipliers:** Traditional calculators often isolate genetics from environmental and lifestyle stressors, missing vital multi-factorial risk components.

---

## 3. Product Goals & Objectives

* **Equitable Risk Adjustment:** Implement a mathematical correction model that scales raw PRS based on a patient’s unique global admixture profile (European, African, East Asian, South Asian).
* **Environmental Contextualization:** Allow real-time adjustments using environmental risk multipliers.
* **Clinical Usability:** Offer preset clinical personas for fast validation and an intuitive dashboard.
* **Auditability & Reporting:** Generate clean, downloadable professional PDF diagnostic reports for patient records and clinical review.

---

## 4. Target Users & Personas

* **Clinicians & Genetic Counselors:** Professionals seeking to interpret genomic data safely across diverse patient populations.
* **Researchers & Bioinformaticians:** Evaluators exploring bias-mitigation models in genomic medicine.
* **Hackathon Judges:** Reviewers assessing clinical utility, technical implementation, and UI/UX design.

---

## 5. Core Features & Functional Requirements

### A. Patient Intake & Persona Presets

* **Requirement:** Provide sidebar controls for quick-loading clinical personas (e.g., Mixed West African/European, East Asian Urban Cohort, South Asian Baseline) alongside custom parameter inputs.
* **Input Parameters:** Raw Polygenic Risk Score (numeric) and Environmental Risk Multiplier (slider ranging from 0.5 to 2.0).

### B. Global Ancestry Admixture Module

* **Requirement:** Enable clinicians to input percentage fractions across four major global populations (European, African, East Asian, South Asian).
* **Validation:** Real-time calculation ensuring total admixture sums to 100%, triggering warnings for invalid distributions.

### C. Contextual Risk Engine & Visualization

* **Requirement:** Compute a bias-corrected adjusted risk score using ancestry weighting.
* **Data Visualization:** Render an interactive Altair bar chart displaying population fraction percentages clearly with distinct color-coding.

### D. Comparative Analytics & Exportable PDF Reporting

* **Requirement:** Provide side-by-side metric comparisons contrasting uncorrected standard baseline risk against context-adjusted risk.
* **PDF Generation:** Automatically compile patient summaries, admixture breakdowns, and clinical recommendations into a formatted PDF via `fpdf` for instant local download.

---

## 6. Technology Stack

* **Frontend & UI Framework:** Streamlit (Python) configured with a custom luxury purple clinical theme and styling (`config.toml`).
* **Data Processing & Visualization:** Pandas, Altair.
* **Reporting:** FPDF (Python library for dynamic document layout and rendering).
