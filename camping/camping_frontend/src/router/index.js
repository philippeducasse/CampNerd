import { createRouter, createWebHistory } from 'vue-router';
import StartPageView from '../components/StartPageView.vue';
import BillingView from '../components/BillingView.vue';
import BookingListView from '../components/BookingListView.vue';
import InvoiceView from '../components/InvoiceView.vue';

const routes = [
  {
    path: '/',
    name: 'StartPageView',
    component: StartPageView
  },
  {
    path: '/billing',
    name: 'BillingView',
    component: BillingView
  },
  {
    path: '/bookings',
    name: 'BookingListView',
    component: BookingListView
  },
  {
    path: '/invoice',
    name: 'InvoiceView',
    component: InvoiceView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
