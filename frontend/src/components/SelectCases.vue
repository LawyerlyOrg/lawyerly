<template>
  <div class="card">
    <header class="has-text-weight-bold">Select Cases</header>
    <h6 class="subtitle is-6 mb-2">
      Click <svg-icon type="mdi" :path="path"></svg-icon> to view case file
    </h6>

    <div class="invisible-box mt-2">
      <div class="control" v-for="(item, index) in cases" :key="index">
        <!-- <input
          type="checkbox"
          :value="item._id.$oid"
          v-model="selectedItem"
          @change="emitSelectedItem"
        /> -->

        {{ item.name }}

        <svg-icon
          type="mdi"
          :path="path"
          @click="item.showText = !item.showText"
        ></svg-icon>
        <div v-if="item.showText">
          <p class="break-newlines" :style="{ width: 200 + '%' }">
            {{ item.summary }}
          </p>
        </div>
      </div>
      <!-- File Upload Button -->
      <div
        class="file has-name is-small is-fullwidth is-black"
        v-if="!isUploading"
      >
        <label class="file-label">
          <input
            class="file-input"
            type="file"
            name="pdfs"
            @change="uploadFiles"
            accept="application/pdf"
            multiple
          />
          <span class="file-cta">
            <span class="file-icon">
              <i class="fas fa-upload"></i>
            </span>
            <span class="file-label"> Add Case Files </span>
          </span>
          <span class="file-name" v-if="uploadingFiles.length">
            {{ uploadingFiles.length }} files selected
          </span>
        </label>
      </div>
      <div v-else>
        <button class="button is-small is-fullwidth is-black" disabled>
        </button>
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
  components: {
    SvgIcon,
  },
  data() {
    return {
      cases: [],
      message: "",
      showModal: false,
      path: mdiTextBoxSearchOutline,
      items: [],
      uploadingFiles: [],
      selectedItem: null,
      isUploading: false,
    };
  },

  watch: {
    cases() {
      this.$emit("custom-event", this.cases);
    },
  },
  methods: {
    fetchCases() {
      axios
        .get(
          "https://lawyerlyservice.uw.r.appspot.com/collection/6536eeb20c27a16e16d0ad92/cases"
        )
        .then((response) => {
          this.cases = response.data;
          console.log(this.cases);
          //this.emitCases();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    uploadFiles(event) {
      const files = Array.from(event.target.files);
      this.uploadingFiles = files;
      this.isUploading = true;

      let uploadPromises = files.map((file) => {
        let formData = new FormData();
        formData.append("pdf", file); // Changed to 'pdf' because we are sending one file at a time

        return axios
          .post(
            "https://lawyerlyservice.uw.r.appspot.com/collection/6536eeb20c27a16e16d0ad92/cases?law_area=criminal_law",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )
          .then((response) => {
            console.log(`File uploaded: ${file.name}`, response);
          })
          .catch((error) => {
            console.error(`Error uploading file: ${file.name}`, error);
          });
      });

      Promise.all(uploadPromises)
        .then(() => {
          this.fetchCases(); // Refresh the list of PDFs after all files are uploaded
        })
        .finally(() => {
          this.isUploading = false;
          this.uploadingFiles = []; // Clear the list
        });
    },
  },
  mounted() {
    this.fetchCases();
  },
};
</script>

<style>
.custom-card .card-content {
  margin: 1px; /* Adjust this value to your liking */
}

.invisible-box {
  display: inline-block; /* This makes the div behave like an inline element, so it can be centered using text-align */
  width: 30%; /* Adjust this width as needed */
  text-align: left; /* This aligns the text to the left of the invisible box */
  margin-bottom: 2em;
}

.align-left {
  text-align: left !important;
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
