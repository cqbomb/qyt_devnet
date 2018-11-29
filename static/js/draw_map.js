function draw(url) {
    $.getJSON(url,function(data) {
        var network = null;

        var container = document.getElementById('mynetwork');
        var data = {
            nodes: data.nodes,
            edges: data.edges
        };
        var options = {};
        network = new vis.Network(container, data, options);
    });
}
