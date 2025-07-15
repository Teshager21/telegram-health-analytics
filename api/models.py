from sqlalchemy import MetaData

metadata = MetaData()

# Define table metadata only if you want to use ORM
# Otherwise, skip models and run SQL queries directly in crud.py
