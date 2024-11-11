async function fetchData() {
    const input = document.getElementById('queryInput').value;
    const response = await fetch(`/query?input=${encodeURIComponent(input)}`);
    const data = await response.json();
    
    const container = document.getElementById('mynetwork');
    // provide the data in the vis format
    let network_data = {
        nodes: data.neigh.nodes,
        edges: data.neigh.edges
    };

    console.log(network_data);
    var options = {
        // Enable this to make the endpoints smaller/larger
        edges: {
            arrows: {
                to: {
                    scaleFactor: 0.5
                }
            }
        }
    };
    // Rellenar el infoContainer con los sinónimos de cada acepción y actualizar el título
    const infoContainer = document.getElementById('infoContainer');
    const aceptions = data.asp.aseptions;
    const word = data.asp.key;
    
    // Limpiar el contenido previo de infoContainer y actualizar el título
    infoContainer.innerHTML = `<h2>Acepción de la palabra "${input}"</h2>`;

    // Iterar sobre cada acepción y mostrar sus sinónimos
    aceptions.forEach((aception, index) => {
        const synonims = aception.synonims;

        if (synonims.length > 0) {
            // Crear un elemento para cada conjunto de sinónimos
            const aceptionElement = document.createElement('div');
            aceptionElement.classList.add('aception');
            aceptionElement.innerHTML = `<h3>Acepción ${index + 1}</h3><p>Sinónimos: ${synonims.join(', ')}.</p>`;
            infoContainer.appendChild(aceptionElement);
        }
    });
    // initialize your network!
    let network = new vis.Network(container, network_data, options)
}