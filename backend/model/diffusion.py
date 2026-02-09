
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GINEConv, global_add_pool

class GNNEncoder(nn.Module):
    """
    A strong Graph Neural Network based on GINE (Graph Isomorphism Network + Edge features).
    This is the component that 'understands' chemical structures.
    """
    def __init__(self, hidden_dim=64, num_layers=4):
        super().__init__()
        
        # Atom Embedding (9 types + 1 mask) -> Hidden
        self.atom_emb = nn.Linear(9, hidden_dim) 
        
        # Bond Embedding (4 types + 1 mask) -> Hidden
        self.bond_emb = nn.Linear(2, hidden_dim) 

        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            mlp = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim * 2),
                nn.ReLU(),
                nn.Linear(hidden_dim * 2, hidden_dim)
            )
            self.convs.append(GINEConv(mlp, train_eps=True))
            
        self.norm = nn.LayerNorm(hidden_dim)

    def forward(self, x, edge_index, edge_attr):
        # x: [NumNodes, 9] (One-hot atom types)
        # edge_attr: [NumEdges, 2] (Bond features)
        
        x = self.atom_emb(x)
        edge_attr = self.bond_emb(edge_attr)
        
        for conv in self.convs:
            # GINEConv expects edge attributes
            x = conv(x, edge_index, edge_attr=edge_attr)
            x = x + F.relu(x) # Residual connection
            
        return self.norm(x)

class DiffusionModel(nn.Module):
    """
    The Generative Engine.
    It takes a Noisy Graph (t) and predicts the Clean Graph (t-1).
    """
    def __init__(self, hidden_dim=64, num_proteins=10):
        super().__init__()
        
        self.encoder = GNNEncoder(hidden_dim)
        
        # Time Embedding (Sinusoidal)
        self.time_mlp = nn.Sequential(
            nn.Linear(1, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # Protein Target Embedding
        self.protein_emb = nn.Embedding(num_proteins, hidden_dim)
        
        # Prediction Heads
        # 1. Predict Atom Types (9 classes)
        self.atom_pred = nn.Linear(hidden_dim, 9)
        
        # 2. Predict Bond Existence/Type (Simple version: predict bond features)
        self.bond_pred = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2) # [BondType, Aromaticity]
        )

    def forward(self, x, edge_index, edge_attr, t, batch, protein_id):
        """
        x: Noisy Atom Features
        edge_attr: Noisy Edge Features
        t: Time step [0, 1]
        protein_id: ID of target protein [Batch]
        """
        # 1. Encode Graph Structure
        h = self.encoder(x, edge_index, edge_attr) # [NumNodes, Hidden]
        
        # 2. Inject Time Info
        t_emb = self.time_mlp(t.view(-1, 1)) # [Batch, Hidden]
        
        # 3. Inject Protein Info
        p_emb = self.protein_emb(protein_id) # [Batch, Hidden]
        
        # Add conditioning to nodes
        h = h + t_emb[batch] + p_emb[batch]
        
        # 4. Predict Clean Atoms
        pred_x = self.atom_pred(h)
        
        # 5. Predict Clean Edges
        # Concatenate source and target node embeddings for each edge
        row, col = edge_index
        edge_h = torch.cat([h[row], h[col]], dim=1)
        pred_edge = self.bond_pred(edge_h)
        
        return pred_x, pred_edge

if __name__ == "__main__":
    print("Testing Diffusion Model Architecture...")
    model = DiffusionModel()
    print(model)
    print("✅ Model compiled successfully.")
