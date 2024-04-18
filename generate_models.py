import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# DB parameters.
db_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")

print(f"Getting the database params {db_uri}")

# Create SQLAlchemy Engine & Metadata
engine  = create_engine(db_uri)
metadata = MetaData()

# List of schemas to reflect
schemas = ['dev', 'aud']

# Bind metadata to engine
metadata.bind = engine

# Reflect database tables into MetaData for each schema
for schema in schemas:
    metadata.reflect(bind=engine, schema=schema)

# Print the number of tables reflected
print(f"Number of tables reflected: {len(metadata.tables)}")

# Create declarative base
Base = declarative_base(metadata=metadata)

# Print the generated model classes
for table in metadata.tables.values():
    print(f"Creating model for table: {table.name}")
    print(f"class {table.name.capitalize()}(Base):")
    print("    __tablename__ = '" + table.name + "'")
    for column in table.columns:
        print("    " + column.name + " = Column(" + repr(str(column.type)) + ")")
    print("\n")