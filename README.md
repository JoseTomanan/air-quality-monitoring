# Air quality monitoring
This is the web app interface for smart air quality monitoring system.
Made in compliance with CS 145 project requirement, IoT cup (semester 2425B).

## To install prerequisites:
```bash
pip install -r requirements.txt
```

## To run the server:
```bash
cd app
uvicorn main:app  # default
uvicorn main:app --reload  # to enable hot reloading
```

## To test the endpoints:
```
https://localhost:8000/docs
```
