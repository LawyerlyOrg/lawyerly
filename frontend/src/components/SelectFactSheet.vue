<template>
  <div>
    <h1>{{ message }}</h1>
  </div>

  <div class="card">
    <header class="has-text-weight-bold">Select Fact Sheet</header>
    <h6 class="subtitle is-6">Click <svg-icon type="mdi" :path="path"></svg-icon> to view fact sheet</h6>

    <div class="card-content">
      <div class="control" v-for="(item, index) in items" :key="index">
        
        <input
          type="radio"
          :value="item._id.$oid"
          v-model="selectedItem"
          @change="emitSelectedItem"
        />
        
        {{ item.name }}

        <svg-icon type="mdi" :path="path" @click="showModal=true"></svg-icon>

        <div v-if="showModal" class="modal is-active">
          <div class="modal-background" @click="showModal = false"></div>
          <div class="modal-content">
            <!-- Any kind of content can go here -->
            <table class="box">
              <h5 class="title is-5">Facts</h5>
              <tr>
                <td class="break-newlines align-left">{{ item.facts }}</td>
              </tr>
            </table>
          </div>
          <button
            class="modal-close is-large"
            aria-label="close"
            @click="showModal = false"
          ></button>
        </div>
        <div></div>
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
  props: ["modelValue"],
  components: {
    SvgIcon,
  },
  data() {
    return {
      items: [],
      selectedItem: this.selectedItem,
      showModal: false,
      path: mdiTextBoxSearchOutline,
    };
  },

  methods: {
    emitSelectedItem() {
      this.$emit("custom-event", this.selectedItem);
    },
  },
  // watch: {
  //   selectedItem(newValue) {
  //     this.$emit('update:modelValue', newValue)
  //   }
  // },
  mounted() {
    axios
      .get(
        "https://lawyerlyservice.uw.r.appspot.com/collection/6536eeb20c27a16e16d0ad92/factsheets"
      )
      .then((response) => {
        this.items = response.data;
        console.log(this.items);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style lang="scss">
@import "~bulma/bulma";

.align-left {
  text-align: left !important;
}

.radio {
  margin-bottom: 0.5rem;

  input[type="radio"] {
    margin-right: 0.5rem;
  }
}

svg { 
  cursor: pointer; 
  height: 1em;  /* 1em is relative to the font-size of the element or the container */
  width: auto;  /* maintain the aspect ratio */
  vertical-align: middle;  /* align with the middle of the adjacent text */
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
