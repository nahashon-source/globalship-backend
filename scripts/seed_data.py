"""
Seed database with test data.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
import uuid
from datetime import datetime

# Import models directly
from app.models.user import User

db = SessionLocal()

try:
    print("=" * 60)
    print("Seeding GlobalShip Database")
    print("=" * 60)
    
    # Check if admin already exists
    admin_email = "admin@globalship.com"
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    
    if not existing_admin:
        # Create admin user
        admin = User(
            id=uuid.uuid4(),
            email=admin_email,
            hashed_password=get_password_hash("Admin123456"),
            full_name="Admin User",
            company_name="GlobalShip Admin",
            is_active=True,
            is_verified=True,
            is_superuser=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(admin)
        db.commit()
        print(f"✅ Created admin user: {admin_email}")
    else:
        print(f"ℹ️  Admin user already exists: {admin_email}")
    
    # Check if demo user already exists
    demo_email = "demo@globalship.com"
    existing_demo = db.query(User).filter(User.email == demo_email).first()
    
    if not existing_demo:
        # Create demo user
        demo = User(
            id=uuid.uuid4(),
            email=demo_email,
            hashed_password=get_password_hash("Demo123456"),
            full_name="Demo User",
            company_name="Demo Company",
            is_active=True,
            is_verified=True,
            is_superuser=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(demo)
        db.commit()
        print(f"✅ Created demo user: {demo_email}")
    else:
        print(f"ℹ️  Demo user already exists: {demo_email}")
    
    print("\n" + "=" * 60)
    print("✅ Seed data created successfully!")
    print("=" * 60)
    print("\nTest Credentials:")
    print("┌" + "─" * 58 + "┐")
    print("│ Admin: admin@globalship.com / Admin123456" + " " * 16 + "│")
    print("│ Demo:  demo@globalship.com  / Demo123456" + " " * 17 + "│")
    print("└" + "─" * 58 + "┘")
    print()
    
except Exception as e:
    print(f"\n❌ Error seeding data: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
