
import pickle
import networkx as nx
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from tqdm import tqdm

def embed_knowledge_graph():
    print("🧬 ALCHEMY: Initializing BioBERT for Semantic Embedding...")
    
    # 1. Load BioBERT (Pre-trained on PubMed)
    model_name = "dmis-lab/biobert-v1.1" 
    # Use a smaller/lighter model if BioBERT is too heavy, but BioBERT is the "Elite" choice.
    # If this fails on your PC due to RAM, we can switch to "distilbert".
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
    except Exception as e:
        print(f"⚠️ BioBERT download failed: {e}")
        print("🔄 Switching to DistilBERT (Lighter fallback)...")
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        model = AutoModel.from_pretrained("distilbert-base-uncased")

    print("✅ Model Loaded. Encoding Clinical Knowledge...")

    # 2. Load the NetworkX Graph
    graph_path = "data/processed/knowledge_graph.gpickle"
    with open(graph_path, "rb") as f:
        G = pickle.load(f)
        
    # 3. Embed Node Texts
    # We only care about embedding the "Meaning" of Mechanism and Toxicity nodes.
    # Molecule nodes will use GNN structure, but SideEffects need NLP.
    
    count = 0
    with torch.no_grad():
        for node in tqdm(G.nodes(data=True)):
            node_id, attrs = node
            node_type = attrs.get('type')
            
            text_to_embed = ""
            
            if node_type == "Toxicity":
                text_to_embed = f"{attrs.get('name', '')} {attrs.get('severity', '')}"
            elif node_type == "Mechanism":
                text_to_embed = attrs.get('name', '')
            
            if text_to_embed:
                # Tokenize & BERT
                inputs = tokenizer(text_to_embed, return_tensors="pt", padding=True, truncation=True, max_length=64)
                outputs = model(**inputs)
                
                # Take the [CLS] token embedding (first token) as the "Sentence Vector"
                embedding = outputs.last_hidden_state[:, 0, :].numpy().flatten()
                
                # Save into Graph
                G.nodes[node_id]['embedding'] = embedding
                count += 1

    print(f"  + Generated {count} Semantic Embeddings.")

    # 4. Save Updated Graph
    with open(graph_path, "wb") as f:
        pickle.dump(G, f)
        
    print(f"✅ Success! Knowledge Graph is now Semantically Enriched.")
    print("   (BioBERT vectors attached to Mechanism/Toxicity nodes)")

if __name__ == "__main__":
    embed_knowledge_graph()
