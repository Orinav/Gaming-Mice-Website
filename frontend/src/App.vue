<script setup>
import { ref, computed } from 'vue'
import MiceTable from './components/MiceTable.vue'
import CheckboxFilter from './components/CheckboxFilter.vue'
import SelectFilter from './components/SelectFilter.vue'

const miceList = ref([])
const selectedBrands = ref([])
const selectedSensors = ref([])
const selectedGrip = ref('')

// הגדרת האפשרויות לתפריט הנפתח (text זה מה שרואים, value זה מה ששומרים)
const gripOptions = [
  { text: 'Claw', value: 'claw' },
  { text: 'Fingertip', value: 'fingertip' },
  { text: 'Palm', value: 'palm' }
]

const fetchMice = async () =>
{
  const response = await fetch('http://127.0.0.1:5000/api/mice')
  miceList.value = await response.json()
}

const availableBrands = computed(() => [...new Set(miceList.value.map(mouse => mouse.brand))])
const availableSensors = computed(() => [...new Set(miceList.value.map(mouse => mouse.sensor))])

const filteredMice = computed(() =>
{
  return miceList.value.filter(mouse =>
  {
    const matchBrand = selectedBrands.value.length === 0 || selectedBrands.value.includes(mouse.brand)
    const matchSensor = selectedSensors.value.length === 0 || selectedSensors.value.includes(mouse.sensor)
    const matchGrip = selectedGrip.value === '' || mouse.grip_style.toLowerCase().includes(selectedGrip.value.toLowerCase())

    return matchBrand && matchSensor && matchGrip
  })
})

fetchMice()
</script>

<template>
  <div class="content">
    <h1>Gaming Mice Comparator</h1>

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

    </div>

    <MiceTable :mice="filteredMice" />

  </div>
</template>

<style>
* {
    box-sizing: border-box;
}

body {
    font-family: Calibri, sans-serif;
    margin: 0;
    background: silver;
}

.content {
    max-width: 1000px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    min-height: 100vh;
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
</style>