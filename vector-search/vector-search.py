# run vector search from CLI using Couchbase Python SDK

import os
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, SearchOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
import couchbase.search as search
from couchbase.vector_search import VectorQuery, VectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

question = "a sushi restaurant with a tasting menu"
#"a luxury american diner that serves hamburgers"

embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector = embeddings_model.embed_query(question)

# show embeddings of search query
# print("Generated embedding vector:", vector)

pa = PasswordAuthenticator(os.getenv("CB_USERNAME"), os.getenv("CB_PASSWORD"))
cluster = Cluster(os.getenv("CB_HOSTNAME"), ClusterOptions(pa))

bucket = cluster.bucket("restaurants")
scope = bucket.scope("california")

search_index = "ca-eateries-index"

try:
    search_req = search.SearchRequest.create(search.MatchNoneQuery()).with_vector_search(
        VectorSearch.from_vector_query(VectorQuery('embedding', vector, num_candidates=2))
    )
    
    result = scope.search(search_index,
                           search_req,
                           SearchOptions(limit=13, fields=["name","content", "embedding"])
                           )
    
    for row in result.rows():
        print("Found row: {}".format(row))
    
    print("Reported total rows: {}".format(result.metadata().metrics().total_rows()))
except CouchbaseException as ex:
    import traceback
    traceback.print_exc()