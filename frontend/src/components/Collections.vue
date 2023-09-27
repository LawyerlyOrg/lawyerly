<template>
  <div class="collections">
    <p>
      Hi there! Create a collection!
    </p>
    <label for="file-upload">Choose a file:</label>
    <input id="file-upload" type="file" @change="onFileSelected" />
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
export default {
  name: 'CollectionsComponent',
  methods: {
    onFileSelected(event) {
      this.file = event.target.files[0];
    },
    //https://lawyerly.vercel.app/api/collection/65149bcca1b526a820ee1892/cases?law_area=criminal_law
    uploadFile() {
      const formData = new FormData();
      formData.append(this.file.name, this.file);

      fetch('https://lawyerly.vercel.app/api/collection/65149bcca1b526a820ee1892/cases?law_area=criminal_law', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          // Handle the response from the Flask backend
          console.log(data)
        })
        .catch(error => {
          // Handle any errors
          console.error(error);
        });
    },
  },
  data() {
    return {
      file: null,
    };
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
