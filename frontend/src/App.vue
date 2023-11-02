// Source: https://www.vuescript.com/form-wizard-stepper/
<template>
  <!-- <nav class="navbar" aria-label="main navigation">
    <div class="navbar">
      <a class="navbar-item" href="https://bulma.io">
        <img src="@/assets/abstract_geometric_design.png" alt:="DEMO">
      </a>
    </div>
  </nav> -->

  <nav
    class="navbar is-fixed-top"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="navbar-brand">
      <a class="navbar-item" href="https://github.com/LawyerlyOrg/lawyerly">
        <img src="@/assets/lawyerly_logo.png" width="112" height="28" />
      </a>
    </div>
  </nav>

  <div id="app">
    <div class="container">

      <h6 class="subtitle is-6" style="text-align: left; margin-bottom: 0; margin-left: 10px">
        <strong>Lawyerly</strong> is a GPT-powered research tool designed to
        save lawyers time by distilling mountains of legal documents into information relevant to their case!
      </h6>

      <h6 class="subtitle is-6" style="text-align: left; margin-left: 10px; margin-top: 5px; color: grey">
        <em>Created using: Flask (Python),  Vue.js, MongoDB, OpenAI API, Langchain, Pinecone</em>
      </h6>

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
            <SelectFactSheet
              v-bind:child-prop="selectedItem"
              v-on:custom-event="updateSelectedItem"
            />
          </div>
        </h5>
        <h5 v-if="currentTabIndex === 1">
          <SelectCases
            v-bind:child-prop="cases"
            v-on:custom-event="updateCases"
          />
        </h5>
        <h5 v-if="currentTabIndex === 2">
          <RelevanciesReport :selected="selectedItem" :sharedCases="cases" />
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
import "form-wizard-vue3/dist/form-wizard-vue3.css";
import Wizard from "form-wizard-vue3";
import SelectFactSheet from "./components/SelectFactSheet.vue";
import SelectCases from "./components/SelectCases.vue";
import RelevanciesReport from "./components/RelevanciesReport.vue";

export default {
  name: "App",
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
        console.log("First Tab");
      }
      console.log("All Tabs");
    },
    wizardCompleted() {
      console.log("Wizard Completed");
    },
  },
  computed: {
    nextButtonOptions() {
      return this.currentTabIndex === 2
        ? {
            text: "test",
            icon: "check",
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
  margin-top: 5rem;
}

.container {
  max-width: 800px; /* or whatever width you prefer */
}
</style>
