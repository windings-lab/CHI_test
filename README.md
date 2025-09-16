# CHI Test Project

A weather data processing application that supports both SQLite and PostgreSQL databases.

## Project Initialization

This project uses `uv` for dependency management. To initialize and run the project:

1. Install project dependencies:
   ```bash
   uv sync
   ```

2. Get your OpenWeatherMap API key:
   - Go to [OpenWeatherMap API](https://openweathermap.org/api)
   - Sign up for a free account
   - Navigate to your API keys section
   - Copy your API key

3. Create a `.env` file with your configuration:
   ```bash
   # Create .env file
   touch .env
   ```
   
   Edit the `.env` file to set your API key and database preferences:
   ```
   # API Configuration
   API_KEY=your_actual_api_key_from_openweathermap
   
   # Database Configuration
   # Set to 'sqlite' for SQLite or 'postgres' for PostgreSQL
   DATABASE_TYPE=sqlite
   
   # PostgreSQL Configuration (only used when DATABASE_TYPE=postgres)
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=db
   POSTGRES_USER=gaster
   POSTGRES_PASSWORD=admin
   ```

4. Run database migrations (required before first run):
   ```bash
   uv run alembic upgrade head
   ```

5. Run the application:
   ```bash
   uv run python src/main.py
   ```

## Database Setup

This project supports both SQLite and PostgreSQL databases.

### SQLite (Default)

SQLite is the default database and requires no additional setup. The database file will be created automatically at `data.db`.

### PostgreSQL Setup

1. Start the PostgreSQL container:
   ```bash
   docker-compose up -d
   ```

2. Set environment variables for PostgreSQL:
   ```bash
   export DATABASE_TYPE=postgresql
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432
   export POSTGRES_DB=db
   export POSTGRES_USER=gaster
   export POSTGRES_PASSWORD=admin
   ```

3. Run database migrations:
   ```bash
   uv run alembic upgrade head
   ```

## Environment Variables

| Variable            | Default     | Description                             |
|---------------------|-------------|-----------------------------------------|
| `DATABASE_TYPE`     | `sqlite`    | Database type: `sqlite` or `postgres`   |
| `POSTGRES_HOST`     | `localhost` | PostgreSQL host                         |
| `POSTGRES_PORT`     | `5432`      | PostgreSQL port                         |
| `POSTGRES_DB`       | `db`        | PostgreSQL database name                |
| `POSTGRES_USER`     | `gaster`    | PostgreSQL username                     |
| `POSTGRES_PASSWORD` | `admin`     | PostgreSQL password                     |
