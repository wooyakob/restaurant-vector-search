from flask import Flask, render_template, request, jsonify
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
import os

from app.vector_search import RestaurantSearch

app = Flask(__name__)

pa = PasswordAuthenticator(os.getenv("CB_USERNAME"), os.getenv("CB_PASSWORD"))
cluster = Cluster(os.getenv("CB_HOSTNAME"), ClusterOptions(pa))

search_client = RestaurantSearch()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form.get("query")
        rows = search_client.search_restaurants(question)
        return jsonify({
            "results": rows
        })
    return render_template("index.html")

@app.route("/api/restaurant_count", methods=["GET"])
def restaurant_count():
    query = '''
      SELECT COUNT(*) AS total_restaurants
      FROM `restaurants`.`california`.`vector` AS v
      WHERE 
          v.name IS NOT NULL AND
          v.content IS NOT NULL AND
          v.price IS NOT NULL AND
          v.url IS NOT NULL AND
          v.geo IS NOT NULL AND
          v.phone IS NOT NULL;
    '''
    result = cluster.query(query)
    count_row = list(result.rows())[0]
    return jsonify(count=count_row["total_restaurants"])


if __name__ == "__main__":
    app.run(debug=True)