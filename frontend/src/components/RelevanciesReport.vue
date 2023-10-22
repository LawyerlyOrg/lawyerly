<template>
    <div>
    <button v-if="selected" @click="getRelevancy">Generate</button>
  </div>
    <table class="table is-bordered is-striped is-narrow is-hoverable">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in relevancies" :key="key">
          <td>{{ key }}</td>
          <td>{{ value }}</td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script>
import axios from 'axios';

  export default {
    name: 'RelevanciesReport',
    props: {
      selected: {
        type: String,
        required: true,
        default: ''
      }
    },
    data() {
      return {
        fact_sheet_id: '',
        relevancies: [],
      }
    },
    methods: {
      getRelevancy() {
        console.log(this.selected);
        axios.get('https://lawyerlyservice.uw.r.appspot.com/relevancies?collection_id=65149bcca1b526a820ee1892&fact_sheet_id=' + this.selected, 
          { params: { selected: this.selected }}
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