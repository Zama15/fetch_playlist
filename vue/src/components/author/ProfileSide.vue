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
    avatar() {
      return this.author && this.author.avatar.url
        ? `url(${this.author.avatar.url})`
        : false;
    },
  },
};
</script>

<template>
  <div class="author-profile--side">
    <div
      :style="{ backgroundImage: avatar }"
      class="author-profile--side_img"
    ></div>
    <div class="author-profile--side_overlay" v-if="author"></div>
    <div class="author-profile--side_stats py-2 pe-2">
      <!-- <LoadingBlock v-if="!author" />
      <div v-else class="author-profile--side_stats_playlist">
        <i class="bi bi-collection-play"></i>
        <h2>
          {{ author.playlist_count || 0 }}
        </h2>
      </div> -->

      <LoadingBlock v-if="!author" />
      <div class="author-profile--side_stats_followers" v-else>
        <i class="bi bi-person-plus"></i>
        <small>
          {{ formatNumberShort(author.channel_follower_count) }}
        </small>
      </div>
    </div>
  </div>
</template>
