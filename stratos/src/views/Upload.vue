<template>
  <v-app>
    <Header/>
    <v-content id="main-background">
      <v-container class="fill-height">
        <v-row justify="center" align="center">
          <v-col>
            <v-card color="primary" class="elevation-6 pa-6">
              <v-card-text>
                <h1>
                  <v-icon large>mdi-file-upload</v-icon>
                  Upload
                </h1>
                <p class="headline mt-5">This is the place to upload a dataset</p>
                <v-text-field :disabled="loading" v-model="name" label="Data Set Name" color="white"
                ></v-text-field>
                <v-file-input :disabled="loading" v-model="file" show-size color="white" accept=".txt"
                              label="File"></v-file-input>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="submitForm" outlined :loading="loading">Upload</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-dialog v-model="dialog" persistent max-width="400">
      <v-card>
        <v-card-title class="headline">Your dataset has been uploaded!</v-card-title>
        <v-card-text>The data has been sent to the server to be parsed, it will be available for visualizing shortly!
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">Okay!</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
    // @ is an alias to /src
    import Header from '@/components/Header.vue';
    import axios from 'axios';

    export default {
        name: 'upload',
        data: () => ({
            dialog: null,
            file: null,
            name: "",
            loading: false
        }),
        components: {
            Header
        },
        methods: {
            submitForm() {
                try {
                    this.loading = true;
                    let fileName = this.file.name;
                    if (fileName.lastIndexOf('.') <= 0) {
                        return;
                    }
                    const fr = new FileReader();
                    fr.readAsDataURL(this.file);
                    fr.addEventListener('load', () => {
                        let data = fr.result.split(',')[1];
                        let out = {
                            data: data,
                            name: this.name
                        };
                        axios.post('http://127.0.0.1:5050/rawData', out)
                            .then((res) => {
                                console.log(res);
                            })
                            .catch((err) => {
                                console.log(err);
                            });
                        this.dialog = true;
                        this.loading = false;
                    })
                } catch (e) {
                    console.log(e);
                } finally {
                    this.loading = false;
                }
            }
        }
    }
</script>
