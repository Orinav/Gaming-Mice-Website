<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import CheckboxFilter from '../components/CheckboxFilter.vue'

const mice = ref([])
const searchQuery = ref('')

const minWeight = ref(0)
const maxWeight = ref(150)
const minLength = ref(0)
const maxLength = ref(150)

const selectedBrands = ref([])
const selectedSensors = ref([])

const sortKey = ref('')
const sortOrder = ref(1)

watch(minWeight, (newVal) => { if (newVal > maxWeight.value) minWeight.value = maxWeight.value })
watch(maxWeight, (newVal) => { if (newVal < minWeight.value) maxWeight.value = minWeight.value })

watch(minLength, (newVal) => { if (newVal > maxLength.value) minLength.value = maxLength.value })
watch(maxLength, (newVal) => { if (newVal < minLength.value) maxLength.value = minLength.value })

const fetchMice = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/mice')
    mice.value = await response.json()
  } catch (error) {
    console.error('Error fetching mice:', error)
  }
}

onMounted(() => {
  fetchMice()
})

const uniqueBrands = computed(() => {
  const brands = mice.value.map(m => m.brand).filter(b => b && b !== 'Unknown')
  return [...new Set(brands)].sort()
})

const uniqueSensors = computed(() => {
  const relevantMice = selectedBrands.value.length > 0
    ? mice.value.filter(m => selectedBrands.value.includes(m.brand))
    : mice.value
  const sensors = relevantMice.map(m => m.sensor).filter(s => s && s !== 'Unknown')
  return [...new Set(sensors)].sort()
})

watch(uniqueSensors, (newValidSensors) => {
  selectedSensors.value = selectedSensors.value.filter(sensor => newValidSensors.includes(sensor))
})

const sortBy = (key) => {
  if (sortKey.value === key) {
    if (sortOrder.value === 1) {
      sortOrder.value = -1
    } else {
      sortKey.value = ''
      sortOrder.value = 1
    }
  } else {
    sortKey.value = key
    sortOrder.value = 1
  }
}

const filteredMice = computed(() => {
  let result = mice.value.filter(mouse => {
    const matchesSearch = mouse.model.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          mouse.brand.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesBrand = selectedBrands.value.length === 0 || selectedBrands.value.includes(mouse.brand)
    const matchesSensor = selectedSensors.value.length === 0 || selectedSensors.value.includes(mouse.sensor)

    const matchesWeight = mouse.weight_grams >= minWeight.value && mouse.weight_grams <= maxWeight.value
    const matchesLength = mouse.length >= minLength.value && mouse.length <= maxLength.value

    return matchesSearch && matchesBrand && matchesSensor && matchesWeight && matchesLength
  })

  if (sortKey.value) {
    result = result.sort((a, b) => {
      let aVal = a[sortKey.value]
      let bVal = b[sortKey.value]

      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return (aVal - bVal) * sortOrder.value
      }

      aVal = aVal ? String(aVal).toLowerCase() : ''
      bVal = bVal ? String(bVal).toLowerCase() : ''
      return aVal.localeCompare(bVal) * sortOrder.value
    })
  }

  return result
})

const clearAll = () => {
  searchQuery.value = ''
  selectedBrands.value = []
  selectedSensors.value = []
  minWeight.value = 0
  maxWeight.value = 150
  minLength.value = 0
  maxLength.value = 150
  sortKey.value = ''
  sortOrder.value = 1
}

const deleteMouse = async (mouseId) => {
  try {
    await fetch(`http://127.0.0.1:5000/api/mice/${mouseId}`, { method: 'DELETE' })
    mice.value = mice.value.filter(m => m.id !== mouseId)
  } catch (error) {
    console.error('Error deleting mouse:', error)
  }
}
</script>

<template>
  <div class="container">
    <header class="header">
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Search..." />
        <button @click="clearAll" class="clear-btn">Clear All</button>
      </div>
    </header>

    <div class="filters-section">
      <div class="filter-group">
        <h3>Brands</h3>
        <CheckboxFilter :options="uniqueBrands" v-model="selectedBrands" />
      </div>

      <div class="filter-group">
        <h3>Sensors</h3>
        <CheckboxFilter :options="uniqueSensors" v-model="selectedSensors" />
      </div>

      <div class="filter-group sliders-group">
        <div class="slider-container">
          <h3>Weight Range</h3>
          <div class="dual-slider">
            <div class="slider-row">
              <span class="slider-label">Min</span>
              <input type="range" v-model.number="minWeight" min="0" max="150" />
            </div>
            <div class="slider-row">
              <span class="slider-label">Max</span>
              <input type="range" v-model.number="maxWeight" min="0" max="150" />
            </div>
          </div>
          <p class="range-display">{{ minWeight }}g - {{ maxWeight }}g</p>
        </div>

        <div class="slider-container">
          <h3>Length Range</h3>
          <div class="dual-slider">
            <div class="slider-row">
              <span class="slider-label">Min</span>
              <input type="range" v-model.number="minLength" min="0" max="150" />
            </div>
            <div class="slider-row">
              <span class="slider-label">Max</span>
              <input type="range" v-model.number="maxLength" min="0" max="150" />
            </div>
          </div>
          <p class="range-display">{{ minLength }}mm - {{ maxLength }}mm</p>
        </div>
      </div>
    </div>

    <table class="mice-table">
      <thead>
        <tr>
          <th>Image</th>

          <th @click="sortBy('brand')" class="sortable-header" title="Click to sort">
            Brand
            <span v-if="sortKey === 'brand'" class="sort-arrow">{{ sortOrder === 1 ? '▲' : '▼' }}</span>
          </th>

          <th @click="sortBy('model')" class="sortable-header" title="Click to sort">
            Model
            <span v-if="sortKey === 'model'" class="sort-arrow">{{ sortOrder === 1 ? '▲' : '▼' }}</span>
          </th>

          <th @click="sortBy('length')" class="sortable-header" title="Click to sort by Length">
            Dimensions (L×W×H)
            <span v-if="sortKey === 'length'" class="sort-arrow">{{ sortOrder === 1 ? '▲' : '▼' }}</span>
          </th>

          <th @click="sortBy('weight_grams')" class="sortable-header" title="Click to sort by Weight">
            Weight (g)
            <span v-if="sortKey === 'weight_grams'" class="sort-arrow">{{ sortOrder === 1 ? '▲' : '▼' }}</span>
          </th>

          <th>Sensor</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mouse in filteredMice" :key="mouse.id">
          <td>
            <img
              :src="mouse.image_url"
              class="mouse-img"
              v-if="mouse.image_url"
              loading="lazy"
              alt="Mouse Image"
            />
          </td>
          <td>{{ mouse.brand }}</td>
          <td>{{ mouse.model }}</td>
          <td>{{ mouse.length }} × {{ mouse.width }} × {{ mouse.height }}</td>
          <td>{{ mouse.weight_grams }}</td>
          <td>{{ mouse.sensor }}</td>
          <td>
            <button class="delete-btn" @click="deleteMouse(mouse.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
  margin-bottom: 30px;
}

.search-bar {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 600px;
}

.search-bar input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.clear-btn {
  padding: 10px 20px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.clear-btn:hover {
  background-color: #ff6b81;
}

.filters-section {
  display: flex;
  justify-content: space-between;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.filter-group {
  flex: 1;
  padding: 0 15px;
}

.sliders-group {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.slider-container h3 {
  margin-top: 0;
  color: #2f3542;
  border-bottom: 2px solid #eccc68;
  padding-bottom: 5px;
  display: inline-block;
  margin-bottom: 15px;
}

.dual-slider {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slider-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.slider-label {
  width: 35px;
  font-size: 0.85rem;
  font-weight: bold;
  color: #747d8c;
}

.slider-row input[type="range"] {
  flex: 1;
  cursor: pointer;
}

.range-display {
  margin: 15px 0 0 0;
  font-size: 1rem;
  font-weight: bold;
  color: #2f3542;
  text-align: center;
  background-color: #f1f2f6;
  padding: 5px;
  border-radius: 4px;
}

.filter-group h3 {
  margin-top: 0;
  color: #2f3542;
  border-bottom: 2px solid #eccc68;
  padding-bottom: 5px;
  display: inline-block;
}

.mice-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.mice-table th, .mice-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #f1f2f6;
}

.mice-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2f3542;
  user-select: none;
}

.sortable-header {
  cursor: pointer;
  transition: background-color 0.2s;
}

.sortable-header:hover {
  background-color: #e2e6ea;
}

.sort-arrow {
  display: inline-block;
  margin-left: 5px;
  font-size: 0.8rem;
  color: #ff4757;
}

.mice-table tr:hover {
  background-color: #f1f2f6;
}

.mouse-img {
  max-width: 80px;
  max-height: 80px;
  object-fit: contain;
}

.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  transition: transform 0.2s;
}

.delete-btn:hover {
  transform: scale(1.2);
}
</style>