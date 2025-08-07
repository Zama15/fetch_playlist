<script>
export default {
  props: {
    modelValue: [String, Number],
    options: {
      type: Array,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      isOpen: false,
    };
  },
  methods: {
    selectOption(option) {
      this.$emit("update:modelValue", option);
      this.isOpen = false;
    },
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

<template>
  <div class="cdropdown">
    <div class="cdropdown-box card" @click="toggleDropdown">
      <span class="cdropdown-box_selected">{{ modelValue }}</span>
      <i v-if="!isOpen" class="cdropdown-box_icon bi bi-caret-down-fill"></i>
      <i v-else class="cdropdown-box_icon bi bi-caret-up-fill"></i>
    </div>

    <ul v-if="isOpen" class="cdropdown-box_options card">
      <li
        v-for="option in options"
        :key="option"
        @click="selectOption(option)"
        :class="{ selected: option === modelValue }"
      >
        {{ option }}
      </li>
    </ul>
  </div>
</template>
