import os
from pymilvus import MilvusClient

from embeddings import encode_image

# -------------------------------
# Milvus Init at startup
# -------------------------------
IMAGE_FOLDER = "image_folder"
COLLECTION_NAME = "image_collection"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


def create_client():
    milvus_client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")
    return milvus_client

def init_milvus_database(milvus_client=None):
    if not milvus_client:
        milvus_client = create_client()

    if milvus_client.has_collection(COLLECTION_NAME):
        milvus_client.drop_collection(COLLECTION_NAME)

    milvus_client.create_collection(
        collection_name=COLLECTION_NAME,
        dimension=512,  # must match embedding dim
        auto_id=True,
        enable_dynamic_field=True,
    )

    # Insert all existing local images
    raw_data = []
    for file in os.listdir(IMAGE_FOLDER):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            path = os.path.join(IMAGE_FOLDER, file)
            vector = encode_image(path)
            raw_data.append({"vector": vector, "filepath": path})

    if raw_data:
        insert_result = milvus_client.insert(COLLECTION_NAME, data=raw_data)
        print("Inserted", insert_result["insert_count"], "images into Milvus.")