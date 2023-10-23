<template>
  <div class="container">
    <div>
      <button class="button is-primary" v-if="selected && !loading" @click="getRelevancy">
        Generate
      </button>
      <div v-if="loading">
        <i class="fa fa-spinner fa-spin">Loading...</i>
      </div>
    </div>

    <!-- <div v-for="(item, key) in sharedCases" :key="key">
      <td>{{ item.name }}</td>
    </div> -->
    
    <div class="has-text-left">
      <table class="table is-bordered is-striped is-hoverable is-narrow">
        <thead v-if="relevancies === true">
          <tr>
            <th>Case</th>
            <th>Relevancy</th>
          </tr>
        </thead>
        <tbody v-if="relevancies">
          <tr v-for="(item, key) in relevancies" :key="key">
            <td>{{ sharedCases.find((element) => element._id.$oid === key).name }}</td>
            <td class="break-newlines">{{ item }}</td>
          </tr>
        </tbody>
      </table>

      <!-- <table class="table is-bordered is-striped is-hoverable is-narrow">
        <thead>
          <tr>
            <th>Name</th>
            <th>Age</th>
            <th>Gender</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(person, index) in people" :key="index">
            <td>{{ person.name }}</td>
            <td>{{ person.age }}</td>
            <td class="break-newlines">{{ person.gender }}</td>
          </tr>
        </tbody>
      </table> -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RelevanciesReport",
  props: {
    selected: {
      type: String,
      required: true,
      default: "",
    },
    sharedCases: {
      type: Array,
      required: true
    },
  },
  data() {
    return {
      fact_sheet_id: "",
      relevancies: [],
      loading: false,
    };
  },
  methods: {
    getRelevancy() {
      console.log(this.selected);
      this.loading = true;
      axios
        .get(
          "https://lawyerlyservice.uw.r.appspot.com/relevancies?collection_id=65149bcca1b526a820ee1892&fact_sheet_id=" +
            this.selected,
          { params: { selected: this.selected } }
        )
        .then((response) => {
          // handle response data
          this.relevancies = response.data;
          console.log(this.relevancies);
          this.loading = false;
        })
        .catch((error) => {
          // handle error
          console.log(error);
          this.loading = false;
        }, []);
    },
  },
};
</script>

<style>
div {
  margin: 10px;
}
.has-text-left {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}
.container {
  max-width: 600px;
  margin: 0 auto;
}
@media (max-width: 768px) {
  .container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 40px;
  }
}
.break-newlines {
  white-space: pre-line;
}
</style>
