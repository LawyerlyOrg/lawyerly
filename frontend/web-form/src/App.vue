<template>
  <SelectFactSheet />
  <SelectCases />

</template>

<script>

import SelectFactSheet from './components/SelectFactSheet.vue'
import SelectCases from './components/SelectCases.vue'

export default {
  name: 'App',
  components: { SelectFactSheet, SelectCases }
  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  margin: 0;
  background: #eee;
}
</style>
