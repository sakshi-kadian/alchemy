# ALCHEMY
### **Toxicity-Aware Graph Diffusion for Oncology Therapeutics**
*Knowledge-Guided Clinical Drug Discovery*

---

## Overview

**Alchemy** is a state-of-the-art Generative AI platform designed to accelerate the discovery of novel oncology therapeutics. By bridging the gap between deep learning and symbolic reasoning, Alchemy employs a Neuro-Symbolic architecture that combines the creativity of Graph Diffusion Models with the safety constraints of a Clinical Knowledge Graph.

The system generates molecular structures conditioned on protein binding affinity while simultaneously grounding generation in biomedical reality via BioBERT embeddings and toxicity networks, ensuring candidates are structurally valid and safety-aligned.

---

## System Architecture & Workflow

1. **Latent Diffusion**: Random noise is denoised into molecular graphs using a Graph Diffusion Transformer.
2. **Affinity Conditioning**: Generation is steered toward high binding affinity for specific oncology targets.
3. **Knowledge Filtering**: A Clinical Knowledge Graph (NetworkX) acts as a symbolic supervisor, identifying and pruning molecular candidates with hepatotoxic or cardiotoxic substructures.
4. **Explanation**: Reasoning paths are visualized via an interactive 3D dashboard.

---

## Technical Contributions

- **Generative Graph Diffusion**: Developed a custom Graph Diffusion Model using PyTorch Geometric to denoise random graphs into valid molecular structures, achieving 85%+ structural validity.
- **Knowledge-Guided Safety Pipeline**: Integrated BioBERT embeddings with a NetworkX Knowledge Graph to provide real-time toxicity guardrails, filtering high-risk molecular substructures.
- **Bio-Medical Data Engineering**: Constructed a pipeline processing oncology agents from ChEMBL, extracting toxicity warnings and adverse event annotations for knowledge-guided generation.
- **Chemist’s Workstation**: Built a full-stack platform with interactive 3D molecular visualization (React Three Fiber) and explainable AI logic visualizing toxicity reasoning paths.

---

## Tech Stack

- **Generative Model**: PyTorch Geometric (Graph Diffusion Transformer with GINEConv layers)
- **Knowledge Graph**: NetworkX (Toxicity and mechanism-of-action relationships)
- **Embeddings**: BioBERT (Semantic vectorization of clinical text)
- **Backend API**: FastAPI (High-performance async inference engine)
- **Frontend UI**: Next.js 15 + Tailwind (Monochrome workstation aesthetic)
- **Visualization**: React Three Fiber (Real-time 3D rendering of molecular data)
- **Cheminformatics**: RDKit (Cheminformatics validation and SMILES processing)

---

## Usage Guide
1. **Dashboard**: Open `http://localhost:3000/dashboard`.
2. **Prompts**: Type a target description or use the provided demo presets.
3. **Synthesis**: Click the **Initiate Sequence** button.
4. **Analysis**: Inspect the 3D model and Knowledge Graph logic side-by-side.

---

## Performance Metrics

- **Structural Validity**: >85% (measured via RDKit).
- **Training Data**: 1,400+ Oncology Compounds (ChEMBL subset).
- **Inference Time**: <200ms per molecule.

---

## Installation and Setup

#### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Inference Engine
uvicorn backend.main:app --reload
```
Backend runs on: `http://localhost:8000`

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Development Server
npm run dev
```
Frontend runs on: `http://localhost:3000`