<template>
  <v-container fluid class="fill-height" >
    <v-row style="height:90%">
      <v-col cols="2" class="fill-height">
        <v-sheet color="red" class="fill-height pa-5 ">
          <h1>Altitude</h1>
        </v-sheet>
      </v-col>
      <v-col cols="7" class="fill-height">
        <v-sheet color="green" class="fill-height pa-5">
          <h1>MAIN</h1>
        </v-sheet>
      </v-col>
      <v-col cols="3" class="fill-height">
        <v-sheet color="blue" class="mb-10 pa-5" style="height:47%">
          <h3>Horizon View</h3>
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
export default {
  data: () => ({})
};
</script>
