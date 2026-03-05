<script setup>
import { ref, computed, onMounted } from 'vue'
import CheckboxFilter from './components/CheckboxFilter.vue'
// שים לב: מחקנו מכאן את הייבוא של SelectFilter כי כבר אין לנו Grip!

const mice = ref([])
const favorites = ref([])
const searchQuery = ref('')
const maxWeight = ref(150)

const selectedBrands = ref([])
const selectedSensors = ref([])

// משיכת נתונים משרת הפלאסק
const fetchMice = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/mice')
    mice.value = await response.json()
  } catch (error) {
    console.error('Error fetching mice:', error)
  }
}

// משיכת מועדפים
const fetchFavorites = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/favorites')
    const data = await response.json()
    favorites.value = data.map(fav => fav.id)
  } catch (error) {
    console.error('Error fetching favorites:', error)
  }
}

onMounted(() => {
  fetchMice()
  fetchFavorites()
})

// יצירת רשימות ייחודיות לפילטרים (ללא Grip)
const uniqueBrands = computed(() => {
  const brands = mice.value.map(m => m.brand).filter(b => b && b !== 'Unknown')
  return [...new Set(brands)].sort()
})

const uniqueSensors = computed(() => {
  const sensors = mice.value.map(m => m.sensor).filter(s => s && s !== 'Unknown')
  return [...new Set(sensors)].sort()
})

// סינון העכברים
const filteredMice = computed(() => {
  return mice.value.filter(mouse => {
    const matchesSearch = mouse.model.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          mouse.brand.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesBrand = selectedBrands.value.length === 0 || selectedBrands.value.includes(mouse.brand)
    const matchesSensor = selectedSensors.value.length === 0 || selectedSensors.value.includes(mouse.sensor)
    const matchesWeight = mouse.weight_grams <= maxWeight.value

    return matchesSearch && matchesBrand && matchesSensor && matchesWeight
  })
})

const clearAll = () => {
  searchQuery.value = ''
  selectedBrands.value = []
  selectedSensors.value = []
  maxWeight.value = 150
}

const toggleFavorite = async (mouseId) => {
  const isFav = favorites.value.includes(mouseId)
  try {
    if (isFav) {
      await fetch(`http://127.0.0.1:5000/api/favorites/${mouseId}`, { method: 'DELETE' })
      favorites.value = favorites.value.filter(id => id !== mouseId)
    } else {
      await fetch('http://127.0.0.1:5000/api/favorites', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mouse_id: mouseId })
      })
      favorites.value.push(mouseId)
    }
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
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
      <h1>Gaming Mice Comparator</h1>
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

      <div class="filter-group">
        <h3>Weight Range</h3>
        <input type="range" v-model="maxWeight" min="0" max="150" />
        <p>0g - {{ maxWeight }}g</p>
      </div>
    </div>

    <table class="mice-table">
      <thead>
        <tr>
          <th>Fav</th>
          <th>Image</th>
          <th>Brand</th>
          <th>Model</th>
          <th>Weight (g)</th>
          <th>Sensor</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mouse in filteredMice" :key="mouse.id">
          <td>
            <button class="fav-btn" @click="toggleFavorite(mouse.id)">
              <span v-if="favorites.includes(mouse.id)">❤️</span>
              <span v-else>🤍</span>
            </button>
          </td>
          <td><img :src="mouse.image_url" alt="Mouse image" class="mouse-img" v-if="mouse.image_url"/></td>
          <td>{{ mouse.brand }}</td>
          <td>{{ mouse.model }}</td>
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

<style>
/* איפוס רקע כללי של האתר למראה נקי */
body {
  background-color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 20px;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* אזור הכותרת וחיפוש */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  margin: 0;
  font-size: 2rem;
}

.search-bar {
  display: flex;
  gap: 15px;
}

.search-bar input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 250px;
  font-size: 1rem;
}

.clear-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.clear-btn:hover {
  background-color: #ff3333;
}

/* אזור הפילטרים */
.filters-section {
  display: flex;
  justify-content: flex-start;
  gap: 50px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border: 1px solid #eaeaea;
}

.filter-group h3 {
  margin-top: 0;
  font-size: 1rem;
  margin-bottom: 15px;
}

/* עיצוב הטבלה */
.mice-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
}

.mice-table th, .mice-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eaeaea;
}

.mice-table th {
  font-weight: bold;
  font-size: 0.95rem;
}

/* הגבלת גודל התמונות (מה שהשתגע קודם) */
.mouse-img {
  max-width: 50px;
  max-height: 70px;
  object-fit: contain;
}

/* כפתורי פעולות */
.fav-btn, .delete-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 5px;
}

.fav-btn:hover, .delete-btn:hover {
  transform: scale(1.1);
}
</style>