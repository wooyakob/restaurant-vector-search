import os
import json
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

input_path = os.getenv("INPUT_PATH")  # ca-eateries.json file path
output_path = os.getenv("OUTPUT_PATH")  # location to save updated restaurants with embeddings

with open(input_path, "r", encoding="utf-8") as f:
    restaurants = json.load(f)

updated_restaurants = []

for restaurant in restaurants:
    name = restaurant.get("name", "").strip()
    content = restaurant.get("content", "").strip()
    
    
    if not name:
        print("Skipping restaurant with missing name.")
        continue

    combined_text = f"Name: {name}\nContent: {content}"
    embedding_vector = embeddings_model.embed_documents([combined_text])[0]
    restaurant["embedding"] = embedding_vector
    updated_restaurants.append(restaurant)
    
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(updated_restaurants, f, indent=4)

print(f"Embeddings generated and saved to: {output_path}")