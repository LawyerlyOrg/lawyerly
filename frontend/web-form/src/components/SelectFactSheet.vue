<template>
    <div>
    <h1>{{ message }}</h1>
  </div>
    <form>
        <label>Select FactSheet: </label>

        
        <div class="factsheet">
            <input type="radio">
            <label>Ghazals Case</label>
        </div>
        <div class="factsheet">
            <input type="radio">
            <label>Hadis Case</label>
        </div>
        <div class="factsheet">
            <input type="radio">
            <label>Farhangs Case</label>
        </div>
    </form>

</template>

<script>

import axios from 'axios'
export default {
  name: 'App',
  data() {
    return {
      message: '',
    };
  },
  mounted() {
    axios.get('https://lawyerlyservice.uw.r.appspot.com/collection/65149bcca1b526a820ee1892/factsheets')
      .then((response) => {
        this.message = response.data;
        console.log(this.message);
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
    margin: 30px auto;
    background: white;
    text-align: left;
    padding: 40px;
    border-radius: 10px;
}

</style>