<template>
  <div id="app">
    <app-header></app-header>
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/Header'

export default {
  name: "直肠肿瘤辅助诊断系统",
  data() {
    return {

    }
  },
  components: {
    "app-header": Header,
  },
  methods: {

  },

};
</script>

<style scoped></style>
