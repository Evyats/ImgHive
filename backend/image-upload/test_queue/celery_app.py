from celery import Celery
import time

app = Celery(
    "demo",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@app.task
def add(x, y):
    print(f"Running add({x}, {y})")
    time.sleep(1)
    return x + y
