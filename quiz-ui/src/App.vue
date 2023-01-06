<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="header">
    <nav class="header-nav">
      <RouterLink to="/" class="header-nav-link">Home</RouterLink>
      <RouterLink to="/admin" class="header-nav-link">Admin</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>