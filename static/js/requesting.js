// Asegúrate de que el DOM esté completamente cargado antes de añadir los event listeners
document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('queryInput');
    
    // Añadir un event listener para detectar la tecla "Enter"
    queryInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            fetchData();
        }
    });
});

async function fetchData() {
    const input = document.getElementById('queryInput').value.trim();
    if (!input) {
        // Opcional: Manejar el caso en que el input está vacío
        return;
    }

    try {
        const response = await fetch(`/query?input=${encodeURIComponent(input)}`);
        const data = await response.json();
        const infoContainer = document.getElementById('infoContainer');
        const container = document.getElementById('mynetwork');

        if (data.status !== 0) {
            infoContainer.innerHTML = `<h2>No se encontraron resultados para la palabra "${input}"</h2>`;
            container.innerHTML = '';
            return;
        }

        // Preparar los datos para vis-network
        let network_data = {
            nodes: data.neigh.nodes,
            edges: data.neigh.edges
        };

        console.log(network_data);

        const options = {
            edges: {
                arrows: {
                    to: {
                        scaleFactor: 0.5
                    }
                }
            }
        };

        // Rellenar el infoContainer con las acepciones y sinónimos
        const aceptions = data.asp.aseptions;    
        infoContainer.innerHTML = `<h2>Acepciones de la palabra "${input}"</h2>`;

        aceptions.forEach((aception, index) => {
            const synonims = aception.synonims;

            if (synonims.length > 0) {
                // Crear un elemento para cada acepción
                const aceptionElement = document.createElement('div');
                aceptionElement.classList.add('aception');
                aceptionElement.innerHTML = `
                    <h3>Acepción ${index + 1}</h3>
                    <p>Sinónimos: ${createSynonymsHTML(synonims)}</p>
                `;
                infoContainer.appendChild(aceptionElement);
            }
        });

        // Inicializar la red con vis-network
        let network = new vis.Network(container, network_data, options);
    } catch (error) {
        console.error('Error al fetchData:', error);
    }
}

// Función para crear el HTML de los sinónimos con eventos clicables
function createSynonymsHTML(synonims) {
    return synonims.map(word => `
        <span 
            class="synonym" 
            onclick="handleSynonymClick('${escapeQuotes(word)}')"
        >
            ${word}
        </span>
    `).join(', ');
}

// Función para manejar el clic en un sinónimo
function handleSynonymClick(word) {
    const queryInput = document.getElementById('queryInput');
    queryInput.value = word;
    fetchData();
}

// Función adicional para manejar el clic en la palabra ejemplo "fuego"
function handleExampleClick(word) {
    const queryInput = document.getElementById('queryInput');
    queryInput.value = word;
    fetchData();
}

// Función para escapar comillas simples en las palabras
function escapeQuotes(word) {
    return word.replace(/'/g, "\\'");
}
