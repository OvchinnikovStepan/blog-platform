from kombu import Queue

broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/0"

task_queues = (
    Queue("moderation.queue"),
    Queue("preview.queue"),
    Queue("publish.queue"),
    Queue("notify.queue"),
    Queue("dlq.queue"),
)

task_default_queue = "celery"

broker_connection_retry_on_startup = True
task_acks_late = True
task_reject_on_worker_lost = True
