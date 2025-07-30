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
};
</script>

<template>
  <div class="playlist-video p-1">
    <div class="playlist-video_img">
      <LoadingBlock v-if="!video" />
      <div v-else :style="{ backgroundImage: `url(${video.thumbnail})` }"></div>
    </div>
    <div class="d-flex flex-column justify-content-center w-100 ps-2">
      <div class="playlist-video_title">
        <LoadingBlock v-if="!video" extraClass="mb-1" />
        <h3 v-else class="h6 mb-1 d-inline-block text-truncate">
          {{ video.title }}
        </h3>
      </div>
      <div class="d-flex flex-row">
        <div class="playlist-video_info">
          <LoadingBlock v-if="!video" extraClass="mb-1" />
          <p v-else class="m-0 d-inline-block text-truncate">
            <i
              v-if="video?.channel_is_verified"
              class="bi bi-check2-circle"
            ></i>
            {{ video.channel }}
          </p>

          <LoadingBlock v-if="!video" />
          <small v-else class="m-0 d-inline-block text-truncate">{{
            video.duration_string
          }}</small>
        </div>
        <div class="playlist-video_stats">
          <LoadingBlock v-if="!video" extraClass="mb-1" />
          <small v-else class="m-0">
            {{ formatNumberShort(video.view_count) }}
            <i class="bi bi-eye ps-1"></i>
          </small>

          <LoadingBlock v-if="!video" extraClass="mb-1" />
          <small v-else class="m-0">
            {{ formatNumberShort(video.like_count) }}
            <i class="bi bi-hand-thumbs-up ps-1"></i>
          </small>
        </div>
      </div>
    </div>
  </div>
</template>
