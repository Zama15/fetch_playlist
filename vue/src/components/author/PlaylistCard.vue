<script>
import {
  fetchPlaylistMetadataById,
  fetchLimitedPlaylistItemsById,
} from "@/services/fetcherApiService";
import VideoDetail from "@/components/playlist/VideoDetail.vue";
import CopyTruncated from "@/components/shared/CopyTruncated.vue";
import LoadingBlock from "@/components/shared/LoadingBlock.vue";

export default {
  props: {
    playlist: {
      type: Object,
      default: null,
    },
  },
  components: {
    LoadingBlock,
    CopyTruncated,
    VideoDetail,
  },
  data: function () {
    return {
      details: null,
      preview: null,

      isOpen: false,

      loadingDetails: false,
      loadingPreview: false,

      error: false,
      errorMessage: "",
    };
  },
  computed: {
    thumbnail() {
      return this.playlist && this.playlist.thumbnails[0].url
        ? `url(${this.playlist.thumbnails[0].url})`
        : false;
    },
  },
  methods: {
    toggleDropdown: function () {
      if (!this.playlist) return;

      this.isOpen = !this.isOpen;

      this.fetchPlaylistMetadata(this.playlist.id);
    },
    fetchPlaylistMetadata: async function (id) {
      if (!this.playlist || this.details || this.loadingDetails) return;

      this.loadingDetails = true;

      const res = await fetchPlaylistMetadataById(id);

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "Unable to retrieve playlist data";
        return;
      }

      this.details = res.data;
      this.loadingDetails = false;

      this.fetchPlaylistPreview(this.details.id);
    },
    fetchPlaylistPreview: async function (id) {
      if (!this.playlist || this.preview || this.loadingPreview) return;

      this.loadingPreview = true;

      const res = await fetchLimitedPlaylistItemsById(id, 1, 3);

      if (!res.ok) {
        this.error = true;
        this.errorMessage =
          res.message || "Unable to retrieve playlist preview";
        return;
      }

      this.preview = res.data.items;
      this.loadingPreview = false;
    },
    toPlaylist: function () {
      if (!this.playlist?.id) return;

      this.$router.push(`/playlist/${this.playlist.id}`);
    },
  },
};
</script>

<template>
  <div class="author-playlist_card card">
    <div
      :style="{ backgroundImage: thumbnail }"
      class="author-playlist_img card-img-top thumbnail"
    >
      <div
        v-if="playlist"
        @click="toPlaylist"
        class="thumbnail--overlay lg link"
      ></div>
    </div>
    <div
      :class="['author-playlist_info', 'card-body', { active: isOpen }]"
      @click="toggleDropdown"
    >
      <div class="author-playlist_info_title">
        <LoadingBlock v-if="!playlist" />
        <h3 v-else class="text-truncate">{{ playlist.title || "" }}</h3>
      </div>
      <div class="author-playlist_info_details--dropdown">
        <LoadingBlock v-if="!playlist" />
        <i v-else-if="playlist && !isOpen" class="bi bi-caret-down-fill"></i>
        <i v-else class="bi bi-caret-up-fill"></i>
      </div>
    </div>
    <div class="author-playlist_info_details card-footer" v-if="isOpen">
      <div class="d-flex flex-col justify-content-between">
        <div class="author-playlist_info_details_title">
          <LoadingBlock v-if="loadingDetails" />
          <CopyTruncated v-else :text="details.id" />
        </div>

        <div class="author-playlist_info_details_count">
          <LoadingBlock v-if="loadingDetails" />
          <template v-else>
            <i class="bi bi-collection-play"></i>
            {{ details.playlist_count }}
          </template>
        </div>
      </div>

      <div
        :class="[
          'author-playlist_info_details_playlist',
          { active: !loadingPreview },
        ]"
      >
        <VideoDetail
          v-if="!loadingPreview"
          v-for="(item, index) in preview"
          :key="index"
          :video="item"
        />
        <div v-else class="author-playlist_info_details_playlist--spinner">
          <div class="spinner-grow"></div>
        </div>
      </div>
    </div>
  </div>
</template>
