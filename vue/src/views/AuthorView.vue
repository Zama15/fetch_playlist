<script>
import {
  fetchAuthorMetadataById,
  fetchLimitedPlaylistsByAuthorId,
} from "@/services/fetcherApiService";
import ProfileSide from "@/components/author/ProfileSide.vue";
import ProfileTop from "@/components/author/ProfileTop.vue";
import PlaylistCard from "@/components/author/PlaylistCard.vue";
import LoadingBlock from "@/components/shared/LoadingBlock.vue";

export default {
  components: {
    LoadingBlock,
    ProfileSide,
    ProfileTop,
    PlaylistCard,
  },
  data: function () {
    return {
      author: null,
      playlists: null,

      loadingAuthor: true,
      loadingPlaylists: true,

      error: false,
      errorMessage: "",
    };
  },
  async created() {
    const authorId = this.$route.params.authorId;
    this.fetchAuthorMetadata(authorId);
    this.fetchAuthorPlaylists(authorId);
  },
  methods: {
    fetchAuthorMetadata: async function (authorId) {
      const res = await fetchAuthorMetadataById(authorId);

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "Unable to retrieve author data";
        return;
      }

      this.author = res.data;
      this.loadingAuthor = false;
    },
    fetchAuthorPlaylists: async function (authorId) {
      const res = await fetchLimitedPlaylistsByAuthorId(authorId);

      if (!res.ok) {
        this.error = true;
        this.errorMessage =
          res.message || "Unable to retrieve author playlists";
        return;
      }

      this.playlists = res.data.items;
      this.loadingPlaylists = false;
    },
  },
};
</script>

<template>
  <div class="vw-100 vh-100 overflow-hidden">
    <ProfileTop :author="author" />

    <ProfileSide :author="author" />

    <div class="author-playlist_grid">
      <PlaylistCard
        v-if="!loadingPlaylists"
        v-for="(item, index) in playlists"
        :key="index"
        :playlist="item"
      />
    </div>
  </div>
</template>
