import multiprocessing
import os


# Tính toán worker an toàn hơn
def get_workers():
    # Ưu tiên biến môi trường, nếu không có mới tính toán
    default_workers = multiprocessing.cpu_count() * 2 + 1
    # Giới hạn trần để tránh crash container trên máy chủ lớn
    return int(os.getenv("GUNICORN_WORKERS", min(default_workers, 8)))


bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = get_workers()
worker_class = "gthread"
threads = int(os.getenv("GUNICORN_THREADS", 4))

# Performance
max_requests = 2000
max_requests_jitter = 200
timeout = int(os.getenv("GUNICORN_TIMEOUT", 60))
graceful_timeout = 30
keepalive = 2  # Giảm một chút để ALB quản lý tốt hơn
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
capture_output = True
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")
access_log_format = (
    '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
