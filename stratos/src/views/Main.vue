<template>
  <v-app>
    <Header/>
    <v-content id="main-background">
      <Visualizer/>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import Visualizer from '@/components/Visualizer.vue'
import Header from '@/components/Header.vue'

export default {
  name: 'main',
  components: {
    Header,
    Visualizer
  }
}
</script>
