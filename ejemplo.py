from neo4j import GraphDatabase, RoutingControl
import json
PORT = 7687
URI = f'bolt://localhost:{PORT}'

with open("credentials.json", "r") as f:
    data = json.load(f)
    USER = data['user']
    PASSWORD = data['password']
AUTH = (USER, PASSWORD)

COLORS = ["rgb(255,0,0)", "rgb(0,255,0)", "rgb(0,0,255)", "rgb(255,255,0)", "rgb(0,255,255)", "rgb(255,0,255)", "rgb(128,128,128)", "rgb(128,0,0)", "rgb(128,128,0)", "rgb(0,128,0)", "rgb(128,0,128)", "rgb(0,128,128)", "rgb(0,0,128)", "rgb(0,0,0)", "rgb(255,255,255)"]

with open("datos_12.json", "r") as f:
    DICT = {d['key']:d for d in json.load(f)}

with open("palabras_12.csv", "r") as f:
    lls = [l.split(",") for l in f.readlines()[1:]]
    WORD_DICT = {l[0].strip():int(l[1].strip()) for l in lls}

def get_distance_one(tx, word):
    QUERY = """match (a:Word)-[r:has_syn]->(b:Word) where a.palabra = $word return b"""

    nodes = tx.run(QUERY, word=word)
    QUERY = """match (a:Word)-[r:has_syn]->(b:Word)-[:has_syn]->(c:Word) where a.palabra = $word return b,c"""
    # QUERY = """
    # MATCH p=(a:Word)-[:has_syn]->(:Word)
    # WHERE a.palabra = $word
    # RETURN p"""
    result = tx.run(QUERY, word=word)
    #vecino, sumary, key = driver.execute_query(QUERY,{"word": word}, routing_=RoutingControl.READ, database_="neo4j")

    #records, _, _ = driver.execute_query(QUERY, routing_=RoutingControl.READ, database_="neo4j")
    return [n for n in nodes], [r for r in result] 

def to_json(word: str, wordid: int, records, nodos_a_agregar):
    retdict = dict()
    nodes = set()
    relationships = []

    
    nodes.add((wordid, word))
    nodes_dist_one = {(int(x['b']['id']), x['b']['palabra']) for x in nodos_a_agregar}
    nodes = nodes.union(nodes_dist_one)
    for x in nodes_dist_one:
        relationships.append({
                "from": wordid,
                "to": x[0],
                "arrows": {"to": {"enabled": True, "type": "arrow",}},
                "color": "rgb(0,0,0)",
        })

    for iden, word in nodes:
        records_of_b = [r for r in records 
                        if int(r['b']['id']) == iden and (int(r['c']['id']), r['c']['palabra']) in nodes]
        for record in records_of_b:
            relationships.append({
                "from": record['b']['id'],
                "to": record['c']['id'],
                "arrows": {
                    "to": {
                        "enabled": True,
                        "type": "arrow",
                    }
                },
                "color": "rgb(0,0,0)"
            })
    # colors = [(syn["synonims"],color) for syn,color in zip(DICT[word]["aseptions"], COLORS)]
    # l = []
    # for n in nodes: 
    #    for syns, color in colors:
    #         if n[1] in syns:
    #            l.append({"id": n[0], "label": n[1], "color": {"background": "white","border":color}} )
    #         #else:
    #         #   l.append({"id": n[0], "label": n[1], "color": {"border":"rgb(0,0,0)"}})
    
    # print(l)
    # retdict['nodes'] = l
    retdict['nodes'] = [{"id": n[0], "label": n[1], "color": "rgb(255,255,255)"} for n in nodes]
    retdict['edges'] = relationships
    return retdict
        

def distance_one(word: str) -> dict:
    with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        wordid = WORD_DICT.get(word, None)
        if not wordid:
            return {"status": 1}
        nodes, vecinos = session.read_transaction(get_distance_one, word)
        vecinos = to_json(word, wordid, vecinos, nodes)
        asp_data = DICT.get(word, None)
        if not asp_data:
            return {"status": 2}
        return {"neigh": vecinos, "asp": asp_data, "status":0}



def main(query: str):
    import pprint
    pprint.pprint(distance_one(query))
    #with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
    #    _,vecinos = session.read_transaction(get_distance_one, query)
    #    for vecino in vecinos:
    #        print(f"{vecino['b']['palabra']} -> {vecino['c']['palabra']}")
            # path = vecino['p']  # Aquí asumimos que 'p' es el Path
            # inicial_node = path.nodes[0]  # Accede al primer nodo del Path, que es el nodo inicial
            # final_node = path.nodes[-1]  # Accede al último nodo del Path, que es el nodo final
            # inicial_palabra = inicial_node['palabra']  # Accede a la propiedad 'palabra' del nodo inicial
            # final_palabra = final_node['palabra']  # Accede a la propiedad 'palabra' del nodo final
            # print(f"{inicial_palabra} -> {final_palabra}")

if __name__ == '__main__':
    while True:
        inp = input()
        main(inp)