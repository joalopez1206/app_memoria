from neo4j import GraphDatabase, RoutingControl
import json
PORT = 7687

URI = f'bolt://localhost:{PORT}'
USER = 'neo4j' 
PASSWORD = 'wena4321'
AUTH = (USER, PASSWORD)

with open("datos_12.json", "r") as f:
    DICT = {d['key']:d for d in json.load(f)}

def get_distance_one(tx, word):
    QUERY = """match (a:Word)-[r:has_syn]->(b:Word)-[:has_syn]->(c:Word) where a.palabra = $word return a,b,c"""
    # QUERY = """
    # MATCH p=(a:Word)-[:has_syn]->(:Word)
    # WHERE a.palabra = $word
    # RETURN p"""
    result = tx.run(QUERY, word=word)
    #vecino, sumary, key = driver.execute_query(QUERY,{"word": word}, routing_=RoutingControl.READ, database_="neo4j")

    #records, _, _ = driver.execute_query(QUERY, routing_=RoutingControl.READ, database_="neo4j")
    return [r for r in result] 

def to_json(records):
    retdict = dict()
    nodes = set()
    relationships = []
    for record in records:
        #sinonimo = record['b']
        #nodes.add((sinonimo['id'], sinonimo['palabra']))
        inicio = record['a']
        inicio_id = inicio['id']
        inicio_palabra = inicio['palabra']
        nodes.add((inicio['id'], inicio['palabra']))
        final = record['b']
        final_id = final['id']
        final_palabra = final['palabra']
        if (final['id'], final['palabra']) not in nodes:
            relationships.append({"from": inicio['id'],
                "to": final['id'],
                "arrows": {"to": {"enabled": True, "type": "arrow",}},
                "color": "rgb(0,0,0)",
                })
            nodes.add((final['id'], final['palabra']))

    for record in records:
        cercano = record['c']
        checkear = (cercano['id'], cercano['palabra'])
        if checkear in nodes:
            inicio = record['b']
            final = record['c']
            relationships.append({"from": inicio['id'],
            "to": final['id'],
            "arrows": {"to": {"enabled": True, "type": "arrow",}},
            "color": "rgb(0,0,0)"
            })
    retdict['nodes'] = [{"id": n[0], "label": n[1], "color": "rgb(255,255,255)",} for n in nodes]
    retdict['edges'] = relationships
    return retdict
        

def distance_one(word: str) -> dict:
    with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        vecinos = session.read_transaction(get_distance_one, word)
        vecinos = to_json(vecinos)
        asp_data = DICT[word]
        return {"neigh": vecinos, "asp": asp_data}



def main(query: str):
    with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        vecinos = session.read_transaction(get_distance_one, query)
        for vecino in vecinos:
            print(f"{vecino['b']['palabra']} -> {vecino['c']['palabra']}")
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