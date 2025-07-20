document.addEventListener('DOMContentLoaded', function() {
    const assetTypeFilter = document.getElementById('assetTypeFilter');
    const statusFilter = document.getElementById('statusFilter');
    const manufacturerFilter = document.getElementById('manufacturerFilter');
    const searchInput = document.getElementById('searchInput');
    const tableRows = document.querySelectorAll('.asset-row');

    function filterTable() {
        const assetType = assetTypeFilter.value;
        const status = statusFilter.value;
        const manufacturer = manufacturerFilter.value;
        const searchTerm = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
            const rowAssetType = row.getAttribute('data-type');
            const rowStatus = row.getAttribute('data-status');
            const rowManufacturer = row.getAttribute('data-manufacturer');
            const rowText = row.textContent.toLowerCase();

            const matchesAssetType = !assetType || rowAssetType === assetType;
            const matchesStatus = !status || rowStatus === status;
            const matchesManufacturer = !manufacturer || rowManufacturer === manufacturer;
            const matchesSearch = !searchTerm || rowText.includes(searchTerm);

            if (matchesAssetType && matchesStatus && matchesManufacturer && matchesSearch) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    assetTypeFilter.addEventListener('change', filterTable);
    statusFilter.addEventListener('change', filterTable);
    manufacturerFilter.addEventListener('change', filterTable);
    searchInput.addEventListener('input', filterTable);
}); 