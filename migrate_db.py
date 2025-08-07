#!/usr/bin/env python3
"""
Database migration script for Render deployment
"""

import os
from sqlalchemy import create_engine, text
from config import Config

def migrate_database():
    """Migrate database to support BigInteger telegram_id"""
    print("🔄 Starting database migration...")
    
    try:
        # Create engine
        engine = create_engine(Config.DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            """))
            
            if result.fetchone():
                print("✅ Users table exists, checking column type...")
                
                # Check telegram_id column type
                result = conn.execute(text("""
                    SELECT data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name = 'telegram_id'
                """))
                
                column_type = result.fetchone()
                if column_type and column_type[0] == 'integer':
                    print("⚠️  telegram_id is INTEGER, migrating to BIGINT...")
                    
                    # Migrate telegram_id to BIGINT
                    conn.execute(text("""
                        ALTER TABLE users 
                        ALTER COLUMN telegram_id TYPE BIGINT
                    """))
                    
                    # Migrate user_id in related tables
                    tables = ['wallets', 'income_sources', 'expense_categories', 'transactions']
                    for table in tables:
                        try:
                            conn.execute(text(f"""
                                ALTER TABLE {table} 
                                ALTER COLUMN user_id TYPE BIGINT
                            """))
                            print(f"✅ Migrated {table}.user_id to BIGINT")
                        except Exception as e:
                            print(f"⚠️  Could not migrate {table}.user_id: {e}")
                    
                    conn.commit()
                    print("✅ Database migration completed successfully!")
                else:
                    print("✅ telegram_id is already BIGINT or doesn't exist")
            else:
                print("ℹ️  Users table doesn't exist, will be created with correct types")
                
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    migrate_database() 