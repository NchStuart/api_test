<template>
  <div class="search-container">
    <div class="search-box">
      <input
        v-model="query"
        @input="debounceSearch"
        placeholder="Digite o nome, CNPJ, Registro ou Nome fantasia da operadora"
        type="text"
        class="search-input"
      />
      <span class="search-icon">🔍</span>
    </div>
    <div v-if="loading" class="loading">Carregando resultados...</div>
    <div v-else-if="paginatedResults.length > 0" class="results-table">
      <table>
        <thead>
          <tr>
            <th>Registro ANS</th>
            <th>CNPJ</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>Modalidade</th>
            <th>Data de Registro</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in paginatedResults" :key="result.Registro_ANS">
            <td>{{ result.Registro_ANS }}</td>
            <td>{{ result.CNPJ }}</td>
            <td>{{ result.Razao_Social }}</td>
            <td>{{ result.Nome_Fantasia || '-' }}</td>
            <td>{{ result.Modalidade }}</td>
            <td>{{ result.Data_Registro_ANS }}</td>
          </tr>
        </tbody>
      </table>
      <div class="pagination" v-if="totalPages > 1">
        <button
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="pagination-btn"
        >
          Anterior
        </button>
        <span>Página {{ currentPage }} de {{ totalPages }}</span>
        <button
          :disabled="currentPage === totalPages"
          @click="currentPage++"
          class="pagination-btn"
        >
          Próxima
        </button>
      </div>
    </div>
    <p v-else-if="query && !loading" class="no-results">
      Nenhum resultado encontrado para "{{ query }}".
    </p>
    <p v-else-if="!loading && results.length === 0" class="no-results">
      Nenhuma operadora disponível.
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SearchBar',
  data() {
    return {
      query: '',
      results: [],
      loading: false,
      debounceTimer: null,
      currentPage: 1,
      itemsPerPage: 20
    };
  },
  mounted() {
    this.loadAllOperadoras();
  },
  computed: {
    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.results.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.results.length / this.itemsPerPage);
    }
  },
  methods: {
    async loadAllOperadoras() {
      this.loading = true;
      this.currentPage = 1;
      try {
        const response = await axios.get('http://localhost:8000/operadoras');
        this.results = response.data.operadoras;
      } catch (error) {
        console.error('Erro ao carregar operadoras:', error);
        this.results = [];
      } finally {
        this.loading = false;
      }
    },
    debounceSearch() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(this.search, 500);
    },
    async search() {
      if (!this.query.trim()) {
        this.loadAllOperadoras();
        return;
      }

      this.loading = true;
      this.currentPage = 1;
      try {
        const response = await axios.get('http://localhost:8000/buscar', {
          params: { query: this.query }
        });
        this.results = response.data.resultados;
      } catch (error) {
        console.error('Erro na busca:', error);
        this.results = [];
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.search-container {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.search-box {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 15px;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 25px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #007bff;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: #666;
}

.loading {
  text-align: center;
  color: #007bff;
  font-size: 1.1rem;
}

.results-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #007bff;
  color: white;
  font-weight: 600;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f5f9;
}

.no-results {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
}

.pagination-btn {
  padding: 8px 16px;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  th, td {
    font-size: 0.9rem;
    padding: 10px;
  }

  .search-container {
    padding: 1rem;
  }

  .pagination {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>