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
    <p class="d-flex justify-content-center text-break">
      {{ this.strim(playlist.description, 0, 100, '...') }}
    </p>
  </div>
</template>

<script>

export default {
  props: ['data'],
  inject: ['formatDate', 'strim'],
  data: function() {
    return {
      playlist: this.data.snippet
    }
  }
}
</script>
