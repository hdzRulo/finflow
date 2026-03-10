"""Bank detector placeholder utilities."""


class BankDetector:
    """Identify bank based on extracted logos/keywords/header patterns."""

    def detect(self, text: str) -> str:
        lowered = text.lower()
        if "example bank a" in lowered or "a-bank" in lowered:
            return "ExampleBankA"
        if "example bank b" in lowered or "b-bank" in lowered:
            return "ExampleBankB"
        return "unknown"
