<script setup>
import {ref, computed} from 'vue'

// כך רכיב מצהיר שהוא מוכן לקבל נתונים מבחוץ. כאן הוא מצפה לקבל מערך (Array) בשם "mice"
const props = defineProps
({
  mice: Array
})

const sortOrder = ref(null)

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
      </tr>
    </thead>
    <tbody>
      <tr v-for="mouse in displayedMice" :key="mouse.id">
        <td>{{ mouse.brand }}</td>
        <td>{{ mouse.model }}</td>
        <td>{{ mouse.weight_grams }}</td>
        <td>{{ mouse.grip_style }}</td>
        <td>{{ mouse.sensor }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
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