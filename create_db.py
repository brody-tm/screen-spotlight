## ! This file is only to be run once !

from MovieReviewAppBackend import create_app, db
from config import DevelopmentConfig

# Create the app instance
app = create_app(DevelopmentConfig)

# Create the database tables
with app.app_context():
    try:
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")