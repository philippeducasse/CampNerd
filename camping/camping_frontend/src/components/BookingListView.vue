<template>
  <div>
    <h1>Booking View</h1>
    <!-- <p v-if="!campingSite">No camping site selected</p> -->
    <!-- <div v-else> -->
      <p>Showing bookings for: {{ campingSite.name }}</p>
      <button @click="fetchAllBookings">Show All Bookings</button>
      <table border="1">
        <thead>
          <tr>
            <th>Booking Number</th>
            <th>Campingplatz</th>
            <th>Status</th>
            <th>Abrechnungsstatus</th>
            <th>Price</th>
            <th>Commission Rate</th>
            <th>Total Commission</th>
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
              <input type="number" v-model="booking.commission_rate" step="0.1" />
              <button @click="updateCommissionRate(booking.id, booking.commission_rate)">Update</button>
            </td>
            <td>{{ booking.total_commission }}</td>
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
              <button @click="createInvoice(booking.id)">
                Create Invoice
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
        <BookingLogs :logs="logs" />
      </div>
    <!-- </div> -->
  </div>
</template>

<script>
import BookingLogs from './BookingLogs.vue';

export default {
  name: 'BookingListView',
  components: {
    BookingLogs
  },
  data() {
    return {
      bookings: [],
      logs: [],
      campingSite: null,
      startDate: '',
      endDate: ''
    };
  },
  created() {
    this.fetchQueryParams();
    this.fetchBookings();
  },
  methods: {
    fetchQueryParams() {
      this.campingSite = this.$route.query.camping_site;
      this.startDate = this.$route.query.start_date;
      this.endDate = this.$route.query.end_date;
    },
    fetchBookings() {
      console.log(this.campingSite, this.startDate, this.endDate)
      fetch(`/api/bookings?camping_site=${this.campingSite}&start_date=${this.startDate}&end_date=${this.endDate}`)
      // fetch('/api/bookings')
        .then(response => response.json())
        .then(data => {
          this.bookings = data;
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    fetchAllBookings() {
      fetch('/api/bookings')
        .then(response => response.json())
        .then(data => {
          this.bookings = data;
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    updateCommissionRate(id, rate) {
      fetch(`/api/bookings/${id}/update_commission_rate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        body: JSON.stringify({ commission_rate: rate }),
        credentials: 'include',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(() => {
          this.fetchBookings();
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    markAsBilled(id) {
      fetch(`/api/bookings/${id}/mark_as_billed/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(() => {
          this.fetchBookings();
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    cancelBooking(id) {
      fetch(`/api/bookings/${id}/cancel/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(() => {
          this.fetchBookings();
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    createInvoice(bookingId) {
      fetch(`/api/bookings/${bookingId}/create_invoice/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include',
      })
        .then(response => response.json())
        .then(data => {
          this.message = data.message;
          this.fetchBookings();
        })
        .catch(error => {
          console.error('Error creating invoice:', error);
        });
    },
    creditBooking(id) {
      fetch(`/api/bookings/${id}/credit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        credentials: 'include',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(() => {
          this.fetchBookings();
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    viewLogs(id) {
      fetch(`/api/bookings/${id}/logs/`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          this.logs = data;
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
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
/* Add any specific styles you need here */
</style>
