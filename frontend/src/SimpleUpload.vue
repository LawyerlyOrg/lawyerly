<template>
 <form @submit.prevent="sendFile" enctype="multipart/form-data">
    <div class="field">
        <label for="file" class="label">Upload Case Files</label>
        <input 
        type="file"
        @change = "selectFile" 
        ref="file" 
        />
    </div>

    <div class="field">
       <button class="button is-info">Upload</button>
    </div>
 </form>
</template>

<script>

import axios from 'axios';

export default {
    name: "SimpleUpload",

    data() {
        return {
            file: ""
        }
    },
    
    methods: {
        selectFile() {
            this.file = this.$refs.file.files[0];
        },

        async sendFile() {
            const formData = new FormData();
            formData.append('file', this.file);
            // formData.append('key', this.file.name);
            try {
                await axios.post('https://lawyerly.vercel.app/api/collection/65149bcca1b526a820ee1892/cases?law_area=criminal_law', formData)
            } catch(err) {
                    console.log(err);
            }
        }
    }
}
</script>