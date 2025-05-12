import os
import requests
from urllib.parse import quote_plus
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, SearchOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
import couchbase.search as search
from couchbase.vector_search import VectorQuery, VectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

class RestaurantSearch:
    def __init__(self):
        load_dotenv()
        self.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.pa = PasswordAuthenticator(os.getenv("CB_USERNAME"), os.getenv("CB_PASSWORD"))
        self.cluster = Cluster(os.getenv("CB_HOSTNAME"), ClusterOptions(self.pa))
        self.bucket = self.cluster.bucket("restaurants")
        self.scope = self.bucket.scope("california")
        self.search_index = "ca-eateries-index"

    def search_restaurants(self, question):
        vector = self.embeddings_model.embed_query(question)
        try:
            search_req = search.SearchRequest.create(search.MatchNoneQuery()).with_vector_search(
                VectorSearch.from_vector_query(VectorQuery('embedding', vector, num_candidates=3))
            )
            result = self.scope.search(
                self.search_index,
                search_req,
                SearchOptions(limit=13, fields=["name", "content", "phone", "price", "url", "geo.lat", "geo.lon"])
            )
            rows = result.rows()
            filtered_results = []
            
            gmaps_key = os.getenv("GMAPS_API_KEY")
            for row in rows:
                lat = row.fields.get("geo.lat")
                lon = row.fields.get("geo.lon")
                print("Processing row - lat:", lat, "lon:", lon)

                address = None
                embedUrl = None
                if lat is not None and lon is not None and gmaps_key:
                    reverse_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={gmaps_key}"
                    print("Calling reverse geocode API:", reverse_url) 
                    try:
                        resp = requests.get(reverse_url)
                        print("API response status:", resp.status_code) 
                        if resp.status_code == 200:
                            geo_data = resp.json()
                            print("Reverse geocode response:", geo_data) 
                            if geo_data.get("results"):
                                address = geo_data["results"][0].get("formatted_address")
                                embedUrl = f"https://www.google.com/maps/embed/v1/place?key={gmaps_key}&q={quote_plus(address)}"
                    except Exception as e:
                        print(f"Reverse geocoding error: {e}")
                filtered_results.append({
                    "name": row.fields.get("name"),
                    "content": row.fields.get("content"),
                    "phone": row.fields.get("phone"),
                    "price": row.fields.get("price"),
                    "url": row.fields.get("url"),
                    "location": {
                        "lat": lat,
                        "lon": lon,
                        "address": address,
                        "embedUrl": embedUrl
                    }
                })
            return filtered_results
        except CouchbaseException as ex:
            print(f"An error occurred: {ex}")
            return []