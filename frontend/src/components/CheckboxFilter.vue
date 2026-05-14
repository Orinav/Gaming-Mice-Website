<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  options: Array,
  modelValue: Array
})

const emit = defineEmits(['update:modelValue'])

const searchQuery = ref('')

const filteredOptions = computed(() => {
  const query = searchQuery.value.toLowerCase()
  if (!query) return props.options
  return props.options.filter(option =>
    option.toLowerCase().includes(query) || props.modelValue.includes(option)
  )
})

watch(() => props.modelValue, (newVal) => {
  if (newVal.length === 0) searchQuery.value = ''
})

function onCheckboxChange(option, isChecked)
{
  const newValue = [...props.modelValue]

  if (isChecked)
  {
    newValue.push(option)
  }
  else
  {
    const index = newValue.indexOf(option)
    newValue.splice(index, 1)
  }
  emit('update:modelValue', newValue)
}
</script>

<template>
  <div class="checkbox-filter">
    <input
      v-model="searchQuery"
      type="text"
      class="filter-search"
      placeholder="Search..."
    />
    <label v-for="option in filteredOptions" :key="option" class="checkbox-label">
      <input
        type="checkbox"
        :value="option"
        :checked="modelValue.includes(option)"
        @change="(e) => onCheckboxChange(option, e.target.checked)"
      />
      {{ option }}
    </label>
  </div>
</template>

<style scoped>
.checkbox-filter {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 250px;
  overflow-y: auto;
}

.filter-search {
  padding: 5px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.85rem;
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  cursor: pointer;
}

.checkbox-label input {
  cursor: pointer;
}
</style>
