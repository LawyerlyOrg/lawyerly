<template>
    <div>
      Selected: {{ selected }}
    </div>
    <div>
      <div v-for="{relevancy, index} in relevancies" :key="index">
        {{ relevancy }}
      </div>
      <!-- <p v-if="relevancies">{{ relevancies }}</p> -->
    </div>
  </template>
  
  <script>
import axios from 'axios';

  export default {
    name: 'RelevanciesReport',
    props: {
      selected: {
        default: ''
      }
    },
    data() {
      return {
        relevancies: [],
      }
    },
    watch: {
      selected: function (newVal) {
        //
        axios.get('https://lawyerlyservice.uw.r.appspot.com/relevancies?collection_id=65149bcca1b526a820ee1892&fact_sheet_id=' + newVal, 
          { params: { selected: newVal }}
          )
        .then(response => {
          // handle response data
          this.relevancies = response.data;
          console.log(this.relevancies);
        })
        .catch(error => {
          // handle error
          console.log(error);

        }, []);
      }
    }
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