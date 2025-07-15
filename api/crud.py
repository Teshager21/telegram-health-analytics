from sqlalchemy.orm import Session
from sqlalchemy import text


def get_top_products(db: Session, limit: int):
    result = db.execute(
        text(
            """
        SELECT product_name AS product, COUNT(*) AS mentions
        FROM fct_product_mentions
        GROUP BY product_name
        ORDER BY mentions DESC
        LIMIT :limit
    """
        ),
        {"limit": limit},
    )

    return [dict(row._mapping) for row in result]


def get_channel_activity(db: Session, channel_name: str):
    sql = text(
        """
        SELECT channel_name,
               CAST(date_trunc('day', message_date) AS DATE) AS day,
               COUNT(*) AS messages
        FROM fct_messages
        WHERE channel_name = :channel
        GROUP BY channel_name, day
        ORDER BY day
    """
    )
    result = db.execute(sql, {"channel": channel_name}).fetchall()
    return [dict(row._mapping) for row in result]


def search_messages(db: Session, query: str):
    sql = text(
        """
        SELECT message_id, channel_name, message AS message_text
        FROM stg_telegram_messages
        WHERE message ILIKE :query
    """
    )
    result = db.execute(sql, {"query": f"%{query}%"}).fetchall()
    return [dict(row._mapping) for row in result]
