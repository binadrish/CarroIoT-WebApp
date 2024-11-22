// Obtener referencia de la zona de respuesta
const responseContainer = document.getElementById('response');

// Función para manejar las respuestas
function showResponse(responseData) {
    responseContainer.innerHTML = JSON.stringify(responseData, null, 2);
}

// Función para manejar los errores
function showError(error) {
    responseContainer.innerHTML = `Error: ${error}`;
}


function insertdb(event) {
    const buttonId = 1;
    const newStatus = event.target.getAttribute('status');  // Obtiene el estado desde el atributo 'status'
    const newIp = "192.168.1.10"; 
    const newName = "Carro1"; 
    const newDate = "2024-11-13 15:47:31"; 
    const newDevice = "R5cCI6IkpXVCJ9"; 

    axios.post('http://34.228.237.52/api/item', { id: buttonId, status: newStatus, ip_client:newIp, name:newName, date:newDate, ip_device:newDevice })
        .then(function (response) {
            showResponse(response.data);
        })
        .catch(function (error) {
            showError(error);
        })
        .finally(function () {
            console.log('Petición finalizada');
        });
}

// Agrega event listeners a cada botón para que llamen a updateDatabase con el evento
document.getElementById('adelante').addEventListener('click', insertdb);
document.getElementById('atras').addEventListener('click', insertdb);
document.getElementById('detenerse').addEventListener('click', insertdb);
document.getElementById('vuelta_izquierda').addEventListener('click', insertdb);
document.getElementById('vuelta_derecha').addEventListener('click', insertdb);
document.getElementById('giro_izquierda').addEventListener('click', insertdb);
document.getElementById('giro_derecha').addEventListener('click', insertdb);
document.getElementById('demo').addEventListener('click', insertdb);

