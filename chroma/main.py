import chromadb
from chromadb.config import Settings

CHROMA_HOST = "chroma-prd.apps-prd"
CHROMA_PORT = 80 
COLLECTION_NAME = "your_collection_name"

print(f"Connecting to Chroma at http://{CHROMA_HOST}:{CHROMA_PORT}...")

try:
    client = chromadb.HttpClient(
        host=CHROMA_HOST, 
        port=CHROMA_PORT
    )
    print(f"✅ Connected successfully. Heartbeat: {client.heartbeat()}")
except Exception as e:
    print(f"❌ Failed to connect to ChromaDB: {e}")
    exit(1)

try:
    collection = client.get_collection(name=COLLECTION_NAME)
    print(f"✅ Successfully retrieved collection: '{COLLECTION_NAME}'")
    print(f"📊 Total documents in collection: {collection.count()}")
except Exception as e:
    print(f"❌ Could not retrieve collection '{COLLECTION_NAME}': {e}")
    print("\nAvailable collections in this instance:")
    try:
        collections = client.list_collections()
        for c in collections:
            print(f" - {c.name}")
    except Exception as list_e:
        print(f"Failed to list collections: {list_e}")
    exit(1)

test_query = "What is sustainable agriculture?"

print(f"\n🔍 Querying collection for: '{test_query}'")
try:
    results = collection.query(
        query_texts=[test_query],
        n_results=3, # Number of nearest neighbors to return
        # where={"source": "k8s-docs"}, # Optional: filter by metadata
    )
    
    print("\n📋 Query Results:")
    print("=" * 40)
    print(f"IDs:        {results.get('ids')}")
    print(f"Distances:  {results.get('distances')}")
    print(f"Metadata:   {results.get('metadatas')}")
    print(f"Documents:  {results.get('documents')}")

except Exception as e:
    print(f"❌ Failed to query collection: {e}")