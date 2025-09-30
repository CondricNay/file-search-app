<template>
  <div class="results">
    <div v-for="img in images" :key="img.id" class="result-item">
      <div class="img-wrapper">
        <img :src="`http://localhost:8000${img.url}`" class="result-img" />
        <button class="delete-btn" @click="$emit('delete-image', img.id)">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  images: Array
})
</script>

<style scoped>
.results {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.result-item {
  width: 150px;
  position: relative;
}
.img-wrapper {
  position: relative;
}
.result-img {
  width: 100%;
  display: block;
  border-radius: 4px;
}
.delete-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  background: red;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
  font-weight: bold;
  line-height: 18px;
  text-align: center;
  padding: 0;
}
.delete-btn:hover {
  background: darkred;
}
</style>
