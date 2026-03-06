<script setup>
import { ref, computed, onMounted } from 'vue'

const mice = ref([])
const searchQuery = ref('')
const selectedMice = ref([])

const alignOption = ref('center')

const arenaColors = ['#00e5ff', '#ffea00', '#ff00ff', '#00ff00', '#ff4757', '#ffa502', '#7bed9f']

const fetchMice = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/mice')
    const data = await response.json()
    mice.value = data.sort((a, b) => (a.brand + a.model).localeCompare(b.brand + b.model))
  } catch (error) {
    console.error('Error fetching mice:', error)
  }
}

onMounted(() => {
  fetchMice()
})

const searchResults = computed(() => {
  if (!searchQuery.value.trim()) return []
  const query = searchQuery.value.toLowerCase()
  return mice.value.filter(m =>
    (m.brand + ' ' + m.model).toLowerCase().includes(query) &&
    !selectedMice.value.find(selected => selected.id === m.id)
  ).slice(0, 15)
})

const addMouseToArena = (mouse) => {
  if (selectedMice.value.length < arenaColors.length) {
    selectedMice.value.push(mouse)
    searchQuery.value = ''
  } else {
    alert('Arena is full! Remove a mouse before adding a new one.')
  }
}

const removeMouseFromArena = (mouseId) => {
  selectedMice.value = selectedMice.value.filter(m => m.id !== mouseId)
}

const PIXELS_PER_MM = 3.5

const getTopViewStyle = (mouse) => {
  const widthPx = (mouse.width || 60) * PIXELS_PER_MM
  const heightPx = (mouse.length || 120) * PIXELS_PER_MM

  let style = {
    width: `${widthPx}px`,
    height: `${heightPx}px`,
    left: '50%',
    transform: 'translateX(-50%)'
  }

  if (alignOption.value === 'center') {
    style.top = '50%'
    style.transform = 'translate(-50%, -50%)'
  } else if (alignOption.value === 'back') {
    style.bottom = '20px'
  } else if (alignOption.value === 'front') {
    style.top = '20px'
  }

  return style
}

const getSideViewStyle = (mouse) => {
  const widthPx = (mouse.length || 120) * PIXELS_PER_MM
  const heightPx = (mouse.height || 40) * PIXELS_PER_MM

  let style = {
    width: `${widthPx}px`,
    height: `${heightPx}px`,
    bottom: '20px'
  }

  if (alignOption.value === 'center') {
    style.left = '50%'
    style.transform = 'translateX(-50%)'
  } else if (alignOption.value === 'back') {
    style.left = '20px'
  } else if (alignOption.value === 'front') {
    style.right = '20px'
  }

  return style
}
</script>

<template>
  <div class="compare-container">
    <h2 class="arena-title">Shape Comparison Arena</h2>

    <div class="search-section">
      <div class="search-wrapper">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="🔍 Search for a mouse to add (e.g., Logitech Superstrike)..."
          class="arena-search-input"
        />
        <ul v-if="searchResults.length > 0" class="search-dropdown">
          <li v-for="m in searchResults" :key="m.id" @click="addMouseToArena(m)">
            <span class="plus-icon">➕</span> {{ m.brand }} {{ m.model }}
          </li>
        </ul>
      </div>
    </div>

    <div class="selected-mice-panel" v-if="selectedMice.length > 0">
      <div
        v-for="(mouse, index) in selectedMice"
        :key="mouse.id"
        class="mouse-card"
        :style="{ borderTopColor: arenaColors[index] }"
      >
        <button class="remove-btn" @click="removeMouseFromArena(mouse.id)">❌</button>
        <div class="color-indicator" :style="{ backgroundColor: arenaColors[index] }"></div>
        <h4>{{ mouse.brand }} {{ mouse.model }}</h4>
        <p>{{ mouse.length }} × {{ mouse.width }} × {{ mouse.height }} mm</p>
        <p>{{ mouse.weight_grams }}g</p>
      </div>
    </div>

    <div class="alignment-toolbar" v-if="selectedMice.length > 0">
      <span class="toolbar-label">Align Shapes By:</span>
      <button :class="{ active: alignOption === 'front' }" @click="alignOption = 'front'">Front (Fingertips)</button>
      <button :class="{ active: alignOption === 'center' }" @click="alignOption = 'center'">Center (Sensor)</button>
      <button :class="{ active: alignOption === 'back' }" @click="alignOption = 'back'">Back (Palm)</button>
    </div>

    <div class="arena-board" v-if="selectedMice.length > 0">

      <div class="view-panel">
        <h3>Top View</h3>
        <div class="svg-wrapper top-view-wrapper">
          <div
            v-for="(mouse, index) in selectedMice"
            :key="'top-' + mouse.id"
            v-html="mouse.shape_top"
            class="svg-layer"
            :style="[{ '--svg-color': arenaColors[index] }, getTopViewStyle(mouse)]"
          ></div>
        </div>
      </div>

      <div class="view-panel">
        <h3>Side View</h3>
        <div class="svg-wrapper side-view-wrapper">
          <div
            v-for="(mouse, index) in selectedMice"
            :key="'side-' + mouse.id"
            v-html="mouse.shape_side"
            class="svg-layer"
            :style="[{ '--svg-color': arenaColors[index] }, getSideViewStyle(mouse)]"
          ></div>
        </div>
      </div>

    </div>

    <div v-else class="empty-arena">
      <p>The arena is empty! Search and add mice above to compare their shapes.</p>
    </div>
  </div>
</template>

<style scoped>
.compare-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.arena-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
}

.search-section {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.search-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.arena-search-input {
  width: 100%;
  padding: 15px 20px;
  font-size: 1.1rem;
  border: 2px solid #485460;
  border-radius: 30px;
  background-color: #1e272e;
  color: white;
  outline: none;
  transition: border-color 0.3s;
}

.arena-search-input:focus {
  border-color: #00e5ff;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #2d3436;
  border: 1px solid #485460;
  border-radius: 8px;
  margin-top: 5px;
  padding: 0;
  list-style: none;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

.search-dropdown li {
  padding: 12px 20px;
  color: #d2dae2;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #3d4448;
}

.search-dropdown li:hover {
  background-color: #353b48;
  color: #00e5ff;
}

.plus-icon {
  font-size: 0.8rem;
}

.selected-mice-panel {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
}

.mouse-card {
  position: relative;
  background-color: #1e272e;
  padding: 15px 25px;
  border-radius: 8px;
  border-top: 4px solid;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  color: white;
  text-align: center;
  min-width: 200px;
}

.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.remove-btn:hover {
  opacity: 1;
}

.color-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin: 0 auto 10px auto;
}

.mouse-card h4 {
  margin: 0 0 5px 0;
  font-size: 1rem;
}

.mouse-card p {
  margin: 2px 0;
  font-size: 0.85rem;
  color: #808e9b;
}

.alignment-toolbar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
  background-color: #f1f2f6;
  padding: 15px;
  border-radius: 8px;
}

.toolbar-label {
  font-weight: bold;
  color: #2f3542;
}

.alignment-toolbar button {
  padding: 8px 16px;
  border: 2px solid #ced6e0;
  background-color: white;
  color: #2f3542;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}

.alignment-toolbar button:hover {
  border-color: #a4b0be;
}

.alignment-toolbar button.active {
  background-color: #2f3542;
  color: white;
  border-color: #2f3542;
}

.arena-board {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 40px;
  background-color: #111418;
  padding: 40px;
  border-radius: 12px;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
}

.view-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.view-panel h3 {
  color: #bdc3c7;
  margin-bottom: 20px;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.svg-wrapper {
  position: relative;
  width: 400px;
  height: 600px;
  /* העפנו מכאן את ה-border dashed שהיה קודם */
}

.side-view-wrapper {
  height: 300px;
}

.svg-layer {
  position: absolute;
  pointer-events: none;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

:deep(.svg-layer svg) {
  width: 100%;
  height: 100%;
  display: block;
  overflow: visible;
}

:deep(.svg-layer svg path) {
  stroke: var(--svg-color) !important;
  stroke-width: 2px !important;
  fill: none !important;
}

.empty-arena {
  text-align: center;
  padding: 50px;
  font-size: 1.2rem;
  color: #7f8c8d;
  background-color: #f8f9fa;
  border-radius: 12px;
}
</style>