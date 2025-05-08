import os
import json
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

# Initialize the embeddings model
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

input_path = os.getenv("INPUT_PATH")  # ca-eateries.json file path
output_path = os.getenv("OUTPUT_PATH")  # location to save updated restaurants with embeddings

# Load the restaurant data
with open(input_path, "r", encoding="utf-8") as f:
    restaurants = json.load(f)

updated_restaurants = []

# Process each restaurant: combine name and content, generate embedding, and add as field
for restaurant in restaurants:
    name = restaurant.get("name", "").strip()
    content = restaurant.get("content", "").strip()
    
    # If the name is empty, we skip it to avoid later issues
    if not name:
        print("Skipping restaurant with missing name.")
        continue

    combined_text = f"Name: {name}\nContent: {content}"
    embedding_vector = embeddings_model.embed_documents([combined_text])[0]
    restaurant["embedding"] = embedding_vector
    updated_restaurants.append(restaurant)
    
# Write the updated restaurants (each now with an embedding field) to output file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(updated_restaurants, f, indent=4)

print(f"Embeddings generated and saved to: {output_path}")