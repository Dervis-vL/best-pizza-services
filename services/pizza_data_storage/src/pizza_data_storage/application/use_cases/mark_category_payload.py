"""Mark a staged category payload as consumed or failed use case."""

from pizza_data_storage.application import ports


class MarkCategoryPayloadAsConsumedUseCase:  # pylint: disable=too-few-public-methods
    """Mark a staged category payload as consumed."""

    def __init__(self, payload_repository: ports.ICategoryPayloadRepository) -> None:
        """Initialize the use case."""
        self._payload_repository = payload_repository

    def execute(self, payload_id: int) -> bool:
        """Execute the use case."""
        self._payload_repository.mark_consumed(payload_id=payload_id)
        return True


class MarkCategoryPayloadAsFailedUseCase:  # pylint: disable=too-few-public-methods
    """Mark a staged category payload as failed."""

    def __init__(self, payload_repository: ports.ICategoryPayloadRepository) -> None:
        """Initialize the use case."""
        self._payload_repository = payload_repository

    def execute(self, payload_id: int) -> bool:
        """Execute the use case."""
        self._payload_repository.mark_failed(payload_id=payload_id)
        return True
