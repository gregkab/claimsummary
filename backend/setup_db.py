"""
Database setup utility for Claim Action Intelligence.
This script helps you create and set up your PostgreSQL database.
"""

import os
import sys
import subprocess
import getpass
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()

def create_env_file():
    """Create a .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        env_example = os.path.join('..', 'env.example')
        
        if os.path.exists(env_example):
            with open(env_example, 'r') as src, open('.env', 'w') as dest:
                dest.write(src.read())
            print(".env file created from example")
        else:
            # Create a basic .env file
            with open('.env', 'w') as f:
                f.write("DATABASE_URL=postgresql://postgres:postgres@localhost:5432/claimsummary\n")
                f.write("OPENAI_API_KEY=\n")
                f.write("FRONTEND_URL=http://localhost:3000\n")
            print("Basic .env file created")
    else:
        print(".env file already exists")

def setup_database():
    """Set up the PostgreSQL database"""
    print("\n=== Database Setup ===")
    db_name = input("Enter database name [claimsummary]: ") or "claimsummary"
    db_user = input("Enter database user [postgres]: ") or "postgres"
    db_password = getpass.getpass("Enter database password: ")
    db_host = input("Enter database host [localhost]: ") or "localhost"
    db_port = input("Enter database port [5432]: ") or "5432"
    
    # Set DATABASE_URL in .env file
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(f"DATABASE_URL={connection_string}\n")
        
        # Preserve or add OpenAI API key
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        if not openai_key:
            openai_key = getpass.getpass("Enter your OpenAI API key: ")
        f.write(f"OPENAI_API_KEY={openai_key}\n")
        
        # Add frontend URL
        f.write("FRONTEND_URL=http://localhost:3000\n")
    
    print(f"Database connection string saved to .env file")
    
    # Create a test connection to PostgreSQL
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy_utils import database_exists, create_database
        
        print(f"Testing connection to PostgreSQL...")
        engine = create_engine(connection_string)
        
        if database_exists(engine.url):
            print(f"Database '{db_name}' already exists.")
            recreate = input("Do you want to recreate it? (y/n): ").lower() == 'y'
            if recreate:
                # Try to drop the database - first using psycopg2 directly
                try:
                    import psycopg2
                    # Connect to postgres database instead of the target database
                    conn_params = {
                        'dbname': 'postgres',
                        'user': db_user,
                        'password': db_password,
                        'host': db_host,
                        'port': db_port
                    }
                    
                    # Connect, set isolation level, and drop database
                    import psycopg2.extensions
                    conn = psycopg2.connect(**conn_params)
                    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                    cursor = conn.cursor()
                    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
                    conn.close()
                    print(f"Database '{db_name}' dropped.")

                    # Recreate the database
                    postgres_engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres")
                    create_database(engine.url)
                    print(f"Database '{db_name}' recreated.")
                except Exception as e:
                    print(f"Error dropping database: {str(e)}")
                    print("Attempting alternative method...")
                    
                    # Alternative method: Use subprocess to call dropdb
                    try:
                        env = os.environ.copy()
                        env["PGPASSWORD"] = db_password
                        subprocess.run(
                            ["dropdb", "-h", db_host, "-p", db_port, "-U", db_user, db_name], 
                            env=env,
                            check=True
                        )
                        subprocess.run(
                            ["createdb", "-h", db_host, "-p", db_port, "-U", db_user, db_name],
                            env=env,
                            check=True
                        )
                        print(f"Database '{db_name}' recreated using command line tools.")
                    except Exception as e:
                        print(f"Error recreating database with command line tools: {str(e)}")
                        print("Unable to recreate the database. Will use the existing one.")
        else:
            create_database(engine.url)
            print(f"Database '{db_name}' created.")
            
        # Reload environment variables to make sure we're using the updated connection string
        load_dotenv(override=True)
        return True
            
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {str(e)}")
        return False
    
    return True

def run_migrations():
    """Run database migrations"""
    try:
        print("\nRunning database migrations...")
        # Reload environment variables to ensure we have the latest
        os.environ.clear()
        load_dotenv(override=True)
        import migrations
        migrations.create_tables()
        print("Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"Error running migrations: {str(e)}")
        return False

def seed_database():
    """Seed the database with sample data"""
    try:
        print("\nSeeding database with sample data...")
        # Reload environment variables to ensure we have the latest
        os.environ.clear()
        load_dotenv(override=True)
        import seed_data
        seed_data.create_seed_data()
        print("Database seeded successfully!")
        return True
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        return False

def main():
    """Main function to run the setup process"""
    print("Welcome to the Claim Action Intelligence Database Setup Utility")
    
    # Create .env file
    create_env_file()
    
    # Set up database connection
    if setup_database():
        # Run migrations
        if run_migrations():
            # Ask if user wants to seed the database
            if input("\nDo you want to seed the database with sample data? (y/n): ").lower() == 'y':
                seed_database()
    
    print("\nSetup complete! You can now start the application with:")
    print("uvicorn app.main:app --reload")

if __name__ == "__main__":
    main() 