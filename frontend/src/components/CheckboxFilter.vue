<script setup>
import { computed } from 'vue'

const props = defineProps
({
  title: String,
  options: Array,
  modelValue: Array
})

// אנחנו מגדירים שהרכיב הזה יודע "לצעוק" לאבא כשמשהו משתנה
const emit = defineEmits(['update:modelValue'])

const selectedValues = computed
({
  get: () => props.modelValue,
  set: (newValue) => emit('update:modelValue', newValue)
})
</script>

<template>
  <div class="filter-group">
    <h3>{{ title }}</h3>
    <div class="checkbox-group">
      <label v-for="option in options" :key="option">
        <input type="checkbox" :value="option" v-model="selectedValues">
        {{ option }}
      </label>
    </div>
  </div>
</template>

<style scoped>

.filter-group h3
{
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
    color: #333;
}

.checkbox-group
{
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.checkbox-group label
{
    cursor: pointer;
    user-select: none;
    font-size: 15px;
}
</style>