<template>
  <router-view />
</template>

<script>
export default {
  provide() {
    return {
      formatDate: this.formatDate,
    };
  },
  methods: {
    formatDate: function (dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
};
</script>

<style>
@import "./assets/stylesheets/main.css";
</style>
