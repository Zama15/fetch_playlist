<template>
  <div class="playlist-items_item row row-cols-auto py-1 d-flex">
    <div class="playlist-items_item-thumbnail col p-0" ref="videoThumbnail">
      <span class="substitute"></span>
    </div>
    <div class="col-7 d-flex flex-column justify-content-around px-2">
      <h3 class="playlist-items_item-title p-0 m-0 h6" ref="videoTitle">
        <span class="substitute"></span>
      </h3>
      <small class="playlist-items_item-authorTitle" ref="videoAuthor">
        <span class="substitute"></span>
      </small>
    </div>
    <div class="playlist-items_item-info col flex-grow-1 d-flex flex-column justify-content-around align-items-end px-0">
      <small class="d-flex" ref="videoViews">
        <span class="substitute"></span>
      </small>
      <small class="d-flex" ref="videoDuration">
        <span class="substitute"></span>
      </small>
      <small class="d-flex" ref="videoPublishedAt">
        <span class="substitute"></span>
      </small>
    </div>
  </div>
</template>

<script>
export default {
  props: ['id'],
  inject: ['formatDate', 'strim', 'formatNumber', 'formatPeriodTime'],
  mounted() {
    this.$nextTick(() => {
      this.fetchChannel();
    });
  },
  methods: {
    fetchChannel: function() {
      const API = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics';
      const where = `&id=${this.id}`;
      
      fetch(`${API}${where}&key=${import.meta.env.VITE_YOUTUBE_DATA_API_KEY}`)
      .then(response => response.json())
      .then(data => {
        if (data.items.length !== 0) {
          const video = data.items[0];
          
          this.$refs.videoTitle.innerHTML = video.snippet.title;
          this.$refs.videoAuthor.innerHTML = video.snippet.channelTitle
          this.$refs.videoViews.innerHTML = `${this.formatNumber(video.statistics.viewCount)} views`;
          this.$refs.videoDuration.innerHTML = `${this.formatPeriodTime(video.contentDetails.duration)} `
          this.$refs.videoPublishedAt.innerHTML = this.formatDate(video.snippet.publishedAt);
          
          this.$refs.videoThumbnail.innerHTML = `
            <img src="${video.snippet.thumbnails.medium.url}" alt="${video.snippet.title}" />
          `;
        } else if (data.error) {
          this.$refs.videoTitle.innerHTML = data.error.message;
          this.$refs.videoAuthor.innerHTML = `
            <a href="https://www.youtube.com/watch?v=${this.id}" target="_blank" rel="noopener noreferrer">
              ${data.error.errors[0].reason}
            </a>
          `;
          console.log('Object with error:', data.error);
        } else {
          this.$refs.videoTitle.innerHTML = 'No video found';
          this.$refs.videoAuthor.innerHTML = `
            <a href="https://www.youtube.com/watch?v=${this.id}" target="_blank" rel="noopener noreferrer">
              No video found
            </a>
          `;
          console.log('Object with no items:', data);
        }
      }).catch(error => {
        console.log('Error fetching video with url:' + this.id);
        console.error(error);
      });
    }
  },
}
</script>
