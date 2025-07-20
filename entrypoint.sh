#!/bin/sh
python -m app.consumer.event_consumer &
uvicorn app.main:app --host 0.0.0.0 --port 8000 