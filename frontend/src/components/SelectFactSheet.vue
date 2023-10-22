<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
  <form>
    <label>Select Fact Sheet: </label>

    <div class="field">
      <div class="control" v-for="(item, index) in items" :key="index">
        <label class="radio">
          <input type="radio" :value="item._id.$oid" v-model="selectedItem" @change="emitSelectedItem">
          {{ item.name }}
        </label>
      </div>
    </div>

  </form>
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
    axios.get('https://lawyerlyservice.uw.r.appspot.com/collection/65149bcca1b526a820ee1892/factsheets')
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