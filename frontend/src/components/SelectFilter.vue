<script setup>
import { computed } from 'vue'

const props = defineProps
({
  title: String,
  defaultLabel: String, // למשל: "All Grips"
  options: Array,       // מערך של אובייקטים: [{ text: 'Claw', value: 'claw' }]
  modelValue: String    // הערך שנבחר
})

// העובד מגדיר איזה "צעקות" הוא יודע לצעוק למנהל
const emit = defineEmits(['update:modelValue'])

// ה-v-model הפנימי שלנו שמנהל את התקשורת מול המנהל
const selectedValue = computed({
  get: () => props.modelValue, // קורא את מה שהמנהל אמר
  set: (newValue) => emit('update:modelValue', newValue) // צועק למנהל כשמשנים בחירה
})
</script>

<template>
  <div class="filter-group">
    <h3>{{ title }}</h3>
    <select v-model="selectedValue" class="grip-select">
      <option value="">{{ defaultLabel }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.filter-group h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
    color: #333;
}

.grip-select {
    padding: 8px;
    font-size: 14px;
    font-family: inherit;
    border-radius: 4px;
    border: 1px solid #ccc;
}
</style>