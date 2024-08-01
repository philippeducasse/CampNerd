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
  </div>
  <button @click="goToBookingView">Show all Bookings</button>
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
          }else {
            this.campingSites = data;
          }
        })
        .catch(error => {
          console.error('Error fetching camping sites:', error);
        });
    },
    fetchAllBookings() {
      fetch('/api/bookings')
        .then(response => response.json())
        .then(data => {
          this.bookings = data;
          this.$router.push({
        path: '/bookings',
      });
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
    },
    goToBookingView() {
      console.log('Navigating to bookings view with parameters:', {
        camping_site: this.campingSite,
        start_date: this.startDate,
        end_date: this.endDate
      });
      this.$router.push({
        path: '/bookings',
        query: {
          camping_site: this.campingSite,
          start_date: this.startDate,
          end_date: this.endDate
        }
      });
    }
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
