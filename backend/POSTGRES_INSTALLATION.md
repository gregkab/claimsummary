# PostgreSQL Installation Guide

This guide will help you install and configure PostgreSQL for the Claim Action Intelligence application.

## Installation

### macOS

1. **Using Homebrew**:
   ```bash
   brew install postgresql@14
   brew services start postgresql@14
   ```

2. **Using Postgres.app** (Alternative):
   - Download and install from [postgresapp.com](https://postgresapp.com/)
   - Open the app to start the PostgreSQL server

### Windows

1. **Using Installer**:
   - Download the installer from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Run the installer and follow the wizard
   - Make sure to remember the password you set for the postgres user
   - Launch pgAdmin to verify installation

### Linux (Ubuntu/Debian)

1. **Using apt**:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

## Verification

To verify PostgreSQL is running:

### macOS
```bash
# Check if PostgreSQL is running via Homebrew
brew services list

# Or via ps
ps aux | grep postgres
```

### Windows
```bash
# Open Services app and look for PostgreSQL service
# Or use PowerShell
Get-Service postgresql*
```

### Linux
```bash
sudo systemctl status postgresql
```

## Common Issues and Solutions

### Connection Refused Error

If you get a "Connection refused" error:

1. **Check PostgreSQL is running**:
   - Use the verification commands above

2. **Check PostgreSQL configuration**:
   - Locate and check your `postgresql.conf` file:
     - macOS (Homebrew): `/usr/local/var/postgresql@14/postgresql.conf`
     - Windows: `C:\Program Files\PostgreSQL\14\data\postgresql.conf`
     - Linux: `/etc/postgresql/14/main/postgresql.conf`
   - Ensure it's listening on the correct address:
     ```
     listen_addresses = '*'  # or 'localhost'
     ```

3. **Check client authentication**:
   - Locate and check your `pg_hba.conf` file (in the same directory as `postgresql.conf`)
   - Ensure it allows local connections:
     ```
     # IPv4 local connections:
     host    all             all             127.0.0.1/32            md5
     # IPv6 local connections:
     host    all             all             ::1/128                 md5
     ```

4. **Restart PostgreSQL**:
   - macOS: `brew services restart postgresql@14`
   - Windows: Restart via Services app
   - Linux: `sudo systemctl restart postgresql`

### Port Conflict

If PostgreSQL can't start because of a port conflict:

1. **Check if something else is using port 5432**:
   ```bash
   # On macOS/Linux
   sudo lsof -i :5432
   
   # On Windows (PowerShell)
   netstat -ano | findstr 5432
   ```

2. **Change PostgreSQL port**:
   - Edit `postgresql.conf` and change:
     ```
     port = 5433  # or another free port
     ```
   - Restart PostgreSQL
   - Update your `.env` file to use the new port

## Basic PostgreSQL Commands

Once PostgreSQL is running, you can:

1. **Connect to PostgreSQL**:
   ```bash
   # Connect as postgres user
   psql -U postgres
   ```

2. **Create a database**:
   ```sql
   CREATE DATABASE claimsummary;
   ```

3. **List databases**:
   ```sql
   \l
   ```

4. **Connect to a database**:
   ```sql
   \c claimsummary
   ```

5. **List tables**:
   ```sql
   \dt
   ``` 