from enum import Enum

class ArticleStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_PUBLISH = "PENDING_PUBLISH"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    ERROR = "ERROR"
