import os
import uvicorn

from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from embeddings import encode_image, encode_text
from milvus_init import create_client, init_milvus_database

# Config
IMAGE_FOLDER = "image_folder"
COLLECTION_NAME = "image_collection"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Init FastAPI
app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Milvus
milvus_client = create_client()
init_milvus_database(milvus_client)


@app.get("/")
def root():
    return {"message": "API is running"}

# Upload (save + insert into Milvus)
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    path = os.path.join(IMAGE_FOLDER, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())

    # also insert embedding into Milvus
    vector = encode_image(path)
    milvus_client.insert(COLLECTION_NAME, [{"vector": vector, "filepath": path}])

    return {"filename": file.filename, "url": f"/images/{file.filename}"}

# List all images
@app.get("/images")
def list_images():
    files = [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith(('.png','.jpg','.jpeg','.gif'))]
    return [{"id": f, "url": f"/images/{f}"} for f in files]


# Serve single image
@app.get("/images/{filename}")
def get_image(filename: str):
    path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404)
    return FileResponse(path)

# Delete (file + remove from Milvus)
@app.delete("/images/{filename}")
def delete_image(filename: str):
    filepath = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Image not found")

    filepath = filepath.replace("\\", "/")
    milvus_client.delete(COLLECTION_NAME, filter=f'filepath == "{filepath}"')
    os.remove(filepath)

    return {"message": "Image deleted successfully"}


# Search (text → embeddings → top-k)
@app.post("/search")
async def search_images(req: Request):
    data = await req.json()
    query_text = data.get("query_text", "")

    vector = encode_text(query_text)
    results = milvus_client.search(
        COLLECTION_NAME,
        data=[vector],
        limit=10,
        output_fields=["filepath"]
    )

    return [
        {"id": os.path.basename(hit['entity']['filepath']),
        "url": f"/images/{os.path.basename(hit['entity']['filepath'])}"}
        for r in results
        for hit in r
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)