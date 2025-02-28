document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.querySelector('input[name="q"]');
    const levelSelect = document.querySelector('select[name="level"]');
    const searchResults = document.getElementById('search-results');

    function performSearch() {
        const query = searchInput.value;
        const level = levelSelect.value;
        const params = new URLSearchParams({ q: query, level: level }).toString();
        console.log('Отправка запроса:', params); // Логирование внутри функции

        fetch(`${searchForm.action}?${params}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            searchResults.innerHTML = html;
        })
        .catch(error => console.error('Ошибка:', error));
    }

    // События для поля ввода и выпадающего списка
    searchInput.addEventListener('input', performSearch);
    levelSelect.addEventListener('change', performSearch);
});