# AIS FastAPI + Streamlit Vessel Tracker

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)

## 🚢 Overview

**AIS FastAPI + Streamlit Vessel Tracker** is a lightweight full‑stack Python application for visualizing AIS (Automatic Identification System) data stored in a PostGIS database. It exposes vessel positions via a FastAPI backend and renders them on an interactive map through a Streamlit frontend, complete with pagination and filtering.

## ✨ Features

* **FastAPI backend**: Serves AIS data in GeoJSON format via RESTful endpoints.
* **Streamlit frontend**: Interactive map powered by [pydeck](https://pydeck.gl/) and [Streamlit](https://streamlit.io/).
* **Filtering & Pagination**: Control the number of records fetched from the API.
* **Containerized**: Docker Compose setup for PostGIS, Adminer, and pgAdmin.

## 🛠️ Tech Stack

| Layer     | Technology                |
| --------- | ------------------------- |
| Database  | PostgreSQL + PostGIS      |
| ORM       | SQLAlchemy + GeoAlchemy2  |
| API       | FastAPI                   |
| Frontend  | Streamlit, pydeck, pandas |
| Container | Docker, Docker Compose    |

## 📦 Prerequisites

* [Docker & Docker Compose](https://docs.docker.com/compose/install/)
* [Python 3.11+](https://www.python.org/downloads/)
* `pip` package manager

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ksubc/AIS-FastAPI-Streamlit.git
cd AIS-FastAPI-Streamlit
```

### 2. Start the PostGIS database

```bash
docker-compose up -d db adminer pgadmin
```

* **Adminer** available at: [http://localhost:8080](http://localhost:8080)
* **pgAdmin** available at:  [http://localhost:5050](http://localhost:5050) (login with credentials in `.env.pgadmin`)

### 3. Configure your environment variables

Copy the existing `.env` into the backend folder (unmodified):

```bash
cp .env backend/.env
```

### 4. Run the FastAPI backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Your API is now live at: `http://localhost:8000/vessels/?limit=50`

### 5. Run the Streamlit frontend

In a separate terminal:

```bash
# ensure you have Streamlit dependencies
pip install streamlit pandas requests pydeck python-dotenv

# launch the app
streamlit run streamlit_app.py --server.port 8501
```

Open the map at: [http://localhost:8501](http://localhost:8501)

## 🐳 Docker-compose All‑in‑One (Optional)

To run API + Streamlit together:

```yaml
services:
  api:
    build: ./backend
    env_file: ./backend/.env
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --port 8000

  web:
    image: python:3.11
    working_dir: /app
    volumes:
      - ./:/app
    command: bash -c "pip install streamlit pandas requests pydeck python-dotenv && \
                     streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"
    ports:
      - "8501:8501"
    env_file:
      - .env
    depends_on:
      - api
```

```bash
docker-compose up -d db api web
```

## ⚙️ Environment Variables

| Variable            | Description                    | Default                          |
| ------------------- | ------------------------------ | -------------------------------- |
| `POSTGRES_DB`       | Database name                  | `mydatabase`                     |
| `POSTGRES_USER`     | Database username              | `aisuser`                        |
| `POSTGRES_PASSWORD` | Database password              | `aispass`                        |
| `DB_HOST`           | Postgres host (inside backend) | `localhost`                      |
| `DB_PORT`           | Postgres port                  | `5432`                           |
| `API_URL`           | FastAPI endpoint for Streamlit | `http://localhost:8000/vessels/` |

## 🎯 Usage

1. **Inspect raw data**: view the table of AIS records in the sidebar.
2. **Adjust record count**: use the slider to fetch more or fewer vessels.
3. **Explore the map**: pan, zoom, and click on vessel points for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the **MIT License**.

---

*Built with ❤️ by Kyle Sanchez*
