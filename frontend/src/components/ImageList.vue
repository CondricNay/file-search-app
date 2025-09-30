<template>
  <div class="results">
    <div v-for="img in images" :key="img.id" class="result-item">
      <img :src="`http://localhost:8000${img.url}`" class="result-img" />
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
}
.result-img {
  width: 100%;
  display: block;
}
</style>
