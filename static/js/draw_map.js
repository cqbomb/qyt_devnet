function draw(url) {
    $.getJSON(url,function(data) {
        var network = null;

        var container = document.getElementById('mynetwork');
        var data = {
            nodes: data.nodes,
            edges: data.edges
        };
        var options = {
                // edges: {
                //     smooth: {
                //         type: 'cubicBezier',
                //         forceDirection: 'vertical',
                //         roundness: 0.4
                //     }
                // },
                // layout: {
                //     hierarchical: {
                //         direction: 'Up-Down'
                //     }
                // },
                physics:false
        };
        network = new vis.Network(container, data, options);
    });
}
