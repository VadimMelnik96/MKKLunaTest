from dataclasses import dataclass


@dataclass
class GatewayResult:
    """Результат из шлюза"""
    success: bool
    error_message: str | None = None
