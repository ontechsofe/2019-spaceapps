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
                  Select the Visualization
                </h1>
                <v-autocomplete v-model="model" item-text="name" item-value="id" class="mt-12" color="white"
                                background-color="primary" label="DataSets" :items="dataSetNames"></v-autocomplete>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn outlined @click="gotoVisualization">Go</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
    // @ is an alias to /src
    import Header from '@/components/Header.vue';
    import axios from 'axios';

    export default {
        name: 'select',
        data: () => ({
            dataSets: [],
            model: null
        }),
        methods: {
            gotoVisualization() {
                this.$router.push(`/visualizer/${this.model}`);
            }
        },
        computed: {
            dataSetNames() {
                return this.dataSets
            }
        },
        components: {
            Header
        },
        mounted() {
            axios.get('http://localhost:5050/allDataSets').then(res => {
                this.dataSets = res.data;
            }).catch(err => {
                console.log(err);
            })
        }
    }
</script>
