// Función para consultar la API y actualizar la tabla en tiempo real
function updateTable() {
    axios.get('http://34.228.237.52/api/item')
        .then(function(response) {
            showResponse(response.data); // Llama a la función que genera la tabla
        })
        .catch(function(error) {
            showError(error);
        });
}

// Función para mostrar los datos en una tabla
function showResponse(data) {
    const tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = ''; // Limpiar contenido previo

    const table = document.createElement('table');
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';

    const header = table.createTHead();
    const headerRow = header.insertRow();

    const columns = ["ID", "Status", "IP Cliente", "Nombre", "Fecha", "ID Dispositivo"];
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        th.style.border = '1px solid #ddd';
        th.style.padding = '8px';
        th.style.backgroundColor = '#f2f2f2';
        headerRow.appendChild(th);
    });

    const tbody = document.createElement('tbody');
    table.appendChild(tbody);

    data.data.forEach(item => {
        const row = tbody.insertRow();
        row.insertCell().textContent = item.id;
        row.insertCell().textContent = item.status;
        row.insertCell().textContent = item.ip_client;
        row.insertCell().textContent = item.name;
        row.insertCell().textContent = item.date;
        row.insertCell().textContent = item.id_device;
        
        row.querySelectorAll('td').forEach(cell => {
            cell.style.border = '1px solid #ddd';
            cell.style.padding = '8px';
        });
    });

    tableContainer.appendChild(table);
}

// Función para mostrar errores
function showError(error) {
    console.error('Error:', error);
    const tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = `<p style="color: red;">Error al obtener los datos: ${error.message}</p>`;
}

// Iniciar actualización en tiempo real cada 5 segundos (5000 ms)
setInterval(updateTable, 2000);