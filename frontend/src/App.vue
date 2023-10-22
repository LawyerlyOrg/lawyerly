<template>
  <SelectFactSheet v-bind:child-prop="selectedItem" v-on:custom-event="updateSelectedItem"/>
  <SelectCases />
  <RelevanciesReport :selected="selectedItem"/>

</template>

<script>

import SelectFactSheet from './components/SelectFactSheet.vue'
import SelectCases from './components/SelectCases.vue'
import RelevanciesReport from './components/RelevanciesReport.vue'

export default {
  name: 'App',
  components: { SelectFactSheet, SelectCases, RelevanciesReport },
  data() {
  return {
    selectedItem: '',
  }
},
methods: {
  updateSelectedItem(newValue) {
    this.selectedItem = newValue;
  }
}
  
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
  background: white;
}
</style>
