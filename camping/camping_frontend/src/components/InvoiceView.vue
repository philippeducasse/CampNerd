<template>
    <div>
      <h1>Invoice Management</h1>
      <div>
        <label for="billing_date">Billing Date:</label>
        <input type="date" v-model="billingDate" id="billing_date" required>
        <button @click="generateInvoices">Generate Invoices</button>
      </div>
      <div>
        <button @click="displayUnsentInvoices">Display Unsent Invoices</button>
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
            </tr>
          </tbody>
        </table>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InvoiceView',
    data() {
      return {
        billingDate: '',
        invoices: [],
        message: '',
      };
    },
    methods: {
      generateInvoices() {
        fetch('/api/generate_invoices/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          body: JSON.stringify({
            billing_date: this.billingDate,
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
      createCredits() {
        fetch('/api/create_credits/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          credentials: 'include', // Ensure cookies are sent with the request
        })
          .then(response => response.json())
          .then(data => {
            this.message = data.message;
          })
          .catch(error => {
            console.error('Error creating credits:', error);
          });
      },
      displayUnsentInvoices() {
        fetch('/api/unsent_invoices/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          credentials: 'include', // Ensure cookies are sent with the request
        })
          .then(response => response.json())
          .then(data => {
            this.invoices = data.invoices;
          })
          .catch(error => {
            console.error('Error displaying unsent invoices:', error);
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
  /* Add any specific styles you need here */
  </style>
  