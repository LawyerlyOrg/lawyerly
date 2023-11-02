<template>
  <div class="card">
    <header class="has-text-weight-bold">Select Cases</header>
    <h6 class="subtitle is-6">
      Click <svg-icon type="mdi" :path="path"></svg-icon> to view fact sheet
    </h6>

    <div class="invisible-box">
      <div class="control" v-for="(item, index) in cases" :key="index">
        <input
          type="checkbox"
          :value="item._id.$oid"
          v-model="selectedItem"
          @change="emitSelectedItem"
        />

        {{ item.name }}

        <svg-icon
          type="mdi"
          :path="path"
          @click="item.showText = !item.showText"
        ></svg-icon> 
        <div v-if="item.showText">
          <p class="break-newlines" :style="{ width: 200 + '%'}">{{ item.summary }}</p>
        </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiTextBoxSearchOutline } from "@mdi/js";


export default {
  name: "App",
  components: {
    SvgIcon,
  },
  data() {
    return {
      cases: [],
      message: "",
      showModal: false,
      path: mdiTextBoxSearchOutline,
    };
  },
  watch: {
    cases() {
      this.$emit("custom-event", this.cases);
    },
  },
  mounted() {
    axios
      .get(
        "https://lawyerlyservice.uw.r.appspot.com/collection/6536eeb20c27a16e16d0ad92/cases"
      )
      .then((response) => {
        this.cases = response.data;
        console.log(this.cases);
        //this.emitCases();
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style>
.custom-card .card-content {
  margin: 1px; /* Adjust this value to your liking */
}

.invisible-box {
  display: inline-block; /* This makes the div behave like an inline element, so it can be centered using text-align */
  width: 30%; /* Adjust this width as needed */
  text-align: left; /* This aligns the text to the left of the invisible box */
  margin-bottom: 2em;
}

.align-left {
  text-align: left !important;
}

header {
  display: block;
  font-size: 1.5em;
  margin-top: 0.5em;
  margin-bottom: 0.67em;
  padding-top: 1em;
  margin-left: 0;
  margin-right: 0;
  font-weight: bold;
}
</style>
