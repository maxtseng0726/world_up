<template>
  <header class="navbar">
    <router-link to="/home">Home</router-link> |
    <router-link to="/goals">Goals</router-link> |
    <router-link to="/levels">Levels</router-link>
  </header>

  <!-- The current page content drops in here -->
  <router-view />
</template>
<style>
:root {
  font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 24px;
  font-weight: 400;

  color: #0f0f0f;
  background-color: #f6f6f6;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}
</style>
