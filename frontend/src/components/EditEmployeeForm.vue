<template>
  <div class="edit-employee-container">
    <h1 class="title">Edit Employee</h1>
    <form @submit.prevent="updateEmployee" class="form-container">
      <div class="form-group">
        <label for="name">Name:</label>
        <input v-model="employee.name" id="name" type="text" class="input-field" />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="employee.email" id="email" type="email" class="input-field" />
      </div>
      <div class="form-group">
        <label for="phone">Phone:</label>
        <input v-model="employee.phone" id="phone" type="text" class="input-field" />
      </div>
      <div class="form-group">
        <label for="department">Department:</label>
        <input v-model="employee.department" id="department" type="text" class="input-field" />
      </div>
      <button type="submit" class="submit-button">Save Changes</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditEmployeeForm",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      employee: {
        name: "",
        email: "",
        phone: "",
        department: "",
      },
    };
  },
  mounted() {
    this.fetchEmployeeData();
  },
  methods: {
    async fetchEmployeeData() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/employees/${this.id}`);
        this.employee = response.data;
      } catch (error) {
        console.error("Error fetching employee data:", error);
      }
    },

    async updateEmployee() {
      try {
        await axios.put(`http://127.0.0.1:8000/employees/${this.id}`, this.employee);
        this.$router.push('/');
      } catch (error) {
        console.error("Error updating employee:", error);
      }
    },
  },
};
</script>

<style scoped>
.edit-employee-container {
  max-width: 450px;
  margin: 40px auto;
  padding: 20px;
  background: #e0e0e0;
  border-radius: 15px;
  box-shadow: 10px 10px 20px #bebebe, -10px -10px 20px #ffffff;
  font-family: 'Arial', sans-serif;
  text-align: center;
}

.title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: start;
  text-align: left;
}

label {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 5px;
  color: #333;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 10px;
  background: #e0e0e0;
  box-shadow: inset 5px 5px 10px #bebebe, inset -5px -5px 10px #ffffff;
  font-size: 16px;
  color: #333;
  outline: none;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.input-field:focus {
  box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
  transform: scale(1.02);
}

.submit-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  background: #4caf50;
  border: none;
  border-radius: 10px;
  box-shadow: 5px 5px 15px #bebebe, -5px -5px 15px #ffffff;
  cursor: pointer;
  transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
}

.submit-button:hover {
  background: #45a049;
  box-shadow: 3px 3px 10px #bebebe, -3px -3px 10px #ffffff;
  transform: translateY(-2px);
}

.submit-button:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .edit-employee-container {
    padding: 15px;
  }

  .input-field {
    font-size: 14px;
  }

  .submit-button {
    font-size: 14px;
  }
}
</style>
