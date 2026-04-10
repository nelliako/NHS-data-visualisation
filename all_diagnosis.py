import os
import re
import pandas as pd

# Configuration 
BASE_PATH = # path
OUTPUT_FILE = # output
TARGET_CODES = ['F00', 'F01', 'F02', 'F03', 'F05', 'G30', 'G31', 'G32']

def get_year_label(filename):
    m = re.search(r'diag(\d{4})(\d{2})', filename)
    return f"{m.group(1)}-{m.group(2)}" if m else None

# 1. Discover files
all_files = sorted([f for f in os.listdir(BASE_PATH) if 'diag' in f.lower() and f.endswith('.xlsx') 
                    and not any(x in f.lower() for x in ['4cha', 'sum', 'prim'])])

records = []

# 2. Extract data
for fname in all_files:
    year_label = get_year_label(fname)
    if not year_label: continue

    try:
        full_path = os.path.join(BASE_PATH, fname)
        xl = pd.ExcelFile(full_path)
        sheet = next((s for s in xl.sheet_names if 'All' in s and '3' in s), None)
        
        if sheet:
            # Find the header row dynamically
            df_raw = pd.read_excel(full_path, sheet_name=sheet, nrows=30, header=None)
            hdr_row = next((i for i, row in df_raw.iterrows() if 'Main diagnosis' in ' '.join(str(x) for x in row.values)), None)
            
            if hdr_row is not None:
                df = pd.read_excel(full_path, sheet_name=sheet, skiprows=hdr_row)
                code_col = 'All diagnoses: 3 character code and description'
                main_col = 'Main diagnosis'

                # Clean and Filter
                df['_code'] = df[code_col].astype(str).str.strip().str[:3].str.upper()
                hits = df[df['_code'].isin(TARGET_CODES)].copy()

                for _, row in hits.iterrows():
                    # Clean numeric values (remove commas, handle asterisks)
                    raw_val = str(row[main_col]).replace(',', '').replace('*', '0').strip()
                    raw_val = re.sub(r'\(.*?\)', '', raw_val).strip()
                    
                    records.append({
                        'Year': year_label,
                        'Code': row['_code'],
                        'MainDiag_FCE': int(float(raw_val)) if raw_val else 0
                    })
        print(f"Processed: {year_label}")
    except Exception as e:
        print(f"Error {fname}: {e}")

# 3. Build pivot table
df_all = pd.DataFrame(records)
pivot = (df_all.pivot_table(index='Year', columns='Code', values='MainDiag_FCE', aggfunc='sum')
         .reindex(columns=TARGET_CODES).fillna(0).astype(int))

# 4. Save to excel
pivot.to_excel(OUTPUT_FILE)
print(f"\nSuccess! Table saved to: {OUTPUT_FILE}")