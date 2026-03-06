import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

workers = int(
    os.getenv(
        "GUNICORN_WORKERS",
        multiprocessing.cpu_count() * 2 + 1
    )
)

worker_class = "gthread"
threads = int(os.getenv("GUNICORN_THREADS", 4))

max_requests = 2000
max_requests_jitter = 200

timeout = int(os.getenv("GUNICORN_TIMEOUT", 60))
graceful_timeout = 30
keepalive = 5

preload_app = True

accesslog = "-"
errorlog = "-"
capture_output = True

loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")