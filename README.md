# 📂 Image Search App

An end-to-end **image upload and search application** built with:

- **Vue 3** – Frontend (drag & drop upload, search bar, image list, delete)  
- **FastAPI** – Backend (REST API for upload, search, delete)  
- **Milvus** – Vector database for image embeddings and similarity search  
- **Axios** – API communication between frontend and backend  

This app allows you to **upload images, search similar images by text query, and delete images** from the database.

---

## 🚀 Features

- 🖼️ **Drag & drop or click-to-upload** images  
- 🔍 **Text-based search** with Milvus vector similarity search  
- 🗑️ **Delete images** from database and storage  
- 📋 **Image listing** with automatic refresh after upload/search/delete  
- ⚡ FastAPI backend + Vue 3 frontend  

---

## 📦 Tech Stack

- **Frontend:** Vue 3, Axios  
- **Backend:** FastAPI (Python)  
- **Database:** Milvus (vector search)  
- **Others:** Pymilvus, uvicorn, Python 3.10+  

---

## ⚙️ Installation

### 1. Clone the repository

    git clone https://github.com/your-username/image-search-app.git
    cd image-search-app

### 2. Backend setup (FastAPI + Milvus)

    cd backend
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

Run the backend server:

    uvicorn main:app --reload --host 0.0.0.0 --port 8000

This will start the API at [http://localhost:8000](http://localhost:8000).

### 3. Frontend setup (Vue 3)

    cd frontend
    npm install
    npm run dev

This will start the Vue app at [http://localhost:5173](http://localhost:5173) (default Vite port).

---

## 🔑 API Endpoints

| Method   | Endpoint           | Description                      |
|----------|--------------------|----------------------------------|
| `GET`    | `/images`          | Get all uploaded images          |
| `POST`   | `/upload`          | Upload a new image               |
| `POST`   | `/search`          | Search images by text query      |
| `DELETE` | `/images/{id}`     | Delete an image by ID            |

---

## 🖥️ Usage

1. Open the frontend in your browser (`http://localhost:5173`).  
2. Drag & drop images or click to upload.  
3. Use the search bar to find similar images.  
4. Delete images by clicking the ❌ button.  

---

## 🛠️ Development Notes

- Uploaded images are stored in a folder on the backend (`image_folder/`).  
- Metadata and embeddings are stored in **Milvus**.  
- Make sure Milvus is running before starting the backend.  

To start Milvus (Docker example):

    docker run -d --name milvus-standalone \
      -p 19530:19530 \
      -p 9091:9091 \
      milvusdb/milvus:latest

---
