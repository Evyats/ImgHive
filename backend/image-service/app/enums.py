from enum import Enum


class Status(str, Enum):
    queued = "queued"
    processing = "processing"
    done = "done"
    failed = "failed"