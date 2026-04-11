import os
import re
import pandas as pd

# Configuration 
BASE_PATH = # path
OUTPUT_FILE = 'Dementia_AllDiagnoses_FCE_Report.xlsx'
TARGET_CODES = ['F00', 'F01', 'F02', 'F03', 'F05', 'G30', 'G31', 'G32']

def get_year_label(filename):
    m = re.search(r'diag(\d{4})(\d{2})', filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None

# Discover files 
all_files = sorted([
    f for f in os.listdir(BASE_PATH)
    if 'diag' in f.lower()
    and f.endswith('.xlsx')
    and all(k not in f.lower() for k in ['4cha', 'sum', 'prim'])
])

# Extract Data 
records = []

for fname in all_files:
    year_label = get_year_label(fname)
    if not year_label: continue

    try:
        xl = pd.ExcelFile(os.path.join(BASE_PATH, fname))
        sheet = next((s for s in xl.sheet_names if 'All' in s and '3' in s), None)
        if not sheet: continue

        # Locate the header row
        df_raw = pd.read_excel(xl, sheet_name=sheet, header=None, nrows=30)
        hdr_row = next((i for i, row in df_raw.iterrows() 
                        if 'Main diagnosis' in ' '.join(str(x) for x in row.values)), None)
        if hdr_row is None: continue

        # Identify column positions
        hdr_vals = [str(x).lower() for x in df_raw.iloc[hdr_row].values]
        code_idx = next((j for j, v in enumerate(hdr_vals) if 'all diagnoses: 3 character' in v), None)
        all_diag_idx = next((j for j, v in enumerate(hdr_vals) if v.strip() in ('all diagnoses', 'all  diagnoses')), None)

        if code_idx is None or all_diag_idx is None: continue

        # Process data rows
        df_data = pd.read_excel(xl, sheet_name=sheet, header=None, skiprows=hdr_row + 1)
        df_data['_code'] = df_data.iloc[:, code_idx].astype(str).str.strip().str[:3].str.upper()
        
        hits = df_data[df_data['_code'].isin(TARGET_CODES)].copy()

        for _, row in hits.iterrows():
            raw_val = str(row.iloc[all_diag_idx]).replace(',', '').replace('*', '0').strip()
            raw_val = re.sub(r'\(.*?\)', '', raw_val).strip()
            try:
                value = int(float(raw_val))
            except:
                value = 0
                
            records.append({'Year': year_label, 'Code': row['_code'], 'AllDiag_FCE': value})

    except Exception as e:
        print(f"Error processing {fname}: {e}")

# Build Table 
df_all = pd.DataFrame(records)
pivot = (df_all
         .pivot_table(index='Year', columns='Code', values='AllDiag_FCE', aggfunc='sum')
         .reindex(columns=TARGET_CODES)
         .fillna(0)
         .astype(int))

# Add Totals and formatting
pivot['Total'] = pivot.sum(axis=1)
pivot = pivot.reset_index()

# Add Average row
avg_row = pivot.drop('Year', axis=1).mean().round().astype(int).to_dict()
avg_row['Year'] = 'Average'
pivot = pd.concat([pivot, pd.DataFrame([avg_row])], ignore_index=True)

# Save Raw Excel 
output_path = os.path.join('/mnt/user-data/outputs', OUTPUT_FILE)
pivot.to_excel(output_path, index=False)

print(f"Table created successfully at: {output_path}")