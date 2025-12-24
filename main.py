from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


print(client.get_collections().model_dump().get("collections")[0].get("name"))
print(type(client.get_collections()))

# delete collection if exists
if "my_first_collection" == client.get_collections().model_dump().get("collections")[0].get("name"):
     client.delete_collection(collection_name="my_first_collection")

# Define the collection name
collection_name = "my_first_collection"

# Create the collection with specified vector size and distance metric
client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=4,
        distance=models.Distance.COSINE
        )
)

# Retrieve and display the list of collections
collections = client.get_collections()
print("Existing Collections:", collections)

# Defiine the vectors to be inserted
points = [
    models.PointStruct(
        id=1,
        vector=[0.1, 0.2, 0.3, 0.4],
        payload={"category": "example"}
        ),
    models.PointStruct(
        id=2,
        vector=[0.2, 0.3, 0.4, 0.5],
        payload={"category": "demo"}
    )

]

# Insert the vectors into the collection
client.upsert(
    collection_name=collection_name,
    points=points
)


# retrieve collection details
collection_info = client.get_collection(collection_name=collection_name)
print("Collection Info:", collection_info)


# Perform a vector search
query_vector = [0.08, 0.14, 0.33, 0.28]

search_results = client.query_points(
    collection_name=collection_name,
    query= query_vector,
    limit=1
)

print("Search Results:", search_results)