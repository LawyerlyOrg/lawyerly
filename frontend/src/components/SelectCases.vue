<template>
<div class="card">
  <header class="card-header">
    <p class="card-header-title">
      List of Cases
    </p>
  </header>
  <div class="card-content">
    <ul>
      <li v-for="(item, index) in cases" :key="index">
      {{ item.name }}
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
</style>
