<template>
  <div class="row h-100 d-flex justify-content-center align-items-center">
    <div class="col-md-6">

      <h1 class="text-center fw-bold">Get Playlists</h1>

      <div class="alert alert-danger d-flex align-items-center justify-content-between" v-if="error" @click="dismissError">
        <div>
          <i class="bi bi-exclamation-triangle-fill fs-4 pe-3"></i>
          {{ errorMessage }}
        </div>
        <i class="bi bi-x fs-4"></i>
      </div>

      <div class="mb-3 form-group justify-content-center d-flex row">
        <label for="playlist-id" class="form-label fs-5 w-100 p-0">
          By id
        </label>
        <input type="text" name="playlist-id" id="playlist-id" class="form-control p-2" v-model="playlistId" />

        <button class="btn btn-primary mt-3 w-50 playlist" v-if="playlistId" @click="getPlaylists">
          Get Playlist
        </button>        
      </div>

      <div class="mb-3 form-group justify-content-center d-flex row">
        <label for="playlist-author-id" class="form-label fs-5 w-100 p-0">
          By author id
        </label>
        <input type="text" name="playlist-author-id" id="playlist-author-id" class="form-control" v-model="authorId" />

        <button class="btn btn-primary mt-3 w-50 playlist" v-if="authorId" @click="getAuthorPlaylists">
          Get Playlists
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  const API = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet&'

  export default {
    data: function() {
      return {
        playlistId: '',
        authorId: '',
        error: false,
        errorMessage: '',
      }
    },
    methods: {
      getPlaylists: function(e) {
        e.preventDefault();
        
        if (this.playlistId.length < 24 && this.playlistId !== '') {
          this.error = true;
          this.errorMessage = 'The length of the id is too short(24 characters required)';
        } else {
          const where = `id=${this.playlistId}`;

          fetch(`${API}${where}&key=${import.meta.env.VITE_YOUTUBE_DATA_API_KEY}`)
            .then(response => response.json())
            .then(data => {
              if (data.items.length === 0) {
                this.error = true;
                this.errorMessage = 'No playlist found with the given id';
              } else {
                this.$emit('to', 1);
              }
            }).catch(error => {
              console.error('Error:', error);
              this.error = true;
              this.errorMessage = 'An error occurred while fetching the data';
            });
        }
      },

      getAuthorPlaylists: function(e) {
        e.preventDefault();
        
        if (this.authorId.length < 24 && this.authorId !== '') {
          this.error = true;
          this.errorMessage = 'The length of the id is too short(24 characters required)';
        } else {
          const where = `channelId=${this.authorId}`;
          
          fetch(`${API}${where}&key=${import.meta.env.VITE_YOUTUBE_DATA_API_KEY}`)
            .then(response => response.json())
            .then(data => {
              if (typeof data.error !== 'undefined') {
                this.error = true;
                this.errorMessage = data.error.message;
              } else {
                this.$emit('to', 2)
              }
            }).catch(error => {
              console.error('Error:', error);
              this.error = true;
              this.errorMessage = 'An error occurred while fetching the data';
            });
        }
      },

      dismissError: function() {
        this.error = false;
      }
    }
  }
</script>
