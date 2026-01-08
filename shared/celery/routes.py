from shared.celery.tasks import (
    MODERATE_POST,
    GENERATE_PREVIEW,
    PUBLISH_POST,
    NOTIFY_FOLLOWERS,
)

task_routes = {
    MODERATE_POST: {"queue": "moderation.queue"},
    GENERATE_PREVIEW: {"queue": "preview.queue"},
    PUBLISH_POST: {"queue": "publish.queue"},
    NOTIFY_FOLLOWERS: {"queue": "notify.queue"}
}
