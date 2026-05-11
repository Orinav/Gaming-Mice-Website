<template>
  <nav class="navbar">
    <div class="nav-links">
      <router-link to="/mice" class="nav-item">Mice Catalog</router-link>
      <router-link to="/compare" class="nav-item">Shape Compare</router-link>
    </div>
  </nav>

  <main>
    <router-view></router-view> <!-- The content is injected automatically by Vue Router at runtime, That's why navbar never disappears in compare to other elements-->
  </main>
</template>

<style>
body
{
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #ffffff;
}

.navbar {
  background-color: #2c3e50;
  padding: 15px 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-item {
  color: #bdc3c7;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: white;
  background-color: #34495e;
}

.router-link-active { /* This class is active only at run time */
  color: white;
  background-color: #e74c3c;
}

.router-link-active:hover { /* This class is active only at run time */
  background-color: #c0392b;
}
</style>