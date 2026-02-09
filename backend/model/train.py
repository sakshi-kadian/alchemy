
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from dataset import OncologyDataset
from diffusion import DiffusionModel
import os

def train():
    print("🚀 ALCHEMY: Initializing Generative Training Pipeline...")
    
    # 1. Load Data
    full_dataset = OncologyDataset(root='backend/data')
    loader = DataLoader(full_dataset, batch_size=4, shuffle=True)
    
    # 2. Initialize Model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"   Using Compute Device: {device}")
    
    model = DiffusionModel(hidden_dim=64).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    
    # 3. Training Loop
    epochs = 5  # Reduced for fast verification (Resume MVP) # Should be 1000+ for real results, but 100 for demo
    model.train()
    
    print(f"👉 Starting Training for {epochs} Epochs...")
    
    for epoch in range(1, epochs+1):
        total_loss = 0
        
        for batch in loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            
            # --- Diffusion Process (Add Noise) ---
            # Sample time t uniformly [0, 1]
            t = torch.rand(batch.num_graphs, device=device)
            
            # Create Noisy Input (x_t)
            # In real diffusion, we mix signal with gaussian noise based on t.
            # Simplified here: x_noisy = x + noise * t
            noise_x = torch.randn_like(batch.x) * t[batch.batch].unsqueeze(1)
            noisy_x = batch.x + noise_x
            
            noise_edge = torch.randn_like(batch.edge_attr) * t[batch.batch[batch.edge_index[0]]].unsqueeze(1)
            noisy_edge_attr = batch.edge_attr + noise_edge
            
            # --- Model Prediction (Denoise) ---
            # NEW: Sample random protein target (0-9)
            # In a real scenario, this would come from batch.y (target class)
            protein_id = torch.randint(0, 10, (batch.num_graphs,), device=device)
            
            # Forward Pass (Predict Clean Graph from Noisy)
            # model predicts: atom_types, edge_types
            # Pass protein_id for conditioning
            pred_x, pred_edge = model(noisy_x, batch.edge_index, noisy_edge_attr, t, batch.batch, protein_id)
            
            # --- Loss Calculation ---
            # We want the model to predict the ORIGINAL (clean) x and edge_attr
            # Regression Loss (MSE)
            loss_x = F.mse_loss(pred_x, batch.x)
            loss_edge = F.mse_loss(pred_edge, batch.edge_attr)
            
            loss = loss_x + loss_edge
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        if epoch % 10 == 0:
            print(f"   Epoch {epoch:03d} | Loss: {total_loss:.4f} | AtomLoss: {loss_x:.4f}")

    # 4. Save Model
    os.makedirs('backend/checkpoints', exist_ok=True)
    torch.save(model.state_dict(), 'backend/checkpoints/diffusion_model.pth')
    print("✅ Training Complete. Model saved to backend/checkpoints/diffusion_model.pth")

if __name__ == "__main__":
    train()
