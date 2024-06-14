document.addEventListener('DOMContentLoaded', (event) => {
    const serialPortsSelect = document.getElementById('serial-ports');
    const baudrateSelect = document.getElementById('baudrate');
    const refreshPortsButton = document.getElementById('refresh-ports');
    const connectSerialButton = document.getElementById('connect-serial');
    const temperatureDisplay = document.getElementById('temperature-display');

    async function listSerialPorts() {
        console.log('Listando puertos seriales...');
        try {
            const ports = await navigator.serial.getPorts();
            console.log('Puertos disponibles:', ports);
            serialPortsSelect.innerHTML = '';
            ports.forEach(port => {
                const option = document.createElement('option');
                option.value = port;
                option.textContent = `${port.getInfo().usbVendorId}:${port.getInfo().usbProductId}`;
                serialPortsSelect.appendChild(option);
            });
            if (ports.length === 0) {
                console.log('No hay puertos seriales disponibles.');
                alert('No hay puertos seriales disponibles.');
            }
        } catch (error) {
            console.error('Error al listar puertos seriales:', error);
        }
    }

    async function requestAndConnectSerialPort() {
        const baudrate = parseInt(baudrateSelect.value, 10);
        if (!baudrate) {
            alert('Por favor selecciona un baudrate');
            return;
        }

        try {
            const port = await navigator.serial.requestPort();
            await port.open({ baudRate: baudrate });

            const textDecoder = new TextDecoderStream();
            const readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
            const reader = textDecoder.readable.getReader();

            while (true) {
                const { value, done } = await reader.read();
                if (done) {
                    console.log('Stream cerrado');
                    reader.releaseLock();
                    break;
                }
                if (value) {
                    console.log('Datos recibidos:', value);
                    temperatureDisplay.textContent = value;
                }
            }

            await readableStreamClosed.catch((error) => {
                console.error('Error en la lectura del stream:', error);
            });

            await port.close();
        } catch (error) {
            console.error('Error al conectar al puerto serial:', error);
        }
    }

    refreshPortsButton.addEventListener('click', listSerialPorts);
    connectSerialButton.addEventListener('click', requestAndConnectSerialPort);

    // Inicialmente, popula la lista de puertos seriales
    listSerialPorts();
});
