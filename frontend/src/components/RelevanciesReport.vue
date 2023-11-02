<template>
  <div class="container">
    <div>
      <button class="button is-primary" v-if="selected && !loading && !isHidden" @click="getRelevancy(); isHidden=true">
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
      <table class="table is-hoverable is-fullwidth" v-if="displayContent">
        <thead >
          <tr>
            <th>Case</th>
            <th>Relevancy</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, key) in relevancies" :key="key">
            <td>{{ sharedCases.find((element) => element._id.$oid === key).name }}</td>
            <td class="break-newlines">{{ item }}</td>
          </tr>
        </tbody>
      </table>
  

      <!-- <table class="table is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Case</th>
            <th>Relevancy</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(person, index) in people" :key="index">
            <td>{{ person.name }}</td>
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
      isHidden: false,
      displayContent: false,
      people: [
         { name: "JaneJaneJaneJane Smith", gender: "- Both the summary and the factsheet mention the topic of law and legal reforms.\n- Both mention the concept of self-defence.\n- Both mention the purpose of simplifying the legislative text.\n- Both mention the removal of preconditions in the old law.\n- Both mention a three-part framework in the new law.\n- Both mention a specific case involving a person named Allison and her partner Daniel." },
         { name: "Alice Johnson", gender: "- Both the summary and the factsheet mention a case involving a trial judge's error of law.\n- Both mention the concept of party liability.\n- Both mention the need for a new trial.\n- Both mention the Criminal Code and its treatment of principal offenders and parties to an offense.\n- Both mention the importance of considering all theories of liability based on the evidence." },
         { name: "Bob Brown", gender: "- Both the Summary and the Factsheet mention Canada and its legal system.\n- Both mention the topic of self-defence.\n- Both mention the purpose of the reforms to simplify the legislative text and facilitate the application of self-defence principles.\n- Both mention the removal of preconditions and the creation of a single, three-part defence.\n- Both mention a person named Daniel and his sexual relationship with a person named Allison." },
         { name: "Charlie Davis", gender: "Non-Binary" },
      ],
    };
  },
  methods: {
    getRelevancy() {
      console.log("this is the fact sheet: " + this.selected);
      this.loading = true;
      axios
        .get(
          "https://lawyerlyservice.uw.r.appspot.com/relevancies?collection_id=6536eeb20c27a16e16d0ad92&fact_sheet_id=" +
            this.selected,
          { params: { selected: this.selected } }
        )
        .then((response) => {
          // handle response data
          this.relevancies = response.data;
          if (response.data != null) {
            this.displayContent = true;
          }
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
