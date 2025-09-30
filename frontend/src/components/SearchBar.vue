<template>
  <input
    type="text"
    v-model="query"
    placeholder="Search images..."
    class="search-input"
  />
</template>

<script setup>
import { defineEmits, ref, watch } from 'vue'

const emit = defineEmits(['search'])
const query = ref('')

// Notify parent whenever the query changes
watch(query, (val) => emit('search', val))
</script>

<style scoped>
.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
}
</style>
