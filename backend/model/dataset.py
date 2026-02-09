
import pandas as pd
import torch
from torch_geometric.data import Data, InMemoryDataset
from rdkit import Chem
from rdkit.Chem import rdmolops
import numpy as np

# Allowed Atom Types (Organic Chemistry subset)
ATOM_TYPES = ['C', 'N', 'O', 'S', 'F', 'Cl', 'Br', 'P', 'I']

def one_hot_encoding(x, permitted_list):
    """
    Maps input x to a one-hot vector based on the permitted list.
    If x is not in the list, maps to the last element (Unknown).
    """
    if x not in permitted_list:
        x = permitted_list[-1]
        
    binary_encoding = [int(x == possible) for possible in permitted_list]
    return binary_encoding

class OncologyDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(OncologyDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0], weights_only=False)

    @property
    def raw_file_names(self):
        return ['oncology_drugs.csv']

    @property
    def processed_file_names(self):
        return ['oncology_processed.pt']

    def download(self):
        # We assume data is already in data/raw from Phase 1
        pass

    def process(self):
        print("🧪 ALCHEMY: Converting SMILES to Graph Tensors...")
        
        # Load CSV
        df = pd.read_csv(self.raw_paths[0])
        
        data_list = []
        
        for index, row in df.iterrows():
            smiles = row['smiles']
            mol = Chem.MolFromSmiles(smiles)
            
            if mol is None:
                continue
                
            # 1. Node Features (Atom Types)
            # Size: [Num_Atoms, Num_Atom_Types]
            node_features = []
            for atom in mol.GetAtoms():
                node_features.append(
                    one_hot_encoding(atom.GetSymbol(), ATOM_TYPES)
                )
            
            x = torch.tensor(node_features, dtype=torch.float)
            
            # 2. Edge Index (Connectivity) & Edge Attributes (Bond Types)
            # Size: [2, Num_Edges] and [Num_Edges, Num_Bond_Types]
            edge_indices = []
            edge_attrs = []
            
            for bond in mol.GetBonds():
                i = bond.GetBeginAtomIdx()
                j = bond.GetEndAtomIdx()
                
                # Undirected graph: Add (i, j) and (j, i)
                edge_indices.append([i, j])
                edge_indices.append([j, i])
                
                # Bond Type One-Hot: Single, Double, Triple, Aromatic
                bond_type = bond.GetBondTypeAsDouble()
                is_aromatic = 1.0 if bond.GetBondType() == Chem.rdchem.BondType.AROMATIC else 0.0
                
                # Simple Feature: [BondOrder, IsAromatic]
                attr = [bond_type, is_aromatic] 
                edge_attrs.append(attr)
                edge_attrs.append(attr)
                
            edge_index = torch.tensor(edge_indices, dtype=torch.long).t().contiguous()
            edge_attr = torch.tensor(edge_attrs, dtype=torch.float)
            
            # Create Data Object
            data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, smiles=smiles)
            data_list.append(data)
            
        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        # Save
        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])
        print(f"✅ Saved processed dataset with {len(data_list)} graphs.")

if __name__ == "__main__":
    # Test Run
    dataset = OncologyDataset(root='backend/data')
    print(f"Loaded Dataset: {dataset}")
    print(f"Sample Graph: {dataset[0]}")
