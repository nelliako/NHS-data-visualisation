import os, re
import pandas as pd

# Config 

CSV_DIR  = './csv_files'   # 1998-99 to 2011-12 summary CSVs
XLSX_DIR = './xlsx_files'  # 2012-13 to 2023-24 diagnosis xlsx files
OUT_PATH = './Chapter5_FCE_LongFormat.csv'

GROUPS = [
    ('F00-F09', 0,  9, 'Organic, including symptomatic, mental disorders'),
    ('F10-F19', 10, 19,  'Mental and behavioural disorders due to psychoactive substance use'),
    ('F20-F29', 20,29, 'Schizophrenia, schizotypal and delusional disorders'),
    ('F30-F39', 30, 39,  'Mood [affective] disorders'),
    ('F40-F69', 40, 69, 'Neurotic, stress-related, somatoform, behavioural syndromes and personality disorders'),
    ('F70-F79',70, 79, 'Mental retardation'),
    ('F80-F99', 80,99,  'Other mental and behavioural disorders'),
]

# Helpers 

def clean_num(val):
    s = re.sub(r'\(.*?\)', '', str(val)).replace(',', '').replace('-', '').strip()
    try:
        return int(float(s)) if s else 0
    except:
        return 0

def get_year(fname):
    m = re.search(r'(\d{4})-(\d{2})-prim', fname)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.search(r'(\d{2})-(\d{2})', fname)
    if m:
        y1, y2 = m.group(1), m.group(2)
        return f"{'19' if int(y1) >= 98 else '20'}{y1}-{y2}"
    m = re.search(r'diag(\d{4})(\d{2})', fname)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None

# Extract from CSVs (1998-99 to 2011-12) 

# Two source rows (F00-F03 + F04-F09) add up to our F00-F09 group
PREFIX_MAP = {
    'F00-F03': 'F00-F09', 'F04-F09': 'F00-F09',
    'F10-F19': 'F10-F19', 'F20-F29': 'F20-F29',
    'F30-F39': 'F30-F39', 'F40-F69': 'F40-F69',
    'F70-F79': 'F70-F79', 'F80-F99': 'F80-F99',
}

records = []

for fname in sorted(os.listdir(CSV_DIR)):
    if not fname.endswith('.csv'):
        continue
    year = get_year(fname)
    if not year:
        continue

    df  = pd.read_csv(os.path.join(CSV_DIR, fname), header=None, on_bad_lines='skip')
    hdr = next(i for i, row in df.iterrows()
               if 'finished consultant' in ' '.join(str(x) for x in row.values).lower())
    fce_col = next(j for j, v in enumerate(df.iloc[hdr].astype(str).str.lower())
                   if 'finished consultant' in v)

    totals = {g[0]: 0 for g in GROUPS}
    for i in range(hdr + 1, len(df)):
        desc = str(df.iloc[i, 0]).strip().upper()
        for prefix, group in PREFIX_MAP.items():
            if desc.startswith(prefix):
                totals[group] += clean_num(df.iloc[i, fce_col])
                break

    for key, _, _, desc in GROUPS:
        records.append({'Year': year, 'Chapter': key, 'Description': desc,
                        'FCE': totals[key], 'Source': 'CSV primary diagnosis summary'})
  

# Extract from XLSXs (2012-13 to 2023-24) 

xlsx_files = sorted([f for f in os.listdir(XLSX_DIR)
                     if f.endswith('.xlsx') and 'diag' in f.lower()
                     and not any(x in f.lower() for x in ['4cha', 'sum', 'prim', 'dementia'])])

for fname in xlsx_files:
    year = get_year(fname)
    if not year:
        continue

    xl    = pd.ExcelFile(os.path.join(XLSX_DIR, fname))
    sheet = next(s for s in xl.sheet_names if 'All' in s and '3' in s)
    raw   = pd.read_excel(os.path.join(XLSX_DIR, fname), sheet_name=sheet, header=None, nrows=30)

    hdr      = next(i for i, row in raw.iterrows()
                    if 'Main diagnosis' in ' '.join(str(x) for x in row.values))
    hdr_vals = raw.iloc[hdr].astype(str).tolist()
    code_col = next(j for j, v in enumerate(hdr_vals) if 'all diagnoses: 3 character' in v.lower())
    main_col = next(j for j, v in enumerate(hdr_vals) if v.strip().lower() == 'main diagnosis')

    data = pd.read_excel(os.path.join(XLSX_DIR, fname), sheet_name=sheet, header=None, skiprows=hdr + 1)
    data['_code'] = data.iloc[:, code_col].astype(str).str.strip().str[:3].str.upper()
    data['_num']  = pd.to_numeric(data['_code'].str[1:], errors='coerce')
    data['_fce']  = data.iloc[:, main_col].apply(clean_num)
    fdata = data[data['_code'].str.match(r'^F\d{2}$')]

    for key, lo, hi, desc in GROUPS:
        total = int(fdata[(fdata['_num'] >= lo) & (fdata['_num'] <= hi)]['_fce'].sum())
        records.append({'Year': year, 'Chapter': key, 'Description': desc,
                        'FCE': total, 'Source': 'XLSX all diagnoses 3-char (main diagnosis)'})


# Sort and save 

df_out = pd.DataFrame(records)
df_out['_y'] = df_out['Year'].apply(lambda y: int(y[:4]))
df_out['_g'] = df_out['Chapter'].apply(lambda c: int(re.search(r'F(\d+)', c).group(1)))
df_out = df_out.sort_values(['_y', '_g']).drop(columns=['_y', '_g'])

df_out.to_csv(OUT_PATH, index=False)
