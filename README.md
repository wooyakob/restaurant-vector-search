# California Restaurant Finder
This web app demonstrates vector search for restaurants in California stored in Couchbase Capella. It extracts restaurant data from the Landmark collection (via a SQL++ query in `ca-eateries.sql`), generates embeddings using a sentence-transformer model, and performs semantic search using dot product similarity.

![Search Bar](restaurant-vector-search/search-bar.png)
![Search Results](restaurant-vector-search/search-results.png)
![Restaurant Discovered](restaurant-vector-search/restaurant-discovered.png)

## Overview
### Data Source
- Extracts restaurant data from the preloaded travel-sample dataset.
- Uses the Landmark collection.

### Embedding Generation
- Combines restaurant names and descriptions into a single text string.
- Converts text into a 384-dimensional vector using the `all-MiniLM-L6-v2` model.
- Embeddings are generated using [`gen-embeddings.py`](vector-search/gen-embeddings.py) and stored in `ca-eateries-embedding.json`.

### Vector Search
- Performs semantic search using dot product similarity between query and restaurant embeddings.
- A large positive dot product indicates a high degree of similarity.
- A value close to zero indicates orthogonal (dissimilar) embeddings.
- To output similarity scores to the console with Couchbase's Python SDK, run [`vector-search.py`](vector-search/vector-search.py).

### Google Maps
- **Reverse Geocoding:** Converts latitude/longitude into a human-readable address.
- **Map Embed:** Dynamically embeds maps within the search results to visually locate restaurants.

## Architecture
### Data Preparation
1. Run `ca-eateries.sql` against the Landmark collection in Couchbase Capella to generate `ca-eateries.json`.
2. Import `ca-eateries.json` into the `ca-eateries` collection.
3. Combine the restaurant's name and description for generating embeddings.

### Embedding Generation
- Use [`gen-embeddings.py`](vector-search/) along with the `all-MiniLM-L6-v2` model.
- Output is stored in `ca-eateries-embedding.json`.

### Search Indexing
- Create a fulltext search index in Couchbase Capella.
- Can import index in Capella [`restaurants.california.ca-eateries-index.json`](vector-index/).

### Web App
- Provides a client-side search interface.
- Displays restaurant details and embedded maps.
- Dynamically fetches and displays the total number of restaurants from an API endpoint.
- Links to restaurant websites to easily book a restaurant you discover.

## Setup
### Environment Variables
Create a `.env` file and set values in `.env.example`

Will need to setup an Open AI and Google Maps API key separately.

### Running the App
In restaurant-web-app directory:
```sh
python3 -m app.main
```

### Index and Collection Setup
- Import the JSON data files into the designated Couchbase collections.
- Follow Couchbase documentation to create the required search indexes.

## Usage

### Search Interface
- Open the web app in your browser.
- Use the search input to describe your dream restaurant.

### Result Display
- Shows details such as name, description, address, phone, price, and website.
- If available, shows an embedded map of the restaurant's location.
- Returns the three most relevant results using dot product similarity. 