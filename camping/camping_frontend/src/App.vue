<template>
  <div id="app">
    <BillingView />
    <BookingList />
  </div>
</template>

<script>
import BillingView from './components/BillingView.vue';
import BookingList from './components/BookingList.vue';

export default {
  name: 'App',
  components: {
    BillingView,
    BookingList
  },
};
</script>

<style>
</style>
