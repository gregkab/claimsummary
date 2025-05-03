# Database Setup Guide

This guide will help you set up the PostgreSQL database for the Claim Action Intelligence application.

## Prerequisites

- PostgreSQL installed on your system (version 12 or higher recommended)
- Python environment set up with dependencies installed

## Steps to Set Up the Database

### 1. Create a PostgreSQL Database

Connect to your PostgreSQL server and create a new database:

```bash
psql -U postgres
```

In the PostgreSQL shell:

```sql
CREATE DATABASE claimsummary;
```

### 2. Create a Database User (Optional)

If you want to use a specific user instead of the default postgres user:

```sql
CREATE USER claimuser WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE claimsummary TO claimuser;
```

### 3. Configure Environment Variables

Copy the provided `env.example` file to `.env` in the backend directory:

```bash
cp env.example backend/.env
```

Edit the `.env` file and update the `DATABASE_URL` with your specific connection details:

```
DATABASE_URL=postgresql://username:password@localhost:5432/claimsummary
```

Also, add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run Database Migrations

Execute the migrations script to create the database tables:

```bash
cd backend
python migrations.py
```

This will create all the required tables in your database.

### 5. Load Sample Data (Optional)

To populate the database with sample data for development and testing:

```bash
python seed_data.py
```

This will create 3 sample claims, 5 email threads, and 8 action items.

## Verifying the Setup

You can verify your database setup by running:

```bash
psql -U postgres -d claimsummary -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
```

You should see a list of tables including `claims`, `email_threads`, and `action_items`.

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Ensure PostgreSQL is running:
   ```bash
   sudo service postgresql status  # Linux
   brew services list              # macOS
   ```

2. Check if you can connect to the database directly:
   ```bash
   psql -U postgres -d claimsummary
   ```

3. Verify your DATABASE_URL format:
   ```
   postgresql://username:password@host:port/database_name
   ```

### Migration Errors

If you encounter migration errors:

1. Check for any error messages in the console output
2. Ensure your PostgreSQL user has the necessary permissions
3. Try dropping and recreating the database:
   ```sql
   DROP DATABASE claimsummary;
   CREATE DATABASE claimsummary;
   ``` 