<template>
  <div id="app">
    <header>
      <h1>Busca de Operadoras de Saúde</h1>
      <p>Encontre informações sobre operadoras registradas na ANS</p>
    </header>
    <main>
      <SearchBar />
    </main>
    <footer>
      <p>&copy; 2025 - Processo Seletivo da IntuitiveCare - Nicholas Stuart</p>
    </footer>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue';

export default {
  name: 'App',
  components: {
    SearchBar
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f7fa;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  text-align: center;
  padding: 2rem 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
  font-size: 0.9rem;
}
</style>