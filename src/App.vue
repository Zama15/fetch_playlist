<template>
  <component
    v-bind:is="screens[position]"
    v-bind:data="data"
    @to="handleTo"
    @data="setData"
  />
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
        position: 0,
        data: {},
      }
    },
    provide() {
      return {
        formatDate: this.formatDate,
        strim: this.strim
      }
    },
    methods: {
      handleTo: function(to) {
        this.position = to;
      },
      setData: function(data) {
        this.data = data;
      },
      formatDate: function(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
      },
      strim: function(string, start, width, trim_maker = "") {
        width -= trim_maker.length;

        if (string.length > width) {
          return string.substring(start, width) + trim_maker;
        } else {
          return string;
        }
      }
    },
  }
</script>

<style>
  @import url('https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css');
  @import url('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css');
  @import './assets/stylesheets/main.css';
</style>
