<template>
  <div>
    <h1>{{ message }}</h1>
  </div>

  <div class="card">
    <header class="card-header">
      <p class="card-header-title">
        Select a Fact Sheet
      </p>
    </header>
    <div class="card-content">
      <div class="control" v-for="(item, index) in items" :key="index">
        <label class="radio tooltip-label">
            <input type="radio" :value="item._id.$oid" v-model="selectedItem" @change="emitSelectedItem">
            {{ item.name }}

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

</style>