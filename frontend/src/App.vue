<template>
  <div>
    <ImageUploader @files-selected="uploadFiles" />
    <SearchBar @search="handleSearch" />
    <ImageList :images="filteredImages" />
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
    const res = await axios.get('http://localhost:8000/images_list')
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

function handleSearch(query) {
  searchQuery.value = query
}

const filteredImages = computed(() => {
  if (!searchQuery.value) return results.value
  return results.value.filter(img =>
    img.url.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(() => loadImages())
</script>
