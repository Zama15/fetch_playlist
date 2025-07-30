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
@import url("https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css");
@import url("https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css");
@import "./assets/stylesheets/main.css";
</style>
