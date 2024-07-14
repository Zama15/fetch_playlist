<template>
  <div class="playlist-hero pb-2">
    <div>
      <img :src="playlist.thumbnails.maxres.url" :alt="playlist.title" class="" />
    </div>
    <h1 class="px-3 text-break w-100 text-center">{{ playlist.title }}</h1>
    <small class="d-flex justify-content-center">
      {{ data.contentDetails.itemCount }} videos •
      {{ data.status.privacyStatus }} •
      {{ this.formatDate(playlist.publishedAt) }}
    </small>
    <small class="d-flex justify-content-center">
      {{ data.id }}
    </small>
    <p class="d-flex justify-content-center text-break text-center p-2 m-0">
      {{ this.strim(playlist.description, 0, 100, '...') }}
    </p>
  </div>
  <component 
    v-bind:is="'author'"
    v-bind:id="playlist.channelId"
  />
  <div class="playlist-items my-4 px-4">
    <playlistItem
      v-for="item in playlistItems"
      v-bind:id="item.snippet.resourceId.videoId"
    />
  </div>
</template>

<script>
  import author from './sidekicks/AuthorSmall.vue';
  import playlistItem from './sidekicks/PlayListItem.vue';

  export default {
    props: ['data'],
    inject: ['formatDate', 'strim'],
    components: {
      author,
      playlistItem
    },
    data: function() {
      return {
        playlist: this.data.snippet,
        playlistItems: [],
        nextPageToken: '',
      }
    },
    mounted() {
      this.$nextTick(() => {
        this.fetchPlaylist();
      });
      window.addEventListener('scroll', this.handleScroll);
      this.debug();
    },
    beforeUnmount() {
      window.removeEventListener('scroll', this.handleScroll);
    },
    methods: {
      fetchPlaylist: function(pageToken = '') {
        const API = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50';
        const where = `playlistId=${this.data.id}`;
        const page = pageToken ? `&pageToken=${pageToken}` : '';

        fetch(`${API}&${where}&key=${import.meta.env.VITE_YOUTUBE_DATA_API_KEY}${page}`)
          .then(response => response.json())
          .then(data => {
            this.playlistItems = this.playlistItems.concat(data.items);
            if (data.nextPageToken) {
              this.nextPageToken = data.nextPageToken;
            } else {
              window.removeEventListener('scroll', this.handleScroll);
            }
          }).catch(error => {
            console.error(error);
          });
      }, 
      handleScroll: function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
          this.fetchPlaylist(this.nextPageToken);
        }
      },
      debug: function() {
        const API = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics';
        const where = `&id=BTMaGo1oemY`;

        fetch(`${API}${where}&key=${import.meta.env.VITE_YOUTUBE_DATA_API_KEY}`)
        .then(response => response.json())
        .then(data => {
          console.log(data);
        }).catch(error => {
          console.error(error);
        });
      }
    }
  }
</script>
