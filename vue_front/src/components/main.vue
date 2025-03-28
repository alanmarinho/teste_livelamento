<script setup>
import { ref } from 'vue';
const searchTerm = ref('');
const results = ref([]);
const API_BASE = 'http://127.0.0.1:5000';

const fetchData = async () => {
  if (!searchTerm.value) return;

  try {
    console.log('data', searchTerm.value);
    const response = await fetch(`${API_BASE}/search_operadora?rs=${searchTerm.value}`);
    const data = await response.json();
    results.value = data;
    console.log(data);
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
  }
};
const handleSubmit = (event) => {
  console.log('testes');
  event.preventDefault();
  fetchData();
};
</script>
<template>
  <div class="box">
    <div class="main">
      <h3>Buscar Operadora</h3>
      <form class="form" @submit="handleSubmit">
        <input v-model="searchTerm" type="text" placeholder="Digite algo..." class="input" />
        <input type="submit" value="Pesquisar" class="submit-btn" />
      </form>

      <table v-if="results.length" class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Razão Social</th>
            <th>Registro ANS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in results" :key="index">
            <td>{{ item.id }}</td>
            <td>{{ item.Razao_Social }}</td>
            <td>{{ item.Registro_ANS }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.table {
  width: 100%;
  max-width: 800px;
  margin-top: 20px;
  padding: 3px;
  border-collapse: collapse;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  background-color: black;
  overflow: hidden;
}

.table thead {
  background-color: rgba(148, 148, 148, 0.1);
  color: white;
  text-align: left;
}

.table th {
  padding: 12px;
  font-size: 16px;
}

.table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.form {
  display: flex;
  gap: 10px;
}
.submit-btn {
  padding: 0.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}
.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  outline: none;
  transition: 0.3s;
}
.box {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.4rem;
}
.main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 80%;
}
</style>
