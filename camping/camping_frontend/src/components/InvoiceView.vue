<template>
  <div>
    <h1>Invoice Management</h1>
    <div>
      <label for="camping_site">Camping Site:</label>
      <select v-model="campingSite" id="camping_site" required>
        <option v-for="site in campingSites" :key="site.id" :value="site.id">
          {{ site.name }}
        </option>
      </select>
      <label for="start_date">Start Date:</label>
      <input type="date" v-model="startDate" id="start_date" required>
      <label for="end_date">End Date:</label>
      <input type="date" v-model="endDate" id="end_date" required>
      <button @click="generateInvoices">Generate Invoices</button>
    </div>
    <div v-if="invoices.length">
      <h2>Invoices</h2>
      <table>
        <thead>
          <tr>
            <th>Booking ID</th>
            <th>Booking Number</th>
            <th>Price</th>
            <th>Commission Rate</th>
            <th>Total Commission</th>
            <th>Customer Name</th>
            <th>Departure Date</th>
            <th>Camping Site</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="invoice in invoices" :key="invoice.booking_id">
            <td>{{ invoice.booking_id }}</td>
            <td>{{ invoice.booking_number }}</td>
            <td>{{ invoice.price }}</td>
            <td>{{ invoice.commission_rate }}</td>
            <td>{{ invoice.total_commission }}</td>
            <td>{{ invoice.customer_name }}</td>
            <td>{{ invoice.departure_date }}</td>
            <td>{{ invoice.camping_site_name }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="sendAllInvoices">Send All Invoices</button>
    </div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'InvoiceView',
  data() {
    return {
      campingSites: [],
      campingSite: '',
      startDate: '',
      endDate: '',
      invoices: [],
      message: '',
    };
  },
  created() {
    this.fetchCampingSites();
  },
  methods: {
    fetchCampingSites() {
      fetch('/api/camping_sites/')
        .then(response => response.json())
        .then(data => {
          this.campingSites = data;
        })
        .catch(error => {
          console.error('Error fetching camping sites:', error);
        });
    },
    generateInvoices() {
      fetch('/api/generate_invoices/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken'),
        },
        body: JSON.stringify({
          camping_site: this.campingSite,
          start_date: this.startDate,
          end_date: this.endDate,
        }),
        credentials: 'include', // Ensure cookies are sent with the request
      })
        .then(response => response.json())
        .then(data => {
          this.message = data.message;
          if (data.status === 'success') {
            this.invoices = data.invoices;
          }
        })
        .catch(error => {
          console.error('Error generating invoices:', error);
        });
    },
    sendAllInvoices() {
      // Implement the logic to send all invoices here
      console.log('Sending all invoices:', this.invoices);
      // Example: make an API call to send the invoices
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
/* Add any specific styles you need here */
</style>
