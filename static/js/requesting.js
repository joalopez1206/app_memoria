async function fetchData() {
    const input = document.getElementById('queryInput').value;
    const response = await fetch(`/query?input=${encodeURIComponent(input)}`);
    const data = await response.json();
    
    const container = document.getElementById('mynetwork');
    // provide the data in the vis format
    let network_data = {
        nodes: data.nodes,
        edges: data.edges
    };
    var options = {
    // Enable this to make the endpoints smaller/larger
    edges: {
        arrows: {
            to: {
                scaleFactor: 1
            }
        }
    }
    };

    // initialize your network!
    var network = new vis.Network(container, network_data, options)
}