<template>
    <div>
      <h1>Employee List</h1>
      <input v-model="searchQuery" placeholder="Search by Name or ID" />
  
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Employee ID</th>
            <th>Phone</th>
            <th>Manager</th>
            <th>Department</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in filteredEmployees" :key="emp.id">
            <td>{{ emp.name }}</td>
            <td>{{ emp.email }}</td>
            <td>{{ emp.employee_id }}</td>
            <td>{{ emp.phone }}</td>
            <td>{{ emp.manager_id || 'None' }}</td>
            <td>{{ emp.department }}</td>
            <td>
              <button @click="editEmployee(emp.id)">Edit</button>
              <button @click="deleteEmployee(emp.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        employees: [],
        searchQuery: '',
      };
    },
    computed: {
      filteredEmployees() {
        return this.employees.filter(emp =>
          emp.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          emp.employee_id.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
    },
    mounted() {
      this.fetchEmployees();
    },
    methods: {
      async fetchEmployees() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/employees/');
          this.employees = response.data;
        } catch (error) {
          console.error("Error fetching employees:", error);
        }
      },
      editEmployee(id) {
        this.$router.push(`/edit-employee/${id}`);
      },
      async deleteEmployee(id) {
        try {
          await axios.delete(`http://127.0.0.1:8000/employees/${id}`);
          this.fetchEmployees(); // Refresh the list
        } catch (error) {
          console.error("Error deleting employee:", error);
        }
      }
    }
  };
  </script>
  