<!-- <template>
  <SelectFactSheet v-bind:child-prop="selectedItem" v-on:custom-event="updateSelectedItem"/>
  <SelectCases v-bind:child-prop="cases" v-on:custom-event="updateCases"/>
  <RelevanciesReport :selected="selectedItem" :sharedCases="cases"/>
</template> -->

<template>

<nav class="navbar">
  <div class="navbar">
    <a class="navbar-item" href="https://bulma.io">
      <img src="@/assets/abstract_geometric_design.png" width="112" height="112">
    </a>
  </div>
</nav>
  <div class="container">
    
    

    <div class="columns is-one-half is-gapless">
      <div class="column custom-column">
        <SelectFactSheet
          v-bind:child-prop="selectedItem"
          v-on:custom-event="updateSelectedItem"
        />
      </div>
      <div class="column custom-column">
        <SelectCases
          v-bind:child-prop="cases"
          v-on:custom-event="updateCases"
        />
      </div>
    </div>
    <RelevanciesReport :selected="selectedItem" :sharedCases="cases" />
  </div>
</template>

<script>
import SelectFactSheet from "./components/SelectFactSheet.vue";
import SelectCases from "./components/SelectCases.vue";
import RelevanciesReport from "./components/RelevanciesReport.vue";

export default {
  name: "App",
  components: { SelectFactSheet, SelectCases, RelevanciesReport},
  data() {
    return {
      selectedItem: "",
      cases: [],
    };
  },
  methods: {
    updateSelectedItem(newValue) {
      this.selectedItem = newValue;
    },
    updateCases(newCases) {
      this.cases = newCases;
    },
  },
};
</script>

<style scoped>
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

.container {
  max-width: 800px; /* or whatever width you prefer */
}

@media screen and (min-width: 960px) {
  .container {
    width: 800px; /* or your preferred width */
  }
}
</style>
