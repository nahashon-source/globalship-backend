"""
Create all database tables directly using SQLAlchemy.
"""
from app.db.session import engine
from app.db.base import Base
from sqlalchemy import text

# Import all models to register them
from app.models.user import User
from app.models.shipment import Shipment
from app.models.shipment_event import ShipmentEvent
from app.models.quote import Quote
from app.models.contact_message import ContactMessage

print("=" * 60)
print("Creating GlobalShip Database Tables")
print("=" * 60)

# Test connection first
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"\n✅ Connected to PostgreSQL")
        print(f"   Version: {version[:50]}...")
except Exception as e:
    print(f"\n❌ Database connection failed: {e}")
    exit(1)

# Drop all tables first (optional - use if you want fresh start)
# print("\n⚠️  Dropping existing tables...")
# Base.metadata.drop_all(bind=engine)

# Create all tables
print("\n📦 Creating tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    exit(1)

# List created tables
print("\n" + "=" * 60)
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"📊 Database Tables ({len(tables)}):")
print("=" * 60)

for table in tables:
    columns = inspector.get_columns(table)
    print(f"\n✓ {table}")
    print(f"  Columns: {len(columns)}")
    for col in columns[:5]:  # Show first 5 columns
        print(f"    - {col['name']}: {col['type']}")
    if len(columns) > 5:
        print(f"    ... and {len(columns) - 5} more")

print("\n" + "=" * 60)
print("✅ Setup complete! Check Beekeeper Studio now.")
print("=" * 60)
print("\nBeekeeper Connection Details:")
print("  Host: localhost")
print("  Port: 5432")
print("  Database: globalship_db")
print("  Username: globalship_user")
print("  Password: globalship_password")
print("=" * 60)
