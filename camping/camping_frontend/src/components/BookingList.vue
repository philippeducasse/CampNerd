<template>
  <div>
    <h1>Bookings</h1>
    <table border="1">
      <thead>
        <tr>
          <th>Booking Number</th>
          <th>Campingplatz</th>
          <th>Status</th>
          <th>Abrechnungsstatus</th>
          <th>Price</th>
          <th>Commission Rate</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="booking in bookings" :key="booking.id">
          <td>{{ booking.booking_number }}</td>
          <td>{{ booking.campingplatz_id }}</td>
          <td>{{ booking.status }}</td>
          <td>{{ booking.abrechnungsstatus }}</td>
          <td>{{ booking.price }}</td>
          <td>{{ booking.commission_rate }}</td>
          <td>
            <button v-if="booking.abrechnungsstatus !== 'abgerechnet'" @click="markAsBilled(booking.id)">
              Abrechnen
            </button>
            <button v-if="booking.abrechnungsstatus !== 'storniert'" @click="cancelBooking(booking.id)">
              Stornieren
            </button>
            <button v-if="booking.abrechnungsstatus !== 'gutschreiben'" @click="creditBooking(booking.id)">
              Gutschreiben
            </button>
            <button @click="viewLogs(booking.id)">
              View Logs
            </button>
            <span v-if="booking.abrechnungsstatus === 'abgerechnet'">Abgerechnet</span>
            <span v-if="booking.abrechnungsstatus === 'storniert'">Storniert</span>
            <span v-if="booking.abrechnungsstatus === 'gutschreiben'">Gutschreiben</span>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="logs.length">
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookings: [],
      logs: []
    };
  },
  created() {
    this.fetchBookings();
  },
  methods: {
    fetchBookings() {
      fetch('/api/bookings/', {
        credentials: 'include' // Ensure cookies are sent with the request
      })
        .then(response => response.json())
        .then(data => {
          this.bookings = data;
        });
    },
    markAsBilled(id) {
      fetch(`/api/bookings/${id}/mark_as_billed/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include', // Ensure cookies are sent with the request
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.fetchBookings();
          }
        });
    },
    cancelBooking(id) {
      fetch(`/api/bookings/${id}/cancel/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include', // Ensure cookies are sent with the request
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.fetchBookings();
          }
        });
    },
    creditBooking(id) {
      fetch(`/api/bookings/${id}/credit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include', // Ensure cookies are sent with the request
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.fetchBookings();
          }
        });
    },
    viewLogs(id) {
      fetch(`/api/bookings/${id}/logs/`, {
        method: 'GET',
        credentials: 'include' // Ensure cookies are sent with the request
      })
        .then(response => response.json())
        .then(data => {
          this.logs = data;
        });
    },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
