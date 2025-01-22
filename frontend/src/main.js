import { createApp } from 'vue'; // Use createApp to initialize Vue 3
import App from './App.vue'; // Import the App component
import router from './router'; // Import the router configuration

// Create the Vue app and mount it
createApp(App)
  .use(router) // Use the router
  .mount('#app'); // Mount to the DOM
