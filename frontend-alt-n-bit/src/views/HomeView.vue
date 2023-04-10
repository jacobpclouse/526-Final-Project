<template>
  <div class="home">
    <Header></Header>

    <v-container align-center max-width="600">
      <v-file-input label="Upload file for encryption/decryption" accept="image/*" @change="fileChanged"
        class="mb-4 ml-n10" />

      <v-row>
        <v-col cols="12" sm="4">
          <v-text-field label="Number of blocks 'n'" v-model="numBlocks" class="mb-4" />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" sm="8">
          <v-textarea label="Text for encryption/decryption" v-model="text" no-resize rows="10" class="mb-4 mr-4" />
        </v-col>
      </v-row>
    </v-container>

    <v-row>
      <v-col>
        <v-btn color="primary" class="mr-4" @click="encrypt">Encrypt</v-btn>
        <v-btn color="primary" @click="decrypt">Decrypt</v-btn>
      </v-col>
    </v-row>

    <v-container>
      <v-row justify="center" class="mt-4">
        <v-col cols="12" sm="8" md="6">
          <v-card v-if="result" rounded min-height="500">
            <v-img v-if="isImage" :src="result" width="100%" height="auto" />
            <v-card-text v-else>{{ result }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

<!-- form originally used to test the if frontend was connected with backend -->
    <!-- <form @submit.prevent="sendMessage">
      <input type="text" v-model="message">
      <button type="submit">Send</button>
    </form> -->
  

  </div>
</template>


<script>
// @ is an alias to /src
import Header from "@/components/Header.vue";
import axios from 'axios';

export default {
  name: "HomeView",
  components: {
    Header,
  },
  data() {
    return {
      numBlocks: '',
      text: '',
      file: null,
      isImage: false,
      result: null,
    };
  },
  methods: {
    // Test to see if sending messages works
    // sendMessage() {
    //   axios.post('http://127.0.0.1:5000/', { message: this.message })
    //     .then(response => {
    //       console.log(response.data);
    //     })
    //     .catch(error => {
    //       console.error(error);
    //     });
    // },

    fileChanged(event) {
      this.file = event.target.files[0];
      this.isImage = this.file.type.startsWith('image/');
    },

    // Send encryption data to the flask app
    async encrypt() {
      if (this.file) {
        if (this.isImage) {
          // if image file is being encrypted, then send to image url
          const formData = new FormData();
          formData.append('image', this.file);
          formData.append('numBlocks', this.numBlocks);

          const response = await axios.post('http://127.0.0.1:5000/encrypt-image', formData);
          this.result = response.data;
          console.log(response.data);
        } else {
          // handle non-image file encryption
        }
      } else {
        const response = await axios.post('http://127.0.0.1:5000/encrypt-text', { text: this.text, numBlocks: this.numBlocks });
          // .then(response => {
          //   console.log(response.data);
          // })
          // .catch(error => {
          //   console.error(error);
          // });
        this.result = response.data;
        console.log(response.data);
      }
    },
    async decrypt() {
      if (this.file) {
        if (this.isImage) {
          const formData = new FormData();
          formData.append('image', this.file);
          formData.append('numBlocks', this.numBlocks);

          const response = await axios.post('http://127.0.0.1:5000/decrypt-image', formData);
          this.result = response.data;
          console.log(response.data);
        } else {
          // handle non-image file decryption
        }
      } else {
        // const response = await axios.post('/decrypt-text', { text: this.text, numBlocks: this.numBlocks });
        const response = await axios.post('http://127.0.0.1:5000/decrypt-text', { text: this.text, numBlocks: this.numBlocks });
        this.result = response.data;
        console.log(response.data);
      }
    },
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}

p {
  margin: 40px 20px 20px;
}
</style>