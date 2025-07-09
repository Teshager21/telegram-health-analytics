# 🚀 Shipping a Data Product: From Raw Telegram Data to an Analytical API

An end-to-end data pipeline for Telegram, leveraging:
- **Telethon** for Telegram scraping
- **dbt** for transformations
- **YOLOv8** for computer vision enrichment
- **FastAPI** for analytics APIs
- **Dagster** for orchestration

---

## 🌟 Business Need

Kara Solutions is building a data platform to analyze Ethiopian medical business trends from public Telegram channels.

**Key Questions:**
- What are the top 10 most frequently mentioned medical products?
- How does price/availability of products vary across channels?
- Which channels have the most visual content (e.g., pill vs. cream images)?
- What are daily/weekly trends in health-related posts?

---

## 🗂️ Architecture Overview

```
Telegram Channels
     │
     ▼
Data Scraping (Telethon) ➔ Data Lake (JSON files)
     │
     ▼
Raw Load into PostgreSQL
     │
     ▼
dbt Transformations ➔ Star Schema
     │
     ▼
YOLOv8 Image Detection ➔ Enriched Data Warehouse
     │
     ▼
FastAPI Analytical API
     │
     ▼
Orchestrated by Dagster
```

---

## 💾 Data Storage

- Raw JSON → stored in partitioned folders:
  ```
  data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
  ```
- PostgreSQL → raw tables, staging tables, star schema

---

## 🧩 Tech Stack

| Tool       | Purpose                                   |
|------------|-------------------------------------------|
| Telethon   | Telegram scraping                         |
| dbt        | Data transformations & modeling           |
| PostgreSQL | Data warehouse                            |
| YOLOv8     | Object detection on images                |
| FastAPI    | Analytical API                            |
| Dagster    | Pipeline orchestration                    |
| Docker     | Environment consistency                   |

---

## ✅ Tasks

### Task 0 — Project Setup

- [x] Git repository initialized
- [x] Dockerfile + docker-compose.yml
- [x] requirements.txt
- [x] .env file for secrets (Telegram API, DB creds)
- [x] python-dotenv for env management

### Task 1 — Data Scraping

- Scrape from channels like:
    - https://t.me/lobelia4cosmetics
    - https://t.me/tikvahpharma
    - https://et.tgstat.com/medicine
- Download message metadata, text, media
- Store as JSON in data lake

### Task 2 — Data Modeling & Transformation

- Load raw JSON into PostgreSQL
- dbt layers:
    - Staging
    - Star schema
        - dim_channels
        - dim_dates
        - fct_messages

### Task 3 — Data Enrichment (YOLO)

- Detect objects in images
- Create fct_image_detections
- Join results to star schema

### Task 4 — Analytical API

- FastAPI endpoints:
    - `/api/reports/top-products`
    - `/api/channels/{channel}/activity`
    - `/api/search/messages`

### Task 5 — Orchestration

- Implement Dagster pipeline
    - scrape_telegram_data
    - load_raw_to_postgres
    - run_dbt_transformations
    - run_yolo_enrichment

---

## 📆 Timeline

| Date                   | Milestone         |
|------------------------|-------------------|
| Wed 09 July 2025       | Challenge Start   |
| Sun 12 July 2025       | Interim Submission (Tasks 0-2) |
| Tue 15 July 2025       | Final Submission  |

---

## 💡 Learning Outcomes

- Modern ELT pipeline architecture
- dbt transformations
- Dimensional modeling
- Computer vision enrichment
- API development for analytics
- Orchestration with Dagster

---

## References

- [Telethon Docs](https://docs.telethon.dev/en/stable/)
- [dbt Docs](https://docs.getdbt.com/docs/introduction)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Dagster Docs](https://dagster.io/)
