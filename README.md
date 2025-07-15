# 📊 Telegram Health Analytics

**Telegram Health Analytics** is a pipeline-based data platform that collects, processes, and analyzes multimedia content (images and text) from Telegram business accounts, applying deep learning and NLP techniques to extract insights. This project is designed with modularity, observability, and scalability in mind—leveraging modern data tools such as **Dagster**, **YOLOv8**, **DBT**, and **PostgreSQL**.

---

## 🚀 Project Overview

**Goal:**
To build a robust data analytics system that scrapes Telegram media posts from business channels, applies object detection and enrichment using YOLOv8, transforms the data using DBT models, and stores the results in a Postgres data warehouse for reporting and decision-making.

---

## 🧱 Architecture

       ┌───────────────┐
       │ Telegram API  │
       └──────┬────────┘
              │
     scrape_telegram_data
              ▼
    ┌────────────────────┐
    │ Raw Media & JSON   │
    │  (local storage)   │
    └────────┬───────────┘
             │
 load_raw_to_postgres (psycopg2)
             ▼
    ┌────────────────────┐
    │ Postgres: raw layer│
    └────────┬───────────┘
             │
run_yolo_enrichment (YOLOv8)
             ▼
     ┌────────────────────┐
     │ Object Detection   │
     └────────┬───────────┘
              │
     run_dbt_transformations
              ▼
     ┌────────────────────┐
     │ DBT + PostgreSQL   │
     │ analytics layer    │
     └────────────────────┘


---

## 🛠️ Tech Stack

| Component          | Tool/Library                              |
|-------------------|-------------------------------------------|
| Workflow Orchestration | [Dagster](https://dagster.io/)              |
| Object Detection   | [YOLOv8 (Ultralytics)](https://docs.ultralytics.com/) |
| Data Warehouse     | PostgreSQL                                |
| Data Modeling      | [DBT (Data Build Tool)](https://docs.getdbt.com/) |
| Telegram Scraping  | [Telethon](https://docs.telethon.dev/) or similar |
| Python Scripts     | Python 3.12                               |
| Environment Management | `venv` or `conda`                      |

---

## 🧩 Pipeline Components

### 1. `scrape_telegram_data.py`
Scrapes messages and media files (images) from Telegram public business channels using a Telegram API client.

### 2. `load_raw_to_telegram.py`
Inserts metadata of scraped messages and media into the raw Postgres tables.

### 3. `yolo_image_detection.py`
Runs YOLOv8 object detection on Telegram images and stores results in the `fct_image_detections` table.

### 4. `run_dbt_transformations`
Executes DBT models to transform raw data into analytics-ready formats, like daily message summaries, object frequency, or channel engagement trends.

---

## 🗂️ Folder Structure

telegram-health-analytics/
│
├── src/
│ ├── scraping/ # Telegram scraping logic
│ ├── etl/ # Raw-to-postgres + YOLO enrichment scripts
│ ├── dbt/ # DBT models and project config
│
├── pipelines/
│ └── pipeline.py # Dagster pipeline definition
│
├── data/
│ └── raw/telegram_images/ # Raw downloaded images
│
├── telegram_dbt_project/ # DBT project folder
├── README.md
├── requirements.txt
├── dagster.yaml
└── .env # PostgreSQL & Telegram API credentials


---

## ⚙️ Setup & Usage

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/telegram-health-analytics.git
cd telegram-health-analytics
```
## 2. Create and Activate Virtual Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 3. Set up .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=telegram_dw
DB_USER=postgres
DB_PASSWORD=yourpassword
TG_API_ID=your_telegram_api_id
TG_API_HASH=your_telegram_api_hash

## 4. Run the Pipeline with Dagster
dagster dev
# Or execute pipeline directly
python3 pipelines/pipeline.py

## 5. Run DBT Models
cd telegram_dbt_project
dbt run

✅ Features

    ✅ Telegram data scraping from public business accounts

    ✅ Image object detection using YOLOv8

    ✅ PostgreSQL data warehouse

    ✅ DBT for transformation and analytics

    ✅ Dagster orchestration and scheduling

    ✅ Environment variables for flexible deployment


## 📈 Sample Use Cases

    Track brand presence by analyzing objects in images (e.g., cosmetics, medicine bottles).

    Identify high-engagement Telegram posts based on image richness.

    Detect trends in visual marketing strategies over time.

## 🧪 Testing
Ensure your components work independently:

# Test YOLO script
python3 src/etl/yolo_image_detection.py

# Test DBT models
cd telegram_dbt_project
dbt debug
dbt run

## 👥 Contributors

    Teshager Admasu – Developer & Data Engineer

    10 Academy – Challenge Host

    Open Source Libraries – PyTorch, Ultralytics, Telethon, Dagster, DBT

## 📄 License

MIT License. See LICENSE for details.
🙏 Acknowledgements

    Ultralytics YOLOv8

    Dagster

    DBT

    Telethon
