<script>
import { fetchAuthorMetadataById } from "@/services/fetcherApiService";
import LoadingBlock from "@/components/shared/LoadingBlock.vue";

export default {
  props: {
    id: String,
  },
  components: {
    LoadingBlock,
  },
  data: function () {
    return {
      author: null,
      loading: true,

      hasError: false,
      errorMessage: "",
    };
  },
  mounted() {
    this.fetchAuthor();
  },
  methods: {
    fetchAuthor: async function () {
      const res = await fetchAuthorMetadataById(this.id);

      if (!res.ok) {
        this.hasError = true;
        this.errorMessage =
          res.message || "Failed to load author/channel metadata.";

        return;
      }

      this.author = res.data;
      this.loading = false;
    },
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
  <div class="playlist-author card py-3" :style="{ backgroundImage: banner }">
    <div class="playlist-author_overlay rounded" v-if="!loading"></div>
    <div class="playlist-author_img d-flex justify-content-center pb-2">
      <LoadingBlock v-if="loading" />
      <img v-else :src="author.avatar.url" :alt="author.channel" />
    </div>

    <h2 class="playlist-author_title">
      <LoadingBlock v-if="loading" />
      <span v-else>{{ author.channel || "" }}</span>
    </h2>

    <div class="playlist-author_info">
      <p class="d-flex align-items-center justify-content-center m-0">
        <LoadingBlock v-if="loading" extraClass="mb-2" />
        <small v-else class="pe-2">{{ author.uploader_id || "" }}</small>
      </p>

      <small class="d-flex align-items-center justify-content-center">
        <LoadingBlock v-if="loading" />
        <span v-else>{{ author.id || "" }}</span>
      </small>
    </div>
  </div>
</template>
