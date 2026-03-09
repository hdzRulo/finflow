"""Bank detector placeholder utilities."""


class BankDetector:
    """Identify bank based on extracted logos/keywords/header patterns."""

    def detect(self, text: str) -> str:
        if "example bank a" in text.lower():
            return "ExampleBankA"
        if "example bank b" in text.lower():
            return "ExampleBankB"
        return "unknown"
