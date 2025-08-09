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
    toAuthor: function () {
      if (!this.author?.uploader_id) return;

      this.$router.push(`/author/${this.author.uploader_id}`);
    },
  },
  computed: {
    banner() {
      return this.author && this.author.banner.url
        ? `url(${this.author.banner.url})`
        : false;
    },
    avatar() {
      return this.author && this.author.avatar.url
        ? `url(${this.author.avatar.url})`
        : false;
    },
  },
};
</script>

<template>
  <div class="playlist-author card py-3" :style="{ backgroundImage: banner }">
    <div class="playlist-author_overlay rounded" v-if="!loading"></div>
    <div class="d-flex justify-content-center pb-2">
      <div
        class="playlist-author_img thumbnail"
        :style="{ backgroundImage: avatar }"
      >
        <LoadingBlock v-if="loading" />
        <div v-else @click="toAuthor" class="thumbnail--overlay link"></div>
      </div>
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
