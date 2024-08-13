// static/js/product_list.js

document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('sort_by');
    
    sortSelect.addEventListener('change', function() {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('sort', this.value);
        window.location.search = urlParams.toString();
    });
});