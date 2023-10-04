<template>
    <form @submit.prevent="onSubmit">
      <input type="file" @change="handleFileUpload" />
      <button type="submit">Upload</button>
    </form>
</template>

<script>
import { ref } from "vue";

export default {
  name: 'FileUpload',
  setup() {
    const file = ref(null);

    const handleFileUpload = (event) => {
      file.value = event.target.files[0];
    };

    const onSubmit = () => {
      console.log("selected file", file.value);
      // Upload to server Call API
    };

    return {
      handleFileUpload,
      onSubmit,
      file
    };
  }
};
</script>