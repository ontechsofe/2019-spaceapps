<template>
  <transition name="fade" mode="out-in">
    <router-view></router-view>
  </transition>
</template>

<script>
export default {
  name: 'Stratos',
  data: () => ({}),
};
</script>

<style lang="scss">
  body {
    background: linear-gradient(to bottom, #033a5e 0%, #a1b8c3 100%);
  }
  .fade-enter-active,
  .fade-leave-active {
    transition-duration: 0.3s;
    transition-property: opacity;
    transition-timing-function: ease;
  }
  .fade-enter,
  .fade-leave-active {
    opacity: 0
  }
</style>
