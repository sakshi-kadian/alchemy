
import sys
import os
sys.path.append(os.getcwd())

from rdkit import Chem
from backend.model.generate import AlchemyGenerator
from tqdm import tqdm
import torch

def measure_validity(num_samples=100):
    print("🧪 ALCHEMY: Measuring Structural Validity...")
    
    # Load generator
    # Ensure model exists first (might fail if training not done)
    # If training is running, we might be loading an old or partial checkpoint?
    # Actually, we should wait for training to finish.
    # But we can write the script now.
    
    if not os.path.exists("backend/checkpoints/diffusion_model.pth"):
        print("❌ Model checkpoint not found. Wait for training to complete.")
        return

    try:
        gen = AlchemyGenerator(
            model_path="backend/checkpoints/diffusion_model.pth",
            graph_path="data/processed/knowledge_graph.gpickle"
        )
    except Exception as e:
        print(f"❌ Failed to load generator: {e}")
        return
    
    valid_count = 0
    total = num_samples
    
    print(f"   Generating {total} candidates...")
    
    for i in tqdm(range(total), desc="Sampling"):
        try:
            result = gen.generate_candidate()
            smiles = result['smiles']
            
            # Check if valid
            mol = Chem.MolFromSmiles(smiles)
            if mol is not None:
                valid_count += 1
        except Exception as e:
            # print(f"Error on sample {i}: {e}")
            pass
    
    validity_score = (valid_count / total) * 100
    
    print(f"\n✅ Validity Score: {validity_score:.2f}%")
    print(f"   Valid: {valid_count}/{total}")
    
    if validity_score >= 85:
        print("🎉 PASSED: Exceeds 85% threshold!")
    else:
        print("⚠️  WARNING: Below 85% threshold. Score reflects currently trained model capability.")
    
    # Save results
    with open("VALIDATION_RESULTS.md", "w", encoding='utf-8') as f:
        f.write(f"# ALCHEMY - Validation Results\n\n")
        f.write(f"**Structural Validity Test**\n")
        f.write(f"- **Samples:** {total}\n")
        f.write(f"- **Valid:** {valid_count}\n")
        f.write(f"- **Score:** {validity_score:.2f}%\n")
        f.write(f"- **Outcome:** {'✅ PASSED' if validity_score >= 85 else '⚠️ LOW'}\n")

    return validity_score

if __name__ == "__main__":
    measure_validity(100)
