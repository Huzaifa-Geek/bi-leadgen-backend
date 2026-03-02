from serpapi import GoogleSearch
from typing import List, Dict


class SerpAPIScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_page(self, city: str, industry: str, page: int = 0) -> List[Dict]:
        params = {
            "engine": "google_maps",
            "q": f"{industry} {city}",
            "hl": "en",
            "start": page * 20,
            "api_key": self.api_key
        }

        try:
            search = GoogleSearch(params)
            data = search.get_dict()
            raw_results = data.get("local_results", [])

            processed = []
            for b in raw_results:
                processed.append({
                    "place_id": b.get("place_id"),
                    "name": b.get("title", "N/A"),
                    "rating": b.get("rating"),
                    "reviews": b.get("reviews"),
                    "address": b.get("address", "N/A"),
                    "phone": b.get("phone", "N/A"),
                    "website": b.get("website", "N/A"),
                    "city": city,
                    "industry": industry,
                    "email": None
                })
            return processed

        except Exception as e:
            print(f"Scraper Error: {e}")
            return []


    def fetch_place_details(self, place_id: str) -> Dict:
        params = {
            "engine": "google_maps",
            "place_id": place_id,
            "hl": "en",
            "api_key": self.api_key
        }

        try:
            search = GoogleSearch(params)
            data = search.get_dict()
            result = data.get("place_results", {})

            return {
                "rating": result.get("rating"),
                "reviews": result.get("reviews"),
                "website": result.get("website"),
                "phone": result.get("phone"),
                "address": result.get("address"),
                "description": result.get("description"),
            }

        except Exception as e:
            print(f"Place details error: {e}")
            return {}