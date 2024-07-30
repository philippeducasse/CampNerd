<template>
    <div>
      <h1>Generate Billing</h1>
      <form @submit.prevent="generateBilling">
        <label for="camping_site">Camping Site:</label>
        <select v-model="campingSite" id="camping_site">
          <option v-for="site in campingSites" :key="site.id" :value="site.id">
            {{ site.name }}
          </option>
        </select>
        <label for="start_date">Start Date:</label>
        <input type="date" v-model="startDate" id="start_date" required>
        <label for="end_date">End Date:</label>
        <input type="date" v-model="endDate" id="end_date" required>
        <button type="submit">Generate Billing</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        campingSites: [],
        campingSite: '',
        startDate: '',
        endDate: '',
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
          });
      },
      generateBilling() {
        fetch('/api/billing/', {
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
        })
          .then(response => response.json())
          .then(data => {
            this.message = data.message;
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
  </style>
  