from neo4j import GraphDatabase, RoutingControl
import pprint
PORT = 7687

URI = f'bolt://localhost:{PORT}'
USER = 'neo4j' 
PASSWORD = 'wena4321'
AUTH = (USER, PASSWORD)

def get_distance_one(tx, word):
    QUERY = """
    MATCH p=(a:Word)-[:has_syn]->(:Word)
    WHERE a.palabra = $word
    RETURN p"""
    result = tx.run(QUERY, word=word)
    #vecino, sumary, key = driver.execute_query(QUERY,{"word": word}, routing_=RoutingControl.READ, database_="neo4j")

    #records, _, _ = driver.execute_query(QUERY, routing_=RoutingControl.READ, database_="neo4j")
    return [r for r in result] 

def to_json(records):
    retdict = dict()
    nodes = set()
    relationships = []
    for record in records:
        path = record['p']
        inicio = path.nodes[0]
        final = path.nodes[-1]
        nodes.add((inicio['id'], inicio['palabra']))
        nodes.add((final['id'], final['palabra']))
        relationships.append({"from": inicio['id'], "to": final['id'], "arrows": {"to": {"enabled": True, "type": "arrow",}}})
    retdict['nodes'] = [{"id": n[0], "label": n[1]} for n in nodes]
    retdict['edges'] = relationships
    return retdict
        

def distance_one(word: str) -> dict:
    with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        vecinos = session.read_transaction(get_distance_one, word)
        return to_json(vecinos)



def main(query: str):
    with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        while True:
            vecinos = session.read_transaction(get_distance_one, wea)
            for vecino in vecinos:
                #print(vecino['p'])
                path = vecino['p']  # Aquí asumimos que 'p' es el Path
                inicial_node = path.nodes[0]  # Accede al primer nodo del Path, que es el nodo inicial
                final_node = path.nodes[-1]  # Accede al último nodo del Path, que es el nodo final
                inicial_palabra = inicial_node['palabra']  # Accede a la propiedad 'palabra' del nodo inicial
                final_palabra = final_node['palabra']  # Accede a la propiedad 'palabra' del nodo final
                #print(f"{inicial_palabra} -> {final_palabra}")

if __name__ == '__main__':
    wea = input()
    main(wea)