"""Layout detector placeholder."""


class LayoutDetector:
    """Detect if statement layout is table, line, or mixed."""

    def detect(self, payload: dict) -> str:
        if payload.get("tables"):
            return "table"
        return "line"
