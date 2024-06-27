<template>
  <div class="playlist-author row card py-3 flex-row mx-3 " :style="{ backgroundImage: `url(${authorBanner})` }">
    <div class="playlist-author_overlay rounded" v-if="authorBanner"></div>
    <div class="playlist-author_img flex-row d-flex justify-content-center pb-2" ref="authorThumbnail">
      <span class="substitute"></span>
    </div>
    <h2 class="playlist-author_title d-flex align-items-center justify-content-center" ref="authorTitle">
      <span class="substitute"></span>
    </h2>
    <div class="playlist-author_info">
      <p class="d-flex align-items-center justify-content-center m-0" ref="authorInfo">
        <span class="substitute mb-2"></span>
      </p>
      <small class="d-flex align-items-center justify-content-center" ref="authorId">
        <span class="substitute"></span>
      </small>
    </div>
  </div>
</template>

<script>
export default {
  props: ['id'],
  inject: ['formatDate'],
  data: function() {
    return {
      authorBanner: '',
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.getAuthor();
    });
  },
  methods: {
    getAuthor: function() {
      const API = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,brandingSettings,status&';
      const where = `id=${this.id}`;

      fetch(`${API}${where}&key=${import.meta.env.VITE_YOUTUBE_DATA_API_KEY}`)
        .then(response => response.json())
        .then(data => {
          const author = data.items[0];

          console.log(author);

          this.authorBanner = author.brandingSettings.image?.bannerExternalUrl;
          this.$refs.authorTitle.innerHTML = author.snippet.title;
          this.$refs.authorId.innerHTML = author.id;
          this.$refs.authorInfo.innerHTML = `
          <small class="pe-2">${author.snippet.customUrl}</small> •
          <small class="px-2">${author.status.privacyStatus}</small> •
            <small class="ps-2">${this.formatDate(author.snippet.publishedAt)}</small>
          `;
          this.$refs.authorThumbnail.innerHTML = `
            <img src="${author.snippet.thumbnails.default.url}" alt="${author.snippet.title}" />
          `;
        });
    }
  }
}
</script>
