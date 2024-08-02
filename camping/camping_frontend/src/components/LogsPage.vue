<template>
    <div>
      <h1>Logs</h1>
      <BookingLogs :logs="logs" />
    </div>
  </template>
  
  <script>
  import BookingLogs from '@/components/BookingLogs.vue'
  
  export default {
    name: 'LogsPage',
    components: {
      BookingLogs
    },
    data() {
      return {
        logs: []
      };
    },
    created() {
      this.fetchLogs();
    },
    methods: {
      fetchLogs() {
        fetch('/api/logs/')
          .then(response => response.json())
          .then(data => {
            this.logs = data;
          })
          .catch(error => {
            console.error('Error fetching logs:', error);
          });
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add any specific styles you need here */
  </style>
  