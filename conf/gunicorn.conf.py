import json

# Networking & Module
bind = "0.0.0.0:8000"
wsgi_app = "fala.wsgi:application"

# Worker & Process Management
workers = 4
master = True  # Gunicorn always uses a master process by default
max_requests = 5000
max_requests_jitter = 50  # Recommended when using max_requests to break synchronization

# Timeouts & Buffering
timeout = 30  # Equivalent to harakiri
# Note: Gunicorn doesn't have an exact match for post-buffering or buffer-size
# at the application level; this is typically handled by an upstream reverse proxy like Nginx.

# Lifecycle
preload_app = False  # uWSGI default behavior is to lazy-load per worker
wsgi_lazy_fetch = True

# Logging Configuration
# Gunicorn uses standard  string formatting for logs.
access_log_format = json.dumps(
    {
        "process_name": "gunicorn",
        "timestamp_msec": "%(L)s",  # Request time in milliseconds (as string)
        "method": "%(m)s",  # HTTP method
        "uri": "%(U)s?%(q)s",  # URL path + query string
        "proto": "%(H)s",  # Protocol
        "status": "%(s)s",  # Status code (string/integer depending on parser)
        "referer": "%(f)s",  # Referer
        "user_agent": "%(a)s",  # User Agent
        "remote_addr": "%(h)s",  # Remote address
        "http_host": "%({Host}i)s",  # Host header
        "pid": "%(p)s",  # Process ID
        "rq_size": "%(b)s",  # Response length (Gunicorn doesn't natively track request body size in format strings)
        "rs_time_ms": "%(D)s",  # Request runtime in microseconds
        "rs_size": "%(B)s",  # Response body length
    }
)

# Direct logs to stdout
accesslog = "-"
errorlog = "-"
