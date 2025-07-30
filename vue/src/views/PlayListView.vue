<script>
import { fetchPlaylistMetadataById } from "@/services/fetcherApiService";
import Author from "@/components/sidekicks/AuthorSmall.vue";
import PlaylistVideos from "@/components/PlaylistVideos.vue";
import LoadingBlock from "@/components/shared/LoadingBlock.vue";

export default {
  components: {
    LoadingBlock,
    Author,
    PlaylistVideos,
  },
  data: function () {
    return {
      playlist: null,
      loading: true,

      error: false,
      errorMessage: "",
    };
  },
  async created() {
    const playlistId = this.$route.params.playlistId;
    this.fetchPlaylist(playlistId);
  },
  methods: {
    fetchPlaylist: async function (playlist_id) {
      const res = await fetchPlaylistMetadataById(playlist_id);

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "Unable to retrieve playlist data";
        return;
      }

      this.playlist = res.data;
      this.loading = false;
    },
  },
};
</script>

<template>
  <div class="playlist-hero pb-2">
    <div>
      <img
        v-if="!loading"
        :src="playlist.thumbnail_best.url"
        :alt="playlist.title"
      />
    </div>
    <h1
      class="playlist-hero_title px-3 text-break w-100 text-center d-flex justify-content-center"
    >
      <LoadingBlock v-if="loading" extraClass="mt-2" />
      <template v-else>{{ playlist.title }}</template>
    </h1>
    <div class="playlist-hero_info">
      <small class="d-flex justify-content-center">
        <LoadingBlock v-if="loading" extraClass="mb-2" />
        <template v-else> {{ playlist.playlist_count }} videos </template>
      </small>
      <small class="d-flex justify-content-center">
        <LoadingBlock v-if="loading" />
        <template v-else> {{ playlist.id }} </template>
      </small>
      <p class="playlist-hero_info_description text-break text-center p-2 m-0">
        <LoadingBlock v-if="loading" />
        <span v-else class="d-inline-block text-truncate">
          {{ playlist.description }}
        </span>
      </p>
    </div>
  </div>

  <Author v-if="!loading" :id="playlist?.channel_id" />
  <PlaylistVideos
    v-if="!loading"
    :id="playlist?.id"
    :playlistCount="playlist?.playlist_count"
  />
</template>
