<template>
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/billing">Billing View</router-link></li>
        <li><router-link to="/bookings">Booking View</router-link></li>
        <li><router-link to="/invoice">Create Invoice</router-link></li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavBar'
  };
  </script>
  
  <style scoped>
  nav {
    background-color: #333;
    color: white;
    padding: 1rem;
  }
  
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 1rem;
  }
  
  li {
    display: inline;
  }
  
  a {
    color: white;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>
  