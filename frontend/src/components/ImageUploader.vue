<template>
  <div
    class="upload-area"
    @dragover.prevent
    @drop.prevent="handleDrop"
    @click="triggerFileInput"
  >
    Drag & Drop Images Here or Click to Upload
    <input
      type="file"
      ref="fileInput"
      multiple
      accept="image/*"
      @change="handleFileSelect"
      style="display: none"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['files-selected'])
const fileInput = ref(null)

function triggerFileInput() {
  fileInput.value.click()
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files)
  emit('files-selected', files)
  event.target.value = null
}

function handleDrop(event) {
  const files = Array.from(event.dataTransfer.files)
  emit('files-selected', files)
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed #888;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  color: #555;
}
.upload-area:hover {
  background: #f0f0f0;
}
</style>
