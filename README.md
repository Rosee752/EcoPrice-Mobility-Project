# 🚴 EcoPrice: AI-Powered Mobility Optimization Pipeline

## 🚀 Project Overview
A full-stack data engineering and machine learning project that optimizes micro-mobility operations in Frankfurt. The system ingests real-time IoT data from **297 bike stations**, processes it through an ETL pipeline, and serves demand predictions via an interactive dashboard.

This project solves the "Cold Start" problem by implementing a custom scheduler to build a historical dataset, allowing the ML model to learn distinct day/night demand cycles.

**Live Demo:** [Link to your Streamlit Cloud app if you deploy it]

---

## 🏗️ Architecture & Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Ingestion** | **Python (Requests)** | Automated script hitting CityBikes API every 30 mins. |
| **Orchestration** | **Custom Scheduler** | Python-based cron job for reliable data harvesting. |
| **Storage** | **CSV / Flat File** | Structured storage simulating a Data Lake. |
| **ML Model** | **Scikit-Learn** | RandomForestRegressor trained on spatiotemporal features. |
| **Visualization** | **Streamlit** | Interactive dashboard for real-time monitoring & AI inference. |

---

## 📊 Key Features

### 1. Robust Data Pipeline (ETL)
* Built a fault-tolerant ingestion script (`fetch_data.py`) that handles API outages and schema changes.
* Implemented append-only logic to build a historical time-series dataset without data loss.

### 2. Machine Learning Inference
* **Problem:** Predicting bike availability based on time and location.
* **Solution:** Removed "leakage features" (like empty slots) to force the model to learn temporal patterns.
* **Result:** Successfully predicts the **60% drop in availability** during evening commuter hours at major hubs like *Galluswarte*.

### 3. Business Intelligence Dashboard
* Interactive map showing real-time fleet distribution.
* "Ask the AI" interface allowing stakeholders to simulate future demand scenarios.

---

## 🛠️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [Your GitLab Link Here]
   cd EcoPrice_Project
