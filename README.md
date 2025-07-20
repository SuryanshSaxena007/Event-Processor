# BCN Event-Driven Data Processor for Vendor Orders

**Design & implement an event-driven backend that ingests vendor order events, processes them asynchronously via RabbitMQ, stores/interprets them in SQLite, and exposes aggregate metrics through FastAPI.**

---

## 📝 Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)

   * [Native Setup](#native-setup)
   * [Docker Compose Setup](#docker-compose-setup)
5. [Configuration](#configuration)
6. [Database Initialization](#database-initialization)
7. [Running the Services](#running-the-services)
8. [API Endpoints](#api-endpoints)

   * [Authentication](#authentication)
   * [Event Ingestion](#event-ingestion)
   * [Vendor Metrics](#vendor-metrics)
   * [Chart Visualization](#chart-visualization)
9. [Decoding Base64 Charts](#decoding-base64-charts)
10. [Cleaning Git History](#cleaning-git-history)
11. [License](#license)

---

## ✨ Features

* **Event Ingestion** via `POST /events` into RabbitMQ
* **Asynchronous Processing**: Consumer pulls from `vendor_orders` queue
* **Business Logic**: computes `total_amount`, flags `high_value`, optional anomaly detection
* **Persistence**: Stores orders & users in SQLite (`bcn.db`)
* **Auth**: JWT‑based signup & login (`/auth/signup`, `/auth/token`)
* **Metrics API**: `GET /metrics?vendor_id=` returns totals & 7‑day volume
* **Visualization API**: `GET /metrics/chart?vendor_id=` returns Base64 PNG
* **OpenAPI docs**: available at `/docs`

---

## 🛠 Tech Stack

* **Language**: Python 3.11
* **Framework**: FastAPI, Uvicorn
* **Queue**: RabbitMQ (3-management)
* **Database**: SQLite via SQLAlchemy + aiosqlite
* **Auth**: python-jose, passlib\[bcrypt], OAuth2PasswordBearer
* **Visualization**: Matplotlib
* **Env**: python-dotenv

---

## 📋 Prerequisites

* Python 3.11+ installed
* RabbitMQ installed & management UI running on `localhost:15672`
* `git`, `curl` (or HTTP client)
* (Optional) Docker & Docker Compose if using containerized setup

---

## 🚀 Running the Services

You can run the entire stack **with** or **without** Docker. Choose the approach that suits your environment.

---

### 🐍 Without Docker (Native)

1. **Create & activate** a Python virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   . .venv/Scripts/activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Configure** environment variables in `.env`:

   ```dotenv
   DATABASE_URL=sqlite+aiosqlite:///./bcn.db
   RABBITMQ_URL=amqp://guest:guest@localhost:5672/
   SECRET_KEY=supersecretjwtkey
   ```
4. **Initialize** the database:

   ```bash
   python init_db.py
   ```
5. **Start RabbitMQ** (ensure RabbitMQ service is running and UI at `http://localhost:15672` is accessible).
6. **Launch the consumer** (Terminal 1):

   ```bash
   python -m app.consumer.event_consumer
   ```
7. **Launch the API** (Terminal 2):

   ```bash
   uvicorn app.main:app --reload
   ```

Once both are running, the API is available at `http://localhost:8000` and the consumer will process incoming events from RabbitMQ.

---

### 🐳 With Docker Compose

1. **Ensure Docker Desktop** is running on your machine.

2. **Build & start** all services:

   ```bash
   docker compose up --build
   ```

3. The following containers will start:

   * **api**: FastAPI app + consumer (on port 8000)
   * **rabbitmq**: RabbitMQ broker + management UI (ports 5672 & 15672)

4. **Verify**:

   * API: `http://localhost:8000`
   * Swagger UI: `http://localhost:8000/docs`
   * RabbitMQ UI: `http://localhost:15672` (guest/guest)

To stop, press `Ctrl+C` in the terminal and/or run:

```bash
docker compose down
```

---

## ⚙ Configuration

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=sqlite+aiosqlite:///./bcn.db
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
SECRET_KEY=supersecretjwtkey
```

* **DATABASE\_URL**: SQLAlchemy connect string for SQLite
* **RABBITMQ\_URL**: AMQP URL for RabbitMQ
* **SECRET\_KEY**: JWT signing secret

---

## 🗄️ Database Initialization

Run the init script to (re)create `bcn.db`:

```bash
python init_db.py
```

Confirms tables for `orders` and `users` are created.

---

## 🔄 Running the Services

### 1. Consumer

```bash
. .venv/Scripts/activate
python -m app.consumer.event_consumer
```

Console shows:

```
▶️ Consumer up; waiting for messages.
```

### 2. API

```bash
. .venv/Scripts/activate
uvicorn app.main:app --reload
```

FastAPI runs at `http://127.0.0.1:8000` and `/docs` for Swagger.

---

## 📡 API Endpoints

### Authentication

* **POST** `/auth/signup` — Create a new user
* **POST** `/auth/token` — Obtain JWT token (form data: `username`, `password`)

### Event Ingestion

* **POST** `/events` — Publish order event to message queue

  ```json
  {
    "vendor_id": "V001",
    "order_id": "ORD123",
    "items": [
      {"sku":"SKU1","qty":2,"unit_price":120},
      {"sku":"SKU2","qty":1,"unit_price":50}
    ],
    "timestamp":"2025-07-20T12:00:00.000Z"
  }
  ```

### Vendor Metrics

* **GET** `/metrics?vendor_id=V001` (Bearer token) →

  ```json
  {
    "vendor_id":"V001",
    "total_orders":10,
    "total_revenue":2500,
    "high_value_orders":2,
    "anomalous_orders":0,
    "last_7_days_volume": {"2025-07-14":3, ...}
  }
  ```

### Chart Visualization

* **GET** `/metrics/chart?vendor_id=V001` (Bearer token) →

  ```json
  {
    "vendor_id":"V001",
    "chart_base64":"<long Base64 string>"
  }
  ```

---

## 🖼️ Decoding Base64 Charts

Paste the `chart_base64` string into an online Base64→PNG tool (e.g. [https://base64.guru/converter/decode/image/png](https://base64.guru/converter/decode/image/png)) to view.

---

## 🧹 Cleaning Git History

If you accidentally committed ignored files:

```bash
git rm -r --cached .
git add . .gitignore
git commit -m "chore: clean up tracked files"
```
---
