<template>
  <div>
    <h1>{{ message }}</h1>
  </div>

  <div class="card">
    <header class="has-text-weight-bold">
      Select Fact Sheet
    </header>
    <div class="card-content">
      <div class="control" v-for="(item, index) in items" :key="index" v-on:mouseover="item.showText = true" v-on:mouseleave="item.showText = false">
        <label class="radio tooltip-label">
            <input type="radio" :value="item._id.$oid" v-model="selectedItem" @change="emitSelectedItem">
            {{ item.name }}
            <div v-if="item.showText">
              {{ item.facts }}
            </div>

        </label>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
export default {
  name: 'App',
  props: ['modelValue'],
  data() {
    return {
      items: [],
      selectedItem: this.selectedItem,
    };
  },
  methods: {
    emitSelectedItem() {
      this.$emit('custom-event', this.selectedItem);
    }

  },
  // watch: {
  //   selectedItem(newValue) {
  //     this.$emit('update:modelValue', newValue)
  //   }
  // },
  mounted() {
    axios.get('https://lawyerlyservice.uw.r.appspot.com/collection/6536eeb20c27a16e16d0ad92/factsheets')
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
@import '~bulma/bulma';

.radio {
  margin-bottom: 0.5rem;

  input[type="radio"] {
    margin-right: 0.5rem;
  }
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