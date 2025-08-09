<script>
import { Tooltip } from "bootstrap";
import { triggerRef } from "vue";

export default {
  props: {
    text: {
      type: String,
      required: true,
    },
  },
  methods: {
    copy: async function () {
      try {
        await navigator.clipboard.writeText(this.text);
      } catch (error) {
        console.error(error);
      }
    },
    show: function () {
      this.copy();

      const copyEl = this.$refs.copy;
      const tooltip = new Tooltip(copyEl, {
        trigger: "manual",
        placement: "top",
      });

      tooltip.show();

      const hideTooltip = () => tooltip.hide();

      copyEl.addEventListener("blur", hideTooltip, { once: true });
      setTimeout(hideTooltip, 1500);
    },
  },
};
</script>

<template>
  <div class="copy-block">
    <div class="copy-block_wrapper">
      <div class="copy-block_text text-truncate">
        {{ text }}
      </div>
      <i
        class="copy-block_icon bi bi-copy"
        ref="copy"
        v-on:click="show"
        data-bs-trigger="manual"
        title="Copied!"
      ></i>
    </div>
  </div>
</template>
