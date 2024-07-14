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

  export default {
    components: {
      home,
      playlist,
      channel,
    },
    data: function() {
      return {
        screens: ['home', 'playlist', 'channel'],
        position: 0,
        data: {},
      }
    },
    provide() {
      return {
        strim: this.strim,
        formatDate: this.formatDate,
        formatNumber: this.formatNumber,
        formatPeriodTime: this.formatPeriodTime,
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
          month: 'short',
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
      },
      formatNumber: function(number) {
        return new Intl.NumberFormat('en-US', {
          notation: 'compact',
          maximumFractionDigits: 1
        }).format(number);
      },
      formatPeriodTime: function(duration) {
        const period = duration.match(/(\d+)(?=[MHS])/g);
        const time = {
          hours: period.length === 3 ? period[0] : 0,
          minutes: period.length === 3 ? period[1] : period[0],
          seconds: period.length === 3 ? period[2] : period[1],
        };

        return `${time.hours ? `${time.hours}:` : ''}${time.minutes ? `${time.minutes}:` : ''}${time.seconds ? `${time.seconds}` : ''}`;
      },
    },
  }
</script>

<style>
  @import url('https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css');
  @import url('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css');
  @import './assets/stylesheets/main.css';
</style>
