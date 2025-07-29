<script>
export default {
  props: {
    height: String,
    width: String,
    extraClass: {
      type: String,
      default: "",
    },
  },
  computed: {
    styleObject() {
      const style = {};
      if (this.height) style.height = this.height;
      if (this.width) style.width = this.width;
      return style;
    },
    classList() {
      return ["substitute", this.extraClass].filter(Boolean).join(" ");
    },
  },
};
</script>

<template>
  <span :class="classList" :style="styleObject"></span>
</template>
