<script setup>
import {ref, computed} from 'vue'

// כך רכיב מצהיר שהוא מוכן לקבל נתונים מבחוץ. כאן הוא מצפה לקבל מערך (Array) בשם "mice"
const props = defineProps
({
  mice: Array
})

const sortOrder = ref(null)
const emit = defineEmits(['delete-mouse'])

const toggleWeightSort = () =>
{
  if (sortOrder.value === null)
    sortOrder.value = 'asc'
  else if (sortOrder.value === 'asc')
    sortOrder.value = 'desc'
  else
    sortOrder.value = null
}

const displayedMice = computed(() =>
{
  let result = [...props.mice]

  if (sortOrder.value === 'asc')
    result.sort((a, b) => a.weight_grams - b.weight_grams)
  else if (sortOrder.value === 'desc')
    result.sort((a, b) => b.weight_grams - a.weight_grams)

  return result
})
</script>

<template>
  <table>
    <thead>
      <tr>
        <th>Image</th>
        <th>Brand</th>
        <th>Model</th>
        <th @click="toggleWeightSort" class="sortable-header">
          Weight (g)
          <span v-if="sortOrder === 'asc'">🔼</span>
          <span v-else-if="sortOrder === 'desc'">🔽</span>
          <span v-else>↕️</span>
        </th>
        <th>Grip Style</th>
        <th>Sensor</th>
        <th>Mouse Link</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="mouse in displayedMice" :key="mouse.id">
        <td>
          <img :src="mouse.image_url" :alt="mouse.model" class="mouse-thumb">
        </td>
        <td>{{ mouse.brand }}</td>
        <td>{{ mouse.model }}</td>
        <td>{{ mouse.weight_grams }}</td>
        <td>{{ mouse.grip_style }}</td>
        <td>{{ mouse.sensor }}</td>
        <td>
          <a :href="mouse.buy_url" target="_blank" class="buy-btn">Check Price</a>
        </td>
        <td>
          <button @click="$emit('delete-mouse', mouse.id)" class="delete-btn" title="Delete Mouse">
            🗑️
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.buy-btn {
    display: inline-block;
    padding: 6px 12px;
    background-color: #42b883;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 13px;
    font-weight: bold;
    text-align: center;
}
.buy-btn:hover {
    background-color: #33996a;
}

.mouse-thumb {
    width: 50px;
    height: auto;
    display: block;
    margin: 0 auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

th {
    background-color: #eee;
}

.sortable-header {
    cursor: pointer;
    user-select: none;
}

.sortable-header:hover {
    background-color: #ddd;
}
</style>