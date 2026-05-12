<script setup>
const props = defineProps({
  options: Array,
  modelValue: Array
})

const emit = defineEmits(['update:modelValue'])

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
    <label v-for="option in options" :key="option" class="checkbox-label">
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
