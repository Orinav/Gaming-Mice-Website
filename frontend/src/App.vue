<script setup>
import { ref, computed } from 'vue'
import MiceTable from './components/MiceTable.vue'
import CheckboxFilter from './components/CheckboxFilter.vue'
import SelectFilter from './components/SelectFilter.vue'

const miceList = ref([])
const selectedBrands = ref([])
const selectedSensors = ref([])
const selectedGrip = ref('')
const searchQuery = ref('')

// --- פילטר משקל חדש ---
const minWeight = ref(0)
const maxWeight = ref(150) // נקבע ברירת מחדל גבוהה כדי להציג הכל בהתחלה

const gripOptions = [
  { text: 'Claw', value: 'claw' },
  { text: 'Fingertip', value: 'fingertip' },
  { text: 'Palm', value: 'palm' }
]

const fetchMice = async () => {
  const response = await fetch('http://127.0.0.1:5000/api/mice')
  miceList.value = await response.json()
}

const resetFilters = () => {
  selectedBrands.value = []
  selectedSensors.value = []
  selectedGrip.value = ''
  searchQuery.value = ''
  minWeight.value = 0
  maxWeight.value = 150 // איפוס גם של המשקל
}

const availableBrands = computed(() => [...new Set(miceList.value.map(mouse => mouse.brand))])
const availableSensors = computed(() => [...new Set(miceList.value.map(mouse => mouse.sensor))])

const filteredMice = computed(() => {
  return miceList.value.filter(mouse => {
    const matchBrand = selectedBrands.value.length === 0 || selectedBrands.value.includes(mouse.brand)
    const matchSensor = selectedSensors.value.length === 0 || selectedSensors.value.includes(mouse.sensor)
    const matchGrip = selectedGrip.value === '' || mouse.grip_style.toLowerCase().includes(selectedGrip.value.toLowerCase())

    const query = searchQuery.value.toLowerCase()
    const matchSearch = mouse.brand.toLowerCase().includes(query) ||
                        mouse.model.toLowerCase().includes(query)

    // --- לוגיקת סינון המשקל ---
    const matchWeight = mouse.weight_grams >= minWeight.value && mouse.weight_grams <= maxWeight.value

    return matchBrand && matchSensor && matchGrip && matchSearch && matchWeight
  })
})

fetchMice()

// אובייקט לאגירת הנתונים מהטופס
const newMouse = ref({
  brand: '',
  model: '',
  weight_grams: 0,
  grip_style: '',
  sensor: '',
  image_url: '',
  buy_url: ''
})

// פונקציה לשליחת עכבר חדש ל-Backend
const addMouse = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/mice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newMouse.value)
    })

    if (response.ok) {
      fetchMice() // רענון הטבלה כדי לראות את העכבר החדש
      // איפוס הטופס
      newMouse.value = { brand: '', model: '', weight_grams: 0, grip_style: '', sensor: '', image_url: '', buy_url: '' }
    }
  } catch (error) {
    console.error("Error adding mouse:", error)
  }
}

// פונקציה למחיקת עכבר
const deleteMouse = async (id) => {
  if (confirm("Are you sure you want to delete this mouse?")) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/mice/${id}`, {
        method: 'DELETE'
      })
      if (response.ok) fetchMice()
    } catch (error) {
      console.error("Error deleting mouse:", error)
    }
  }
}
</script>

<template>
  <div class="content">
    <div class="header-section">
      <h1>Gaming Mice Comparator</h1>
      <div class="search-area">
        <input
          v-model="searchQuery"
          placeholder="Search model or brand..."
          class="search-input"
        >
        <button @click="resetFilters" class="reset-btn">Clear All</button>
      </div>
    </div>

    <div class="admin-panel">
      <h3>Add New Mouse (Admin Panel)</h3>
      <div class="add-form">
        <input v-model="newMouse.brand" placeholder="Brand">
        <input v-model="newMouse.model" placeholder="Model">
        <input v-model.number="newMouse.weight_grams" type="number" placeholder="Weight (g)">
        <input v-model="newMouse.grip_style" placeholder="Grip Style">
        <input v-model="newMouse.sensor" placeholder="Sensor">
        <input v-model="newMouse.image_url" placeholder="Image Path (e.g. /images/...)">
        <input v-model="newMouse.buy_url" placeholder="Buy Link">
        <button @click="addMouse" class="add-btn">Add Mouse</button>
      </div>
    </div>

    <div class="filters-container">
      <CheckboxFilter
        title="Filter by Brand:"
        :options="availableBrands"
        v-model="selectedBrands"
      />

      <CheckboxFilter
        title="Filter by Sensor:"
        :options="availableSensors"
        v-model="selectedSensors"
      />

      <SelectFilter
        title="Filter by Grip Style:"
        defaultLabel="All Grips"
        :options="gripOptions"
        v-model="selectedGrip"
      />

      <div class="filter-group">
        <h3>Weight Range (g):</h3>
        <div class="weight-inputs">
          <input type="number" v-model.number="minWeight" class="small-num-input">
          <span>to</span>
          <input type="number" v-model.number="maxWeight" class="small-num-input">
        </div>
        <input
          type="range"
          v-model.number="maxWeight"
          min="0"
          max="150"
          class="weight-slider"
        >
      </div>
    </div>

    <div v-if="filteredMice.length > 0">
      <MiceTable
        :mice="filteredMice"
        @delete-mouse="deleteMouse"
      />
    </div>
    <div v-else class="no-results">
      <p>No mice match your search criteria.</p>
    </div>
  </div>
</template>

<style>
* { box-sizing: border-box; }
body { font-family: Calibri, sans-serif; margin: 0; background: silver; }

.search-input {
    padding: 10px;
    width: 250px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-right: 10px;
}
.search-area {
    display: flex;
    align-items: center;
}

.content {
    max-width: 1000px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    min-height: 100vh;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.filters-container {
    background: #f9f9f9;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 40px;
}

.reset-btn {
    padding: 10px 15px;
    background-color: #ff4d4d;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}

.reset-btn:hover { background-color: #cc0000; }

.no-results {
    text-align: center;
    padding: 40px;
    background: #fdf2f2;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    color: #721c24;
    font-size: 18px;
}

.weight-inputs {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
}

.input-box {
    display: flex;
    flex-direction: column;
}

.input-box label {
    font-size: 12px;
    color: #666;
}

.input-box input {
    width: 60px;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.weight-slider {
    width: 100%;
    cursor: pointer;
    accent-color: #42b883; /* צבע הירוק של Vue */
}

.slider-hint {
    font-size: 12px;
    margin-top: 5px;
    color: #42b883;
    font-weight: bold;
}

.admin-panel {
    background: #f0f0f0;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 1px dashed #999;
}

.add-form {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.add-form input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    flex: 1;
    min-width: 120px;
}

.add-btn {
    background-color: #42b883;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}

.delete-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 18px;
    transition: transform 0.2s;
}

.delete-btn:hover {
    transform: scale(1.2);
}
</style>