<script>
import {
  fetchPlaylistMetadataById,
  fetchAuthorMetadataById,
} from "@/services/fetcherApiService";

export default {
  data: function () {
    return {
      playlistId: "",
      authorId: "",
      error: false,
      errorMessage: "",
    };
  },
  methods: {
    fetchPlaylist: async function (e) {
      e.preventDefault();

      if (this.playlistId.length < 24 && this.playlistId !== "") {
        this.error = true;
        this.errorMessage =
          "The length of the id is too short(24 characters required)";

        return;
      }

      const res = await fetchPlaylistMetadataById(this.playlistId);

      if (!res.ok) {
        this.error = true;
        this.errorMessage =
          res.message || "No playlist found with the given id";
        return;
      }

      this.$router.push(`/playlist/${this.playlistId}`);
    },
    getAuthorPlaylists: async function (e) {
      e.preventDefault();

      if (
        this.authorId.length < 24 &&
        this.authorId !== "" &&
        !this.authorId.includes("@")
      ) {
        this.error = true;
        this.errorMessage =
          "The length of the id is too short(24 characters required)";

        return;
      }

      const res = await fetchAuthorMetadataById(this.authorId);

      if (!res.ok) {
        this.error = true;
        this.errorMessage = res.message || "No author found with the given id";
        return;
      }

      const author = res.data;

      if (!author || !author.uploader_id) {
        this.error = true;
        this.errorMessage = "Author found, but unable to proceed further.";
        return;
      }

      this.$router.push(`/author/${author.uploader_id}`);
    },
    dismissError: function () {
      this.error = false;
    },
  },
};
</script>

<template>
  <div class="container vh-100">
    <div class="row h-100 d-flex justify-content-center align-items-center">
      <div class="col-md-6">
        <h1 class="text-center fw-bold">Get Playlists</h1>

        <div
          class="alert alert-danger d-flex align-items-center justify-content-between"
          v-if="error"
          @click="dismissError"
        >
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
          <input
            type="text"
            name="playlist-id"
            id="playlist-id"
            class="form-control p-2"
            v-model="playlistId"
          />

          <button
            class="btn btn-primary mt-3 w-50 playlist"
            v-if="playlistId"
            @click="fetchPlaylist"
          >
            Get Playlist
          </button>
        </div>

        <div class="mb-3 form-group justify-content-center d-flex row">
          <label for="playlist-author-id" class="form-label fs-5 w-100 p-0">
            By author id
          </label>
          <input
            type="text"
            name="playlist-author-id"
            id="playlist-author-id"
            class="form-control"
            v-model="authorId"
          />

          <button
            class="btn btn-primary mt-3 w-50 playlist"
            v-if="authorId"
            @click="getAuthorPlaylists"
          >
            Get Playlists
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
