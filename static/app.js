// Lê favoritos do localStorage e aplica a classe "active" nos botões correspondentes
function loadFavorites() {
  const favorites = JSON.parse(localStorage.getItem("favoritos")) || [];

  favorites.forEach((idString) => {
    const card = document.querySelector(`.curso-card[data-id="${idString}"]`);
    if (!card) return;

    const btn = card.querySelector(".favorite-btn");
    if (!btn) return;

    btn.classList.add("active");
    // opcional: garantir ícone correto
    btn.textContent = "★";
  });
}

// Alterna o estado de favorito de um curso (salva no localStorage)
function toggleFavorite(id) {
  const idString = String(id);
  const favorites = JSON.parse(localStorage.getItem("favoritos")) || [];

  const index = favorites.indexOf(idString);
  const willBeFavorite = index === -1;

  if (willBeFavorite) {
    favorites.push(idString);
  } else {
    favorites.splice(index, 1);
  }

  localStorage.setItem("favor
