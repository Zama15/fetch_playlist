<script>
import VideoDetail from "@/components/playlist/VideoDetail.vue";
import VideoCompact from "@/components/playlist/VideoCompact.vue";
import { fetchLimitedPlaylistItemsById } from "@/services/fetcherApiService";

export default {
  components: {
    VideoDetail,
    VideoCompact,
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
      default: 50,
    },
  },
  data() {
    return {
      selectedLimit: this.defaultLimit,
      offset: 1,

      items: [],
      loading: false,

      error: false,
      errorMessage: "",

      viewMode: "compact",
      observer: null,
    };
  },
  computed: {
    canLoadMore() {
      return this.items.length < this.playlistCount;
    },
  },
  methods: {
    fetchMore: async function () {
      if (this.loading || !this.canLoadMore) return;

      this.loading = true;

      // console.time("Reconstructing items list");
      const itemsRequested = Array(this.selectedLimit).fill(null);
      this.items.push(...itemsRequested);
      // console.timeEnd("Reconstructing items list");

      // console.time("Fetching Items");
      const res = await fetchLimitedPlaylistItemsById(
        this.id,
        this.offset,
        this.selectedLimit
      );

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "Unable to retrieve playlist videos";
        this.loading = false;

        return;
      }
      // console.timeEnd("Fetching Items");

      // console.time("Restructuring Items List");
      const itemsFetched = res.data.items;
      for (let i = 0; i < itemsFetched.length; i++) {
        this.items[this.offset - 1 + i] = itemsFetched[i];
      }
      this.items = this.items.slice(0, this.playlistCount);
      // console.timeEnd("Restructuring Items List");

      // console.time("Performing final tasks");
      this.offset += this.selectedLimit;
      this.loading = false;
      // console.timeEnd("Performing final tasks");
    },
    setupObserver: function () {
      const sentinel = this.$refs.sentinel;
      if (!sentinel) return;

      this.observer = new IntersectionObserver(
        async ([entry]) => {
          if (entry.isIntersecting && this.canLoadMore) {
            await this.fetchMore();
          }
        },
        {
          root: null,
          rootMargin: "200px",
          threshold: 0.1,
        }
      );

      this.observer.observe(sentinel);
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.fetchMore().then(() => this.setupObserver());
    });
  },
  beforeMount() {
    if (this.observer) this.observer.disconnect();
  },
};
</script>

<template>
  <div class="playlist-wrapper mt-3">
    <div class="playlist-wrapper_control m-2 flex gap-2 justify-end">
      <button
        @click="viewMode = 'detailed'"
        :class="['btn', { active: viewMode === 'detailed' }]"
      >
        <i class="bi bi-list-task"></i>
      </button>
      <button
        @click="viewMode = 'compact'"
        :class="['btn', { active: viewMode === 'compact' }]"
      >
        <i class="bi bi-grid"></i>
      </button>
    </div>

    <div class="playlist-wrapper_list mb-5">
      <div v-if="viewMode === 'compact'" class="playlist-wrapper_list_compact">
        <VideoCompact
          v-for="(item, index) in items"
          :key="index"
          :video="item"
        />
      </div>
      <template v-else>
        <VideoDetail
          v-for="(item, index) in items"
          :key="index"
          :video="item"
        />
      </template>
    </div>

    <div v-show="canLoadMore" ref="sentinel"></div>
  </div>
</template>
