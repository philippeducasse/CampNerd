<template>
  <div>
    <h1>Welcome to the Camping Management System</h1>
    <form @submit.prevent="goToBookingView">
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
      <button type="submit">Go to Booking View</button>
    </form>
    <button @click="goToAllBookings">Show all Bookings</button>
  </div>
</template>

<script>
export default {
  name: 'StartPageView',
  data() {
    return {
      campingSites: [],
      campingSite: '',
      startDate: '',
      endDate: ''
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
          if(data.length === 0){
            console.log('No camping sites found');
          } else {
            this.campingSites = data;
          }
        })
        .catch(error => {
          console.error('Error fetching camping sites:', error);
        });
    },
    goToBookingView() {
      const query = {};
      if (this.campingSite) query.camping_site = this.campingSite;
      if (this.startDate) query.start_date = this.startDate;
      if (this.endDate) query.end_date = this.endDate;

      this.$router.push({
        path: '/bookings',
        query: query
      });
    },
    goToAllBookings() {
    this.$router.push('/bookings');
  },
  }
};
</script>

<style scoped>
nav ul {
  list-style-type: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin-right: 20px;
}
</style>
