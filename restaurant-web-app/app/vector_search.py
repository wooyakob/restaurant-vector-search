import os
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
                #VectorSearch.from_vector_query(VectorQuery('embedding', vector, num_candidates=3))
                # Return the top match determined by dot product similarity score
                VectorSearch.from_vector_query(VectorQuery('embedding', vector, num_candidates=1))
            )
            result = self.scope.search(self.search_index,
                                       search_req,
                                       SearchOptions(limit=13, fields=["name", "content", "embedding"]))
            rows = result.rows()
            filtered_results = []
            for row in rows:
                filtered_results.append({
                    "name": row.fields.get("name"),
                    "content": row.fields.get("content")
                })
            return filtered_results
        except CouchbaseException as ex:
            print(f"An error occurred: {ex}")
            return []