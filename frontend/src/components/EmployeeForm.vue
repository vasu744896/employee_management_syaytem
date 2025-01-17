<template>
  <div>
    <h2>Add Employee</h2>
    <form @submit.prevent="addEmployee">
      <input v-model="employee.name" placeholder="Name" required />
      <input v-model="employee.email" placeholder="Email" type="email" required />
      <input v-model="employee.employee_id" placeholder="Employee ID" required />
      <input v-model="employee.phone" placeholder="Phone Number" required />
      <select v-model="employee.department" required>
        <option value="HR">HR</option>
        <option value="Finance">Finance</option>
        <option value="Engineering">Engineering</option>
      </select>
      <button type="submit">Add Employee</button>
    </form>

    <!-- Display added employees (example) -->
    <h3>Employee List</h3>
    <ul>
      <li v-for="emp in employees" :key="emp.employee_id">
        {{ emp.name }} ({{ emp.employee_id }}) - {{ emp.department }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      employee: {
        name: '',
        email: '',
        employee_id: '',
        phone: '',
        department: 'HR',
        manager_id: null,
      },
      employees: [],  // Employee list to store the fetched employees
    };
  },
  mounted() {
    // Fetch employees when the component is mounted
    this.fetchEmployees();
  },
  methods: {
    async addEmployee() {
      try {
        // Log the employee data before sending the request
        console.log('Sending employee data:', this.employee);

        // Sending the data to the backend API
        const response = await axios.post('http://127.0.0.1:8001/employees/', this.employee);

        // Success message and response data log
        alert('Employee added successfully!');
        console.log('Backend Response:', response.data);

        // After successful addition, update the employee list
        this.fetchEmployees(); // Re-fetch the employee list from the backend

        // Optionally, clear the form
        this.resetForm();

      } catch (error) {
        // Error handling and logging
        console.error('Error adding employee:', error);
        alert('Failed to add employee.');
      }
    },

    // Fetch all employees from the backend
    async fetchEmployees() {
      try {
        const response = await axios.get('http://127.0.0.1:8001/employees/');
        this.employees = response.data;  // Update the employees array
        console.log('Fetched employees:', this.employees);
      } catch (error) {
        console.error('Error fetching employees:', error);
      }
    },

    // Reset the form after adding a new employee
    resetForm() {
      this.employee = {
        name: '',
        email: '',
        employee_id: '',
        phone: '',
        department: 'HR',
        manager_id: null,
      };
    }
  },
};
</script>
