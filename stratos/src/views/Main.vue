<template>
  <v-app>
    <Header/>
    <v-content id="main-background">
      <Visualizer v-bind:id="id"/>
    </v-content>
  </v-app>
</template>

<script>
    import Visualizer from '@/components/Visualizer.vue'
    import Header from '@/components/Header.vue'

    export default {
        name: 'main',
        props: ['id'],
        components: {
            Header,
            Visualizer
        },
        mounted() {
            console.log(this.id)
        }
    }
</script>
