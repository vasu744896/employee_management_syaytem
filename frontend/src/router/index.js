import { createRouter, createWebHistory } from 'vue-router';

// Import components
import EmployeeList from '../components/EmployeeList.vue';
import EditEmployeeForm from '../components/EditEmployeeForm.vue';

// Define routes
const routes = [
  {
    path: '/',
    name: 'EmployeeList',
    component: EmployeeList,
  },
  {
    path: '/edit-employee/:id',
    name: 'EditEmployee',
    component: EditEmployeeForm,
    props: true,
    // Optional: Add a navigation guard to check if the ID exists
    beforeEnter: (to, from, next) => {
      if (to.params.id) {
        next(); // Allow navigation if an ID is provided
      } else {
        next({ name: 'EmployeeList' }); // Redirect to the list if no ID
      }
    },
  },
];

// Create and export the router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
