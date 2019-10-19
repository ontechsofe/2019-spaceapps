<template>
  <v-app>
    <v-content>
      <HelloWorld/>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
export default {
  name: 'full',
  created() {
    this.$vuetify.theme.dark = false;
  }
}
</script>
