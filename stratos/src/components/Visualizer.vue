<template>
  <v-container fluid class="fill-height">
    <v-row style="height:90%">
      <v-col cols="2" class="fill-height">
        <v-sheet color="red" class="fill-height pa-5 ">
          <h1>Altitude</h1>
        </v-sheet>
      </v-col>
      <v-col cols="7" class="fill-height">
        <v-sheet color="green" class="fill-height pa-5">
          <h1>{{ id }}</h1>
        </v-sheet>
      </v-col>
      <v-col cols="3" class="fill-height">
        <v-sheet color="transparent" class="mb-10 pa-5" style="height:47%">
          <v-img src="ftp://ftp.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/Space%20Apps%20Challenge%202019/STRATOS/Stratos_DataSet/TIMMINS2018/CDH/CAM1-NADIR/103L.jpg"></v-img>
        </v-sheet>
        <v-sheet color="purple" class="mt-10 pa-5" style="height:48%">
          <h3>Bottom View</h3>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row style="height:10%">
      <v-col cols="12">
        <v-sheet color="yellow" class="pa-5" style="height:100%">
          <h3>Timeline</h3>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'visualizer',
        props: ['id'],
        data: () => ({
            allPoints: []
        }),
        mounted() {
            console.log(this.id);
            axios.get(`http://google.ca/search?q=${this.id}`)
                .then(res => console.log(res))
                .catch(err => console.log(err));
        }
    };
</script>
