<template>
<div class="card">
  <header class="has-text-weight-bold">
      Select Cases
    </header>
  <div class="card-content">
    <ul>
      <li v-for="(item, index) in cases" :key="index" v-on:mouseover="item.showText = true" v-on:mouseleave="item.showText = false">
      {{ item.name }}
      <div v-if="item.showText">
        {{ item.summary }}
      </div>
    </li>
    </ul>
  </div>
</div>

</template>

<script>
import axios from "axios";
export default {
  name: 'App',
  data() {
    return {
      cases: [],
      message: "",
    };
  },
  watch: {
    cases() {
      this.$emit('custom-event', this.cases);
    }
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
  margin: 1px;  /* Adjust this value to your liking */
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
