<script>
import LoadingBlock from "@/components/shared/LoadingBlock.vue";

export default {
  props: {
    author: {
      type: Object,
      default: null,
    },
  },
  components: {
    LoadingBlock,
  },
  computed: {
    banner() {
      return this.author && this.author.banner.url
        ? `url(${this.author.banner.url})`
        : false;
    },
  },
};
</script>

<template>
  <div class="author-profile--top">
    <div
      :style="{ backgroundImage: banner }"
      class="author-profile--top_img"
    ></div>
    <div class="author-profile--top_info">
      <div class="author-profile--top_info_title">
        <LoadingBlock v-if="!author" extraClass="mb-2" />
        <h1 v-else>
          {{ author.uploader || "" }}
        </h1>
      </div>

      <div class="author-profile--top_info_handle">
        <LoadingBlock v-if="!author" />
        <small v-else>
          {{ author.uploader_id || "" }}
        </small>
      </div>
    </div>
  </div>
</template>
