<template>
  <div class="container vh-100">
    <component v-bind:is="screens[position]" @to="handleTo" />
  </div>
</template>

<script>
  import home from './components/Home.vue';
  import playlist from './components/PlayList.vue';
  import channel from './components/ChannelPlayList.vue';
  import item from './components/PlayListItem.vue';

  export default {
    components: {
      home,
      playlist,
      channel,
      item
    },
    data: function() {
      return {
        screens: ['home', 'playlist', 'channel', 'item'],
        position: 0
      }
    },
    methods: {
      handleTo: function(to) {
        this.position = to;
      }
    }
  }
</script>

<style>
  @import url('https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css');
  @import url('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css');
  @import './assets/stylesheets/main.css';
</style>
