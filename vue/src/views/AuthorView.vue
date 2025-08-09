<script>
import { fetchLimitedPlaylistsByAuthorId } from "@/services/fetcherApiService";
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
      loading: true,

      error: false,
      errorMessage: "",
    };
  },
  async created() {
    const authorId = this.$route.params.authorId;
    this.fetchAuthor(authorId);
  },
  methods: {
    fetchAuthor: async function (authorId) {
      const res = await fetchLimitedPlaylistsByAuthorId(authorId);

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "Unable to retrieve author data";
        return;
      }

      this.author = res.data;
      this.loading = false;
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
        v-if="!loading"
        v-for="(item, index) in author?.entries"
        :key="index"
        :playlist="item"
      />
    </div>
  </div>
</template>
