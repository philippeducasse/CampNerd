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
          <td>
            <button v-if="booking.abrechnungsstatus !== 'abgerechnet'" @click="markAsBilled(booking.id)">
              Mark as Billed
            </button>
            <span v-else>Abgerechnet</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookings: []
    };
  },
  created() {
    this.fetchBookings();
  },
  methods: {
    fetchBookings() {
      fetch('/api/bookings/')
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
          'X-CSRFToken': this.getCookie('csrftoken') // Required for Django CSRF protection
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.fetchBookings();
          }
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
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 8px;
  text-align: left;
}
</style>
