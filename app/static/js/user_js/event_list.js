document.getElementById('category-select').addEventListener('change', function() {
    const categoryId = this.value;
    const url = new URL(window.location);
    if (categoryId) {
        url.searchParams.set('categoria', categoryId);
    } else {
        url.searchParams.delete('categoria');
    }
    window.location.href = url.toString();
});