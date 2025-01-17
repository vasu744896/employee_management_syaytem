<template>
  <div>
    <h1>Employee List</h1>
    <input
      v-model="searchQuery"
      placeholder="Search by Name or ID"
      style="margin-bottom: 20px; padding: 8px; width: 300px;"
    />

    <table border="1" cellspacing="0" cellpadding="10">
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
        <!-- If no employees match the search query, show a message -->
        <tr v-if="filteredEmployees.length === 0">
          <td colspan="7">No employees found.</td>
        </tr>

        <!-- List employees if available -->
        <tr v-for="emp in filteredEmployees" :key="emp.employee_id">
          <td>{{ emp.name }}</td>
          <td>{{ emp.email }}</td>
          <td>{{ emp.employee_id }}</td>
          <td>{{ emp.phone }}</td>
          <td>{{ emp.manager_id || 'None' }}</td>
          <td>{{ emp.department }}</td>
          <td>
            <button @click="editEmployee(emp.employee_id)">Edit</button>
            <button @click="deleteEmployee(emp.employee_id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

axios.defaults.timeout = 5000;  // Set timeout for requests
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

export default {
  data() {
    return {
      employees: [], // List of all employees fetched from the backend
      searchQuery: "", // Search query input by the user
    };
  },
  computed: {
    // Filters employees based on name or employee ID
    filteredEmployees() {
      return this.employees.filter(
        (emp) =>
          emp.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          emp.employee_id.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  mounted() {
    // Fetch the employee list when the component is mounted
    this.fetchEmployees();
  },
  methods: {
    async fetchEmployees() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/employees");
        this.employees = response.data; // Populate employees with the fetched data
        console.log("Fetched employees:", this.employees);
      } catch (error) {
        console.error("Error fetching employees:", error);
      }
    },
    editEmployee(id) {
      // Navigate to the edit page for the selected employee
      this.$router.push(`/edit-employee/${id}`);
    },
    async deleteEmployee(id) {
      try {
        console.log("Deleting employee with ID:", id);
        await axios.delete(`http://127.0.0.1:8000/employees/${id}`);
        this.fetchEmployees(); // Refresh the employee list after deletion
      } catch (error) {
        console.error("Error deleting employee:", error);
      }
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

table th,
table td {
  text-align: left;
  padding: 8px;
}

table th {
  background-color: #f2f2f2;
}

input {
  margin-bottom: 10px;
}
</style>
