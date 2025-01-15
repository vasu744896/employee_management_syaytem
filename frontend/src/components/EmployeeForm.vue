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
          manager_id: null
        }
      };
    },
    methods: {
      async addEmployee() {
        try {
          const response = await axios.post('http://127.0.0.1:8001/employees/', this.employee);
          alert('Employee added successfully!');
          console.log(response.data);
        } catch (error) {
          console.error('Error adding employee:', error);
          alert('Failed to add employee.');
        }
      }
    }
  };
  </script>
  