<template>
    <div>
      <main>
        <HeroSection/>
        <NowPlaying/>
        <HotCinemas/>
        <AboutUs />
      </main>
    </div>
  </template>
  
  <script>
  import NowPlaying from './NowPlaying.vue';
  import HotCinemas from './HotCinemas.vue';
  import AboutUs from './AboutUs.vue';
  import HeroSection from './HeroSection.vue';
  
  export default {
    components: {
      NowPlaying,
      HotCinemas,
      AboutUs,
      HeroSection,
    },
    setup() {
  },
  };
  </script>
  
  <style scoped>
  main {
    margin-top: 15vh; /* 给顶部栏留出空间 */
  }
  </style>
  