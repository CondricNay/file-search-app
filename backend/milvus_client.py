import os

import clip
import matplotlib.pyplot as plt

from PIL import Image
from pymilvus import MilvusClient

model_name = "ViT-B/32"
model, preprocess = clip.load(model_name)
model.eval()

def encode_image(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0)
    image_features = model.encode_image(image)
    image_features /= image_features.norm(
        dim=-1, keepdim=True
    )  # Normalize the image features
    return image_features.squeeze().tolist()


def encode_text(text):
    text_tokens = clip.tokenize(text)
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(
        dim=-1, keepdim=True
    )  # Normalize the text features
    return text_features.squeeze().tolist()


collection_name = "image_collection"

milvus_client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus",
)

# Drop the collection if it already exists
if milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)

# Create a new collection in quickstart mode
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=512,  # this should match the dimension of the image embedding
    auto_id=True,  # auto generate id and store in the id field
    enable_dynamic_field=True,  # enable dynamic field for scalar fields
)


image_dir = "./image_folder"
raw_data = []
image_paths = []

for file in os.listdir(image_dir):
    if file.lower().endswith((".jpg", ".jpeg")):
        image_paths.append(os.path.join(image_dir, file))

print(image_paths)

for image_path in image_paths:
    image_embedding = encode_image(image_path)
    image_dict = {"vector": image_embedding, "filepath": image_path}
    raw_data.append(image_dict)

insert_result = milvus_client.insert(collection_name=collection_name, data=raw_data)

print("Inserted", insert_result["insert_count"], "images into Milvus.")

query_text = "flying"
query_embedding = encode_text(query_text)

search_results = milvus_client.search(
    collection_name=collection_name,
    data=[query_embedding],
    limit=10,  # return top 10 results
    output_fields=["filepath"],  # return the filepath field
)


width = 150 * 5
height = 150 * 2
concatenated_image = Image.new("RGB", (width, height))

result_images = []
for result in search_results:
    for hit in result:
        filename = hit["entity"]["filepath"]
        img = Image.open(filename)
        img = img.resize((150, 150))
        result_images.append(img)

for idx, img in enumerate(result_images):
    x = idx % 5
    y = idx // 5
    concatenated_image.paste(img, (x * 150, y * 150))

print(f"Query text: {query_text}")
print("\nSearch results:")

# show the concatenated image with matplotlib
plt.imshow(concatenated_image)
plt.axis("off")
plt.show()
