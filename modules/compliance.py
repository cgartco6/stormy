import json
from pathlib import Path

class ComplianceManager:
    def __init__(self, region_manager):
        self.region = region_manager
        self.consent_file = Path.home() / ".stormy" / "consent.json"
        self.consent = self.load_consent()

    def load_consent(self):
        if self.consent_file.exists():
            with open(self.consent_file) as f:
                return json.load(f)
        return {
            "data_collection": False,
            "voice_recording": False,
            "location_sharing": False
        }

    def save_consent(self):
        self.consent_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.consent_file, "w") as f:
            json.dump(self.consent, f)

    def request_consent(self, feature):
        rules = self.region.get_compliance()
        # If in GDPR/POPIA, consent must be explicit
        if rules.get("gdpr") or rules.get("popia"):
            # Return a prompt to ask user
            return f"To enable {feature}, I need your consent. Do you agree? (yes/no)"
        # Otherwise, assume opt-in
        return True

    def delete_user_data(self):
        # Delete all user data from memory, logs, etc.
        # Implement as needed
        pass
