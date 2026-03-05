<script setup>
defineProps({
  mice: Array,
  favorites: Array
})
defineEmits(['toggleFavorite', 'deleteMouse'])
</script>

<template>
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
      <tr v-for="mouse in mice" :key="mouse.id">
        <td>
          <button class="fav-btn" @click="$emit('toggleFavorite', mouse.id)">
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
          <button class="delete-btn" @click="$emit('deleteMouse', mouse.id)">🗑️</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

th, td {
    border: 1px solid #eee;
    padding: 12px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
    font-weight: bold;
}

.mouse-thumb {
    width: 60px;
    height: auto;
    display: block;
    margin: 0 auto;
}

/* כפתור מועדפים (❤️) */
.fav-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.4rem;
    transition: transform 0.2s ease;
}

.fav-btn:hover {
    transform: scale(1.2);
}

/* כפתור מחיקה (🗑️) */
.delete-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    padding: 5px;
    border-radius: 4px;
}

.delete-btn:hover {
    background-color: #fff0f0;
}

.buy-btn {
    display: inline-block;
    padding: 6px 12px;
    background-color: #42b883;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

.buy-btn:hover { background-color: #33996a; }

/* כותרת משקל ניתנת למיון */
th[style*="cursor:pointer"]:hover {
    background-color: #e9e9e9;
}
</style>