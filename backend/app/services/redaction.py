import re

class RedactionService:
    def __init__(self):
        self.email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        self.phone_regex = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
        self.upi_regex = re.compile(r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}")
        self.card_regex = re.compile(r"\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}")
        self.address_keywords = [
            "layout", "street", "road", "apartment", "society", "nagar", "sector", "colony", 
            "phase", "floor", "building", "cross", "main", "bangalore", "bengaluru"
        ]

    def redact(self, text: str) -> str:
        if not text:
            return ""
        redacted = text
        redacted = self.email_regex.sub("[EMAIL_REDACTED]", redacted)
        redacted = self.phone_regex.sub("[PHONE_REDACTED]", redacted)
        redacted = self.upi_regex.sub("[UPI_REDACTED]", redacted)
        redacted = self.card_regex.sub("[CARD_REDACTED]", redacted)
        for keyword in self.address_keywords:
            pattern = re.compile(rf"\d+\s+[^.!?]*{keyword}[^.!?]*\d*", re.IGNORECASE)
            redacted = pattern.sub("[ADDRESS_REDACTED]", redacted)
        return redacted
