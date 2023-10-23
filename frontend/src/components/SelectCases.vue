<template>
  <form>
    <label>Cases:</label>
    <div>
      <ul>
        <div v-for="(item, index) in cases" :key="index">
          {{ item.name }}
        </div>
      </ul>
    </div>
  </form>
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
        "https://lawyerlyservice.uw.r.appspot.com/collection/65149bcca1b526a820ee1892/cases"
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
form {
  max-width: 420px;
  margin: 20px auto;
  background: white;
  text-align: left;
  padding: 10px;
  border-radius: 10px;
}
</style>
