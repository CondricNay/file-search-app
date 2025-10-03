<template>
  <div>
    <ImageUploader @files-selected="uploadFiles" />
    <SearchBar @search="handleSearch" />
    <ImageList :images="filteredImages" @delete-image="deleteImage" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import SearchBar from './components/SearchBar.vue'
import ImageList from './components/ImageList.vue'
import ImageUploader from './components/ImageUploader.vue'

const results = ref([])
const searchQuery = ref('')

async function loadImages() {
  try {
    const res = await axios.get('http://localhost:8000/images')
    results.value = res.data
  } catch (err) {
    console.error('Failed to load images:', err)
  }
}

async function uploadFiles(files) {
  for (const file of files) {
    const formData = new FormData()
    formData.append('file', file)
    try {
      await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } catch (err) {
      console.error('Upload failed:', err)
    }
  }
  await loadImages() // refresh after upload
}

async function handleSearch(query) {
  if (!query) {
    searchQuery.value = ''
    results.value = await axios.get('http://localhost:8000/images').then(r => r.data)
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/search', {
      query_text: query,
      top_k: 10
    })
    // Milvus search returns [{id, url}] -> Convert to unique set
    const image_set = [...new Map(res.data.map(img => [img.id, img])).values()]
    results.value = image_set;
    searchQuery.value = query
  } catch (err) {
    console.error('Search failed:', err)
  }
}

async function deleteImage(id) {
  try {
    await axios.delete(`http://localhost:8000/images/${id}`);
    await loadImages(); // refresh the images after deletion
  } catch (err) {
    console.error('Failed to delete image:', err);
  }
}

const filteredImages = computed(() => results.value)

onMounted(() => loadImages())
</script>
