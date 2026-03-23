import requests
import json
from pathlib import Path

class RegionManager:
    def __init__(self):
        self.location = self._detect_location()
        self.units = self._determine_units()
        self.language = self._determine_language()
        self.compliance = self._get_compliance_rules()

    def _detect_location(self):
        # Use free IP geolocation API
        try:
            resp = requests.get("https://ipinfo.io/json", timeout=5)
            data = resp.json()
            return {
                "country": data.get("country", "US"),
                "city": data.get("city", "Unknown"),
                "region": data.get("region", ""),
                "timezone": data.get("timezone", "UTC")
            }
        except:
            return {"country": "US", "city": "Unknown", "region": "", "timezone": "UTC"}

    def _determine_units(self):
        # Metric for most countries except US, Liberia, Myanmar
        us_like = ["US", "LR", "MM"]
        if self.location["country"] in us_like:
            return "imperial"
        return "metric"

    def _determine_language(self):
        # Simple mapping for now; can be extended
        lang_map = {
            "ZA": "en-ZA",  # South Africa
            "US": "en-US",
            "GB": "en-GB",
            "FR": "fr",
            "DE": "de",
            # ...
        }
        return lang_map.get(self.location["country"], "en-US")

    def _get_compliance_rules(self):
        # POPIA for ZA, GDPR for EU, etc.
        country = self.location["country"]
        rules = {}
        if country == "ZA":
            rules["data_residency"] = "local"
            rules["popia"] = True
        elif country in ["DE", "FR", "ES", "IT", "NL", "BE", "PL", "SE", "FI", "DK", "IE", "PT", "AT", "LU", "EE", "LV", "LT", "CZ", "SK", "SI", "HR", "HU", "RO", "BG", "CY", "MT"]:
            rules["gdpr"] = True
            rules["data_residency"] = "eu"
        elif country == "US":
            rules["ccpa"] = True
        return rules

    def get_region(self):
        return f"{self.location['city']}, {self.location['region']}, {self.location['country']}"

    def get_units(self):
        return self.units

    def get_language(self):
        return self.language

    def get_compliance(self):
        return self.compliance
