<template>
  <div>
    <h1>Employee List</h1>
    <input
      v-model="searchQuery"
      placeholder="Search by Name or ID"
      style="margin-bottom: 20px; padding: 8px; width: 300px;"
    />
    <button @click="addEmployee" style="padding: 10px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer;">Add Employee</button>

    <table border="1" cellspacing="0" cellpadding="10" style="width: 100%; border-collapse: collapse;">
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
            <button @click="editEmployee(emp.employee_id)" style="padding: 5px 10px; background-color: #2196F3; color: white; border: none; cursor: pointer;">Edit</button>
            <button @click="deleteEmployee(emp.employee_id)" style="padding: 5px 10px; background-color: #f44336; color: white; border: none; cursor: pointer;">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Error message display -->
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      employees: [], // List of all employees fetched from the backend
      searchQuery: "", // Search query input by the user
      errorMessage: "", // Error message if fetching fails
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
    // Fetches the list of employees from the backend API
    async fetchEmployees() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/employees");
        this.employees = response.data; // Populate employees with the fetched data
        this.errorMessage = ""; // Clear any previous errors
      } catch (error) {
        console.error("Error fetching employees:", error);
        this.errorMessage = "There was an issue fetching the employees."; // Display error message
      }
    },

    // Navigates to the edit employee page
    editEmployee(id) {
      this.$router.push(`/edit-employee/${id}`);
    },

    // Deletes an employee from the backend
    async deleteEmployee(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/employees/${id}`);
        this.fetchEmployees(); // Refresh the employee list after deletion
      } catch (error) {
        console.error("Error deleting employee:", error);
        this.errorMessage = "There was an issue deleting the employee."; // Display error message
      }
    },

    // Redirects to the add employee form (you can define this route as needed)
    addEmployee() {
      this.$router.push("/add-employee"); // Update the path if necessary for your add employee page
    },
    beforeRouteEnter(to, from, next) {
  next(vm => vm.fetchEmployees());
},

  },
};
</script>

<style scoped>
table th,
table td {
  padding: 8px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}

button:hover {
  opacity: 0.8;
}

input {
  margin-bottom: 10px;
  padding: 8px;
  width: 300px;
}
</style>
