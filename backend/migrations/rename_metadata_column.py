""
Migration script to rename the 'metadata' column to 'meta_data' in the notifications table.
"""
from sqlalchemy import text
from database import engine

def upgrade():
    """Rename the column from 'metadata' to 'meta_data'"""
    with engine.connect() as conn:
        # For SQLite
        conn.execute(text("""
            CREATE TABLE notifications_new (
                id INTEGER NOT NULL, 
                user_id INTEGER NOT NULL, 
                title VARCHAR NOT NULL, 
                message VARCHAR NOT NULL, 
                notification_type VARCHAR NOT NULL, 
                meta_data JSON, 
                is_read BOOLEAN, 
                created_at DATETIME, 
                read_at DATETIME, 
                PRIMARY KEY (id), 
                FOREIGN KEY(user_id) REFERENCES users (id)
            )
        """))
        
        # Copy data from old table to new table
        conn.execute(text("""
            INSERT INTO notifications_new 
            (id, user_id, title, message, notification_type, meta_data, is_read, created_at, read_at)
            SELECT id, user_id, title, message, notification_type, metadata, is_read, created_at, read_at
            FROM notifications
        """))
        
        # Drop old table and rename new one
        conn.execute(text("DROP TABLE notifications"))
        conn.execute(text("ALTER TABLE notifications_new RENAME TO notifications"))
        
        # Recreate indexes
        conn.execute(text("CREATE INDEX ix_notifications_id ON notifications (id)"))
        conn.execute(text("CREATE INDEX ix_notifications_user_id ON notifications (user_id)"))
        
        conn.commit()

def downgrade():
    """Revert the column name back to 'metadata'"""
    with engine.connect() as conn:
        # For SQLite
        conn.execute(text("""
            CREATE TABLE notifications_old (
                id INTEGER NOT NULL, 
                user_id INTEGER NOT NULL, 
                title VARCHAR NOT NULL, 
                message VARCHAR NOT NULL, 
                notification_type VARCHAR NOT NULL, 
                metadata JSON, 
                is_read BOOLEAN, 
                created_at DATETIME, 
                read_at DATETIME, 
                PRIMARY KEY (id), 
                FOREIGN KEY(user_id) REFERENCES users (id)
            )
        """))
        
        # Copy data from new table to old table
        conn.execute(text("""
            INSERT INTO notifications_old 
            (id, user_id, title, message, notification_type, metadata, is_read, created_at, read_at)
            SELECT id, user_id, title, message, notification_type, meta_data, is_read, created_at, read_at
            FROM notifications
        """))
        
        # Drop new table and rename old one
        conn.execute(text("DROP TABLE notifications"))
        conn.execute(text("ALTER TABLE notifications_old RENAME TO notifications"))
        
        # Recreate indexes
        conn.execute(text("CREATE INDEX ix_notifications_id ON notifications (id)"))
        conn.execute(text("CREATE INDEX ix_notifications_user_id ON notifications (user_id)"))
        
        conn.commit()

if __name__ == "__main__":
    print("Running database migration...")
    upgrade()
    print("Migration completed successfully.")
