<script>
import LoadingBlock from "@/components/shared/LoadingBlock.vue";

export default {
  props: {
    video: {
      type: Object,
      default: null,
    },
  },
  components: {
    LoadingBlock,
  },
  methods: {
    formatNumberShort(number) {
      if (number === null || number === undefined) return "0";

      const precision = 1;

      const absNum = Math.abs(number);
      if (absNum >= 1e9)
        return (number / 1e9).toFixed(precision).replace(/\.0$/, "") + "B";
      if (absNum >= 1e6)
        return (number / 1e6).toFixed(precision).replace(/\.0$/, "") + "M";
      if (absNum >= 1e3)
        return (number / 1e3).toFixed(precision).replace(/\.0$/, "") + "K";
      return number.toString();
    },
  },
  computed: {
    thumbnail() {
      return this.video && this.video.thumbnail
        ? `url(${this.video.thumbnail})`
        : false;
    },
  },
};
</script>

<template>
  <div class="playlist-video thumbnail">
    <div v-if="thumbnail" class="thumbnail--overlay play"></div>
    <div :style="{ backgroundImage: thumbnail }" class="playlist-video_img">
      <LoadingBlock v-if="!thumbnail" />
    </div>
    <!-- <div :class="['playlist-video_details', 'thumbnail', { active: !video }]"> -->
    <div :class="['playlist-video_details', { active: !video }]">
      <!-- <div v-if="thumbnail" class="thumbnail--overlay play"></div> -->
      <div class="playlist-video_title">
        <LoadingBlock v-if="!video" extraClass="mb-1" />
        <h3 v-else class="h6 mb-1 d-inline-block text-truncate">
          {{ video.title || "" }}
        </h3>
      </div>
      <div class="d-flex flex-row h-25">
        <div class="playlist-video_info">
          <LoadingBlock v-if="!video" />
          <small v-else class="m-0">{{ video.duration_string || "" }}</small>
        </div>
        <div class="playlist-video_stats">
          <LoadingBlock v-if="!(video && video.view_count)" extraClass="mb-1" />
          <small v-else class="m-0">
            {{ formatNumberShort(video.view_count) }}
          </small>
        </div>
      </div>
    </div>
  </div>
</template>
