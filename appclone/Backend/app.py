from flask import Flask, request, jsonify
import osmnx as ox

app = Flask(__name__)

@app.route('/route', methods=['POST'])
def get_route():
    data = request.json
    origin = (data['origin_lat'], data['origin_lon'])
    destination = (data['dest_lat'], data['dest_lon'])
    
    # Get the graph for Bengaluru
    G = ox.graph_from_place('Bengaluru, India', network_type='drive')
    
    # Get the nearest nodes
    orig_node = ox.distance.nearest_nodes(G, origin[1], origin[0])
    dest_node = ox.distance.nearest_nodes(G, destination[1], destination[0])
    
    # Calculate the shortest path
    route = ox.shortest_path(G, orig_node, dest_node)
    
    # Get the route coordinates
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    
    return jsonify(route_coords)

if __name__ == '__main__':
    app.run(debug=True)