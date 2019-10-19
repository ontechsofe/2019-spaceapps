<template>
  <v-app>
    <v-content>
      <HelloWorld/>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/Visualizer.vue'

export default {
  name: 'full',
  components: {
    HelloWorld
  },
  created() {
    this.$vuetify.theme.dark = false;
  }
}
</script>
