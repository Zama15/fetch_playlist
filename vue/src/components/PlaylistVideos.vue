<!-- vue/src/components/PlaylistVideos.vue -->
<script>
import VideoItem from "@/components/sidekicks/VideoItem.vue";
import { fetchLimitedPlaylistItemsById } from "@/services/fetcherApiService";

export default {
  components: {
    VideoItem,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
    playlistCount: {
      type: Number,
      required: true,
    },
    defaultLimit: {
      type: Number,
      default: 5,
    },
  },
  data() {
    return {
      selectedLimit: this.defaultLimit,
      offset: 0,

      items: [],
      loading: false,

      error: false,
      errorMessage: "",
    };
  },
  computed: {
    canLoadMore() {
      return this.items.length < this.playlistCount;
    },
  },
  methods: {
    fetchMore: async function () {
      if (this.loading) return;

      this.loading = true;

      const res = await fetchLimitedPlaylistItemsById(
        this.id,
        this.offset,
        this.selectedLimit
      );

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "Unable to retrieve playlist videos";

        return;
      }

      this.items.push(...res.data.items);
      this.offset += this.selectedLimit;
      this.loading = false;
    },
  },
  mounted() {
    this.fetchMore();
  },
};
</script>

<template>
  <div class="playlist-wrapper mt-3">
    <!-- <div class="playlist-wrapper_control m-2"></div> -->

    <div class="playlist-wrapper_list">
      <VideoItem
        v-for="(item, index) in loading
          ? Array(selectedLimit).fill(null)
          : items"
        :key="index"
        :video="item"
      />
    </div>

    <!-- Load more button -->
    <div v-if="canLoadMore" class="text-center mt-3">
      <button @click="fetchMore" :disabled="loading">
        {{ loading ? "Loading..." : "Load More" }}
      </button>
    </div>
  </div>
</template>
