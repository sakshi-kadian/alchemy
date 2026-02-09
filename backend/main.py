
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Ensure backend modules are visible
sys.path.append(os.getcwd())

from backend.model.generate import AlchemyGenerator

app = FastAPI(title="Alchemy API", version="1.0.0")

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Generator Instance
generator = None

@app.on_event("startup")
def load_engine():
    global generator
    print("🚀 ALCHEMY API: Booting up...")
    try:
        generator = AlchemyGenerator(
            model_path="backend/checkpoints/diffusion_model.pth",
            graph_path="backend/data/processed/knowledge_graph.gpickle"
        )
    except Exception as e:
        print(f"❌ Failed to load engine: {e}")

@app.get("/")
def health_check():
    return {"status": "online", "system": "Alchemy Neuro-Symbolic Engine"}

class GenerateRequest(BaseModel):
    prompt: str

def extract_graph_neighborhood(smiles):
    """
    Extract knowledge graph neighborhood for a generated molecule.
    Returns nodes and links in D3.js format.
    """
    # For demo, return a sample graph (Mocking the Neuro-Symbolic reasoning)
    # In production, query the actual NetworkX graph based on similarity
    
    return {
        "nodes": [
            {"id": "MOL_GEN", "type": "molecule", "label": "Generated Candidate"},
            {"id": "MECH_Kinase", "type": "mechanism", "label": "Target: Kinase"},
            {"id": "TOX_Cardio", "type": "toxicity", "label": "Risk: Cardiotoxicity"},
            {"id": "TOX_Hepato", "type": "toxicity", "label": "Risk: Hepatotoxicity"},
            {"id": "DRUG_Imatinib", "type": "molecule", "label": "Ref: Imatinib"},
            {"id": "SUBSTR_Amide", "type": "molecule", "label": "Substruct: Amide"},
        ],
        "links": [
            {"source": "MOL_GEN", "target": "MECH_Kinase"},
            {"source": "MECH_Kinase", "target": "DRUG_Imatinib"},
            {"source": "MECH_Kinase", "target": "TOX_Cardio"},
            {"source": "MECH_Kinase", "target": "TOX_Hepato"},
            {"source": "MOL_GEN", "target": "SUBSTR_Amide"},
        ]
    }

@app.post("/generate")
def generate_drug(req: GenerateRequest):
    if not generator:
        raise HTTPException(status_code=503, detail="Engine not ready")
    
    print(f"🔬 Request received: {req.prompt}")
    candidate = generator.generate_candidate(req.prompt)
    
    # NEW: Extract graph neighborhood
    graph_data = extract_graph_neighborhood(candidate['smiles'])
    
    return {
        "candidate": candidate,
        "graph_data": graph_data,
        "status": "success"
    }

@app.get("/molecule/{chembl_id}")
def get_molecule_data(chembl_id: str):
    # Retrieve Graph Data for Visualization (Explainability)
    # For MVP, we can return data from our Knowledge Graph directly
    # or just return the standard JSON we built.
    return {"id": chembl_id, "data": "Graph Neighborhood Data"}
