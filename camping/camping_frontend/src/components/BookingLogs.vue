<template>
    <div>
      <h2>Logs</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Field Changed</th>
            <th>Old Value</th>
            <th>New Value</th>
            <th>Date</th>
            <th>User</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ log.field_changed }}</td>
            <td>{{ log.old_value }}</td>
            <td>{{ log.new_value }}</td>
            <td>{{ log.date }}</td>
            <td>{{ log.user }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BookingLogs',
    props: {
      logs: {
        type: Array,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add any specific styles you need here */
  </style>
  