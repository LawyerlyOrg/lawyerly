// Source: https://www.vuescript.com/form-wizard-stepper/
<template>
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
      <h6
        class="subtitle is-6"
        style="text-align: left; margin-bottom: 0; margin-left: 10px"
      >
        <strong>Lawyerly</strong> is a GPT-powered research tool designed to
        save lawyers time by distilling mountains of legal documents into
        information relevant to their case!
      </h6>

      <h6
        class="subtitle is-6"
        style="
          text-align: left;
          margin-left: 10px;
          margin-top: 5px;
          color: grey;
        "
      >
        <!-- <em
          >Created using: Flask (Python), Vue.js, MongoDB, OpenAI API,
          Langchain, Pinecone</em -->
        <!-- > -->
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
          <RelevanciesReport
            :selected-fact-sheet="selectedItem"
            :sharedCases="cases"
          />
        </h5>
      </Wizard>
    </div>

    <div class="container">
      <div class="card">
        <div class="card-content">
          <div class="content">
            <H1 class="title"> How We Made Lawyerly </H1>
            <p class="subtitle is-6">
              <em
                >Created using: Flask (Python), Vue.js, MongoDB, Google Cloud
                Platform (GCP), Vercel, OpenAI</em
              >
            </p>

            <iframe style="border:none" width="800" height="450" src="https://whimsical.com/embed/VbkHMwvj38xjwBk6Ked6w1@2Ux7TurymN7h1RReB9y2"></iframe>

            <h1>Hello World</h1>
            <p>
              Lorem ipsum<sup><a>[1]</a></sup> dolor sit amet, consectetur
              adipiscing elit. Nulla accumsan, metus ultrices eleifend gravida,
              nulla nunc varius lectus, nec rutrum justo nibh eu lectus. Ut
              vulputate semper dui. Fusce erat odio, sollicitudin vel erat vel,
              interdum mattis neque. Sub<sub>script</sub> works as well!
            </p>
            <h2>Second level</h2>
            <p>
              Curabitur accumsan turpis pharetra
              <strong>augue tincidunt</strong> blandit. Quisque condimentum
              maximus mi, sit amet commodo arcu rutrum id. Proin pretium urna
              vel cursus venenatis. Suspendisse potenti. Etiam mattis sem
              rhoncus lacus dapibus facilisis. Donec at dignissim dui. Ut et
              neque nisl.
            </p>
            <ul>
              <li>
                In fermentum leo eu lectus mollis, quis dictum mi aliquet.
              </li>
              <li>
                Morbi eu nulla lobortis, lobortis est in, fringilla felis.
              </li>
              <li>
                Aliquam nec felis in sapien venenatis viverra fermentum nec
                lectus.
              </li>
              <li>Ut non enim metus.</li>
            </ul>
            <article class="message">
              <div class="message-header" mg>Hello World</div>
              <div class="message-body">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                <strong>Pellentesque risus mi</strong>, tempus quis placerat ut,
                porta nec nulla. Vestibulum rhoncus ac ex sit amet fringilla.
                Nullam gravida purus diam, et dictum
                <a>felis venenatis</a> efficitur. Aenean ac
                <em>eleifend lacus</em>, in mollis lectus. Donec sodales, arcu
                et sollicitudin porttitor, tortor urna tempor ligula, id
                porttitor mi magna a neque. Donec dui urna, vehicula et sem
                eget, facilisis sodales sem.
              </div>
            </article>
          </div>
        </div>
      </div>
    </div>
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
      selectedFactSheet: false,
    };
  },
  methods: {
    updateSelectedItem(newValue) {
      this.selectedItem = newValue;
      this.selectedFactSheet = true;
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
        : { disabled: !this.selectedFactSheet };
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

.card-content .content {
  text-align: left;
}

.message {
  max-width: 80%; /* Adjust this value to suit your design needs */
  margin-left: auto; /* Centering the element */
  margin-right: auto; /* Centering the element */
}

.message-header {
  margin: 0rem !important;
}
</style>
