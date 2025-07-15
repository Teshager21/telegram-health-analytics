from dagster import op, job, schedule
import subprocess


@op
def scrape_telegram_data():
    # Example: call your scraping script
    subprocess.run(["python3", "src/scraping/scrape_telegram.py"], check=True)
    return "Scraping done"


@op
def load_raw_to_postgres():
    # Example: call your load script
    subprocess.run(["python3", "src/etl/load_raw_telegram.py"], check=True)
    return "Load to Postgres done"


@op
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run"],
        cwd="telegram_dbt_project",  # <--- this is the key fix
        check=True,
    )


@op
def run_yolo_enrichment():
    # Run your YOLO enrichment script
    subprocess.run(["python3", "src/etl/yolo_image_detection.py"], check=True)
    return "YOLO enrichment done"


@job
def telegram_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()


@schedule(
    cron_schedule="0 0 * * *", job=telegram_data_pipeline, execution_timezone="UTC"
)
def daily_telegram_pipeline_schedule():
    return {}
