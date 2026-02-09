
import csv
import json
import networkx as nx
import pickle

def build_knowledge_graph():
    print("🧠 ALCHEMY: Building Clinical Knowledge Graph (NetworkX)...")
    
    G = nx.DiGraph()
    
    # 1. Load Oncology Drugs -> Add Molecule Nodes
    drug_file = "data/raw/oncology_drugs.csv"
    toxicity_file = "data/raw/oncology_toxicity.csv"
    
    drugs = {} # ID -> Name map
    
    with open(drug_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row['chembl_id']
            name = row['name']
            mechanism = row['mechanism']
            
            drugs[cid] = name
            
            # Add Molecule Node
            G.add_node(cid, type="Molecule", name=name, smiles=row['smiles'])
            
            # Add Mechanism Node & Edge
            if mechanism:
                mech_id = f"MECH_{mechanism.replace(' ', '_')}"
                G.add_node(mech_id, type="Mechanism", name=mechanism)
                G.add_edge(cid, mech_id, relation="HAS_MECHANISM")

    print(f"  + Added {len(drugs)} Molecules and their Mechanisms.")

    # 2. Load Toxicity -> Add Toxicity Nodes & Risk Edges
    with open(toxicity_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row['chembl_id']
            tox_desc = row['description']
            tox_type = row['warning_type']
            
            if cid in drugs:
                # Add Toxicity Value Node (e.g., "Cardiotoxicity")
                # We simplify the text to make it a readable node
                short_tox = tox_desc.split(' ')[0] if len(tox_desc) > 20 else tox_desc
                tox_node_id = f"TOX_{tox_type}_{short_tox}".replace(" ", "_")
                
                if not G.has_node(tox_node_id):
                    G.add_node(tox_node_id, type="Toxicity", name=tox_desc, severity="High")
                
                # Link Molecule -> Toxicity
                G.add_edge(cid, tox_node_id, relation="HAS_RISK", source=row['source'])
                
    print(f"  + Integrated Toxicity Warnings.")
    
    # 3. Save the Graph
    stats = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "isolates": list(nx.isolates(G))
    }
    
    print(f"✅ Graph Built Successfully!")
    print(f"   Nodes: {stats['nodes']}")
    print(f"   Edges: {stats['edges']}")
    
    # Save as Pickle (for Python Backend/AI)
    with open("data/processed/knowledge_graph.gpickle", "wb") as f:
        pickle.dump(G, f)
        
    # Save as JSON (for Frontend Visualization)
    graph_data = nx.node_link_data(G)
    with open("data/processed/graph.json", "w") as f:
        json.dump(graph_data, f, indent=2)
        
    print("💾 Saved to data/processed/")

if __name__ == "__main__":
    build_knowledge_graph()
