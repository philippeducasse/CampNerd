import { createRouter, createWebHistory } from 'vue-router';
import StartPageView from '../components/StartPageView.vue';
import BookingListView from '../components/BookingListView.vue';
import InvoiceView from '../components/InvoiceView.vue';
import LogsPage from '../components/LogsPage.vue';

const routes = [
  {
    path: '/',
    name: 'StartPageView',
    component: StartPageView
  },
  {
    path: '/bookings',
    name: 'BookingListView',
    component: BookingListView
  },
  {
    path: '/invoices',  
    name: 'InvoiceView',
    component: InvoiceView
  },
  {
    path: '/logs',
    name: 'LogsPage',
    component: LogsPage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
