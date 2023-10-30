<!-- <template>
  <SelectFactSheet v-bind:child-prop="selectedItem" v-on:custom-event="updateSelectedItem"/>
  <SelectCases v-bind:child-prop="cases" v-on:custom-event="updateCases"/>
  <RelevanciesReport :selected="selectedItem" :sharedCases="cases"/>
</template> -->

<!-- <template>

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
</style> -->

// Source: https://www.vuescript.com/form-wizard-stepper/
<template>
  <nav class="navbar" aria-label="main navigation">
  <div class="navbar">
    <a class="navbar-item" href="https://bulma.io">
      <img src="@/assets/abstract_geometric_design.png" alt:="DEMO">
    </a>
  </div>
</nav>
  <div id="app">
    <div class="container">
      <h1 class="title">Lawyerly Demo</h1>
      <Wizard
        squared-tabs
        card-background
        navigable-tabs
        scrollable-tabs
        :nextButton="nextButtonOptions"
        :custom-tabs="[
          {
            title: 'Select Fact Sheet',
          },
          {
            title: 'Select Cases',
          },
          {
            title: 'Generate Relevancies',
          },
          
        ]"
        :beforeChange="onTabBeforeChange"
        @change="onChangeCurrentTab"
        @complete:wizard="wizardCompleted"
      >
        <h5 v-if="currentTabIndex === 0">
          <div>
            <SelectFactSheet v-bind:child-prop="selectedItem" v-on:custom-event="updateSelectedItem"/>
          </div>
        
        </h5>
        <h5 v-if="currentTabIndex === 1">
          
          <SelectCases v-bind:child-prop="cases" v-on:custom-event="updateCases"/>
        
        </h5>
        <h5 v-if="currentTabIndex === 2">
          
          <RelevanciesReport :selected="selectedItem" :sharedCases="cases"/>
        
        </h5>
      </Wizard>
    </div>

    <!-- <div style="margin-top: 100px">
      <h1>Vertical with Default Props</h1>
      <Wizard vertical-tabs />
    </div> -->
  </div>
</template>

<script>
import 'form-wizard-vue3/dist/form-wizard-vue3.css';
import Wizard from 'form-wizard-vue3';
import SelectFactSheet from "./components/SelectFactSheet.vue";
import SelectCases from "./components/SelectCases.vue";
import RelevanciesReport from "./components/RelevanciesReport.vue";

export default {
  name: 'App',
  components: {
    Wizard,
    SelectFactSheet,
    SelectCases,
    RelevanciesReport,
  },
  data() {
    return {
      currentTabIndex: 0,
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
    onChangeCurrentTab(index, oldIndex) {
      console.log(index, oldIndex);
      this.currentTabIndex = index;
    },
    onTabBeforeChange() {
      if (this.currentTabIndex === 0) {
        console.log('First Tab');
      }
      console.log('All Tabs');
    },
    wizardCompleted() {
      console.log('Wizard Completed');
    },
  },
  computed: {
    nextButtonOptions() {
      return this.currentTabIndex === 2
        ? {
            text: 'test',
            icon: 'check',
            hideIcon: true, // default false but selected for sample
            hideText: false, // default false but selected for sample
            disabled: true,
          }
        : { disabled: false };
    },
  },
};
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

.container {
  max-width: 800px; /* or whatever width you prefer */
}


</style>
