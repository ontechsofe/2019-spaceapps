<template>
  <v-app-bar app color="primary">
    <v-icon x-large>mdi-balloon</v-icon>
    <v-toolbar-title class="headline text-uppercase">
      <span class="font-weight-bold">STRATOS</span>
      <span class="font-weight-light">PHERE</span>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn to="/" text>Home</v-btn>
    <v-btn to="/upload" text>Upload</v-btn>
    <v-btn to="/visualizer" text>Visualize</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  data: () => ({})
};
</script>
