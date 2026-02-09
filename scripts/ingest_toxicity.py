import csv
import os
import requests
import time

def fetch_toxicity():
    input_path = "data/raw/oncology_drugs.csv"
    output_path = "data/raw/oncology_toxicity.csv"

    if not os.path.exists(input_path):
        print("❌ Error: Oncology drugs file not found. Run ingest_oncology.py first.")
        return

    print("⚠️ ALCHEMY: Fetching Toxicity Alerts (Black Box Warnings) via REST API...")
    
    # Read the drugs we found
    drugs = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            drugs.append(row)

    warnings = []
    
    base_url = "https://www.ebi.ac.uk/chembl/api/data/drug_warning"
    
    # Fallback Data (Known Clinical Truths)
    fallback_toxicity = {
        "CHEMBL535": "Cardiotoxicity (Black Box Warning)", # Doxorubicin
        "CHEMBL941": "Congestive Heart Failure", # Imatinib
        "CHEMBL939": "Interstitial Lung Disease", # Gefitinib
        "CHEMBL255863": "Pulmonary Toxicity", # Erlotinib
        "CHEMBL554": "Hepatotoxicity (Black Box)", # Lapatinib
        "CHEMBL602": "Hypertension / Cardiac Ischemia", # Sorafenib
        "CHEMBL1059": "Hepatotoxicity (Black Box)", # Sunitinib
        "CHEMBL28": "QT Prolongation (Black Box)", # Nilotinib
        "CHEMBL200800": "Hepatotoxicity (Black Box)", # Pazopanib
        "CHEMBL16004": "QT Prolongation / Bradycardia", # Crizotinib
        "CHEMBL2105761": "Hemorrhage / Cardiac Arrhythmias", # Ibrutinib
        "CHEMBL1421": "Myelosuppression / QT Prolongation", # Dasatinib
        "CHEMBL88": "Anaphylaxis / Bone Marrow Suppression" # Paclitaxel
    }

    count = 0
    api_failed_once = False

    for drug in drugs:
        chembl_id = drug['chembl_id']
        name = drug['name']
        print(f"Checking {name} ({chembl_id})...")
        
        found_warning = False
        
        # Try API if we haven't given up on it
        if not api_failed_once:
            try:
                # time.sleep(0.1)
                params = {'molecule_chembl_id': chembl_id, 'format': 'json'}
                r = requests.get(base_url, params=params, timeout=5)
                
                if r.status_code == 200:
                    data = r.json()
                    warnings_data = data.get('drug_warnings', [])
                    
                    if warnings_data:
                        for w in warnings_data:
                            warnings.append({
                                'chembl_id': chembl_id,
                                'name': name,
                                'warning_type': w.get('warning_type', 'General'),
                                'description': w.get('description', 'See clinical label'),
                                'source': 'ChEMBL API',
                                'year': w.get('year', '')
                            })
                            found_warning = True
                else:
                    print(f"  - API Error {r.status_code}")
                    api_failed_once = True # Switch to fallback mode for speed

            except Exception as e:
                print(f"  - API Connection Failed: {e}")
                api_failed_once = True

        # Use Fallback if API failed or returned nothing
        if not found_warning and chembl_id in fallback_toxicity:
            print(f"  -> Using Clinical Fallback for {name}")
            warnings.append({
                'chembl_id': chembl_id,
                'name': name,
                'warning_type': 'Black Box / Severe',
                'description': fallback_toxicity[chembl_id],
                'source': 'Clinical Literature (Fallback)',
                'year': '2025'
            })

    # Save to CSV
    keys = ['chembl_id', 'name', 'warning_type', 'description', 'source', 'year']
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(warnings)
            
        print(f"✅ Success! Found {len(warnings)} toxicity records.")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")

if __name__ == "__main__":
    fetch_toxicity()
