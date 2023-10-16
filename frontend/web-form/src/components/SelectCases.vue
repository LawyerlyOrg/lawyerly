<template>
    <form>
        <label>Select Cases</label>

        <div>
      <ul>
        <div v-for="(item, index) in items" :key="index">
          <input type="checkbox" :value="item.id" v-model="message">
          {{ item.name }}
        </div>
      </ul>
    </div>

        <!-- <div class="case">
            <input type="checkbox">
            <label>Case1</label>
        </div>
        <div class="case">
            <input type="checkbox">
            <label>Case2</label>
        </div>
        <div class="case">
            <input type="checkbox">
            <label>Case3</label>
        </div> -->
    </form>

</template>

<script>

import axios from 'axios'
export default {
    name: 'App',
  data() {
    return {
      items: [],
      message: '',
    };
  },
  mounted() {
    axios.get('https://lawyerlyservice.uw.r.appspot.com/collection/65149bcca1b526a820ee1892/cases')
      .then((response) => {
        this.items = response.data;
        console.log(this.items);
      })
      .catch((error) => {
        console.log(error);
      });
  },


}

</script>

<style>
form {
    max-width: 420px;
    margin: 30px auto;
    background: white;
    text-align: left;
    padding: 40px;
    border-radius: 10px;
}

</style>