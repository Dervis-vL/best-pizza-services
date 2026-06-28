"""Settings level module imports."""

from pizza_worker.settings.worker import WorkerSettings

worker = WorkerSettings()

__all__ = ["WorkerSettings"]
