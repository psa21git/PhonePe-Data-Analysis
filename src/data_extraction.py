import os
import json
import pandas as pd
import sqlite3

def extract_aggregated_transaction(base_dir):
    path = os.path.join(base_dir, "aggregated", "transaction", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data'] and 'transactionData' in data['data'] and data['data']['transactionData']:
                        for item in data['data']['transactionData']:
                            name = item.get('name')
                            for pi in item.get('paymentInstruments', []):
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'Transaction_type': name,
                                    'Transaction_count': pi.get('count', 0),
                                    'Transaction_amount': pi.get('amount', 0.0)
                                })
    return pd.DataFrame(data_list)

def extract_aggregated_user(base_dir):
    path = os.path.join(base_dir, "aggregated", "user", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data'] and 'usersByDevice' in data['data'] and data['data']['usersByDevice']:
                        for item in data['data']['usersByDevice']:
                            data_list.append({
                                'State': state,
                                'Year': int(year),
                                'Quarter': int(quarter),
                                'Brand': item.get('brand'),
                                'Count': item.get('count', 0),
                                'Percentage': item.get('percentage', 0.0)
                            })
    return pd.DataFrame(data_list)

def extract_aggregated_insurance(base_dir):
    path = os.path.join(base_dir, "aggregated", "insurance", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data'] and 'transactionData' in data['data'] and data['data']['transactionData']:
                        for item in data['data']['transactionData']:
                            name = item.get('name')
                            for pi in item.get('paymentInstruments', []):
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'Transaction_type': name,
                                    'Transaction_count': pi.get('count', 0),
                                    'Transaction_amount': pi.get('amount', 0.0)
                                })
    return pd.DataFrame(data_list)

def extract_map_transaction(base_dir):
    path = os.path.join(base_dir, "map", "transaction", "hover", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data'] and 'hoverDataList' in data['data'] and data['data']['hoverDataList']:
                        for item in data['data']['hoverDataList']:
                            district = item.get('name')
                            for mt in item.get('metric', []):
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'District': district,
                                    'Transaction_count': mt.get('count', 0),
                                    'Transaction_amount': mt.get('amount', 0.0)
                                })
    return pd.DataFrame(data_list)

def extract_map_user(base_dir):
    path = os.path.join(base_dir, "map", "user", "hover", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data'] and 'hoverData' in data['data'] and data['data']['hoverData']:
                        for dist, vals in data['data']['hoverData'].items():
                            data_list.append({
                                'State': state,
                                'Year': int(year),
                                'Quarter': int(quarter),
                                'District': dist,
                                'RegisteredUsers': vals.get('registeredUsers', 0),
                                'AppOpens': vals.get('appOpens', 0)
                            })
    return pd.DataFrame(data_list)

def extract_map_insurance(base_dir):
    path = os.path.join(base_dir, "map", "insurance", "hover", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data'] and 'hoverDataList' in data['data'] and data['data']['hoverDataList']:
                        for item in data['data']['hoverDataList']:
                            district = item.get('name')
                            for mt in item.get('metric', []):
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'District': district,
                                    'Transaction_count': mt.get('count', 0),
                                    'Transaction_amount': mt.get('amount', 0.0)
                                })
    return pd.DataFrame(data_list)

def extract_top_transaction(base_dir):
    path = os.path.join(base_dir, "top", "transaction", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data']:
                        # Only take pincodes for simplicity and granularity
                        if 'pincodes' in data['data'] and data['data']['pincodes']:
                            for item in data['data']['pincodes']:
                                entity_name = item.get('entityName')
                                metric = item.get('metric', {})
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'Pincode': entity_name,
                                    'Transaction_count': metric.get('count', 0),
                                    'Transaction_amount': metric.get('amount', 0.0)
                                })
    return pd.DataFrame(data_list)

def extract_top_user(base_dir):
    path = os.path.join(base_dir, "top", "user", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data']:
                        if 'pincodes' in data['data'] and data['data']['pincodes']:
                            for item in data['data']['pincodes']:
                                entity_name = item.get('name')
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'Pincode': entity_name,
                                    'RegisteredUsers': item.get('registeredUsers', 0)
                                })
    return pd.DataFrame(data_list)

def extract_top_insurance(base_dir):
    path = os.path.join(base_dir, "top", "insurance", "country", "india", "state")
    if not os.path.exists(path):
        return pd.DataFrame()
    data_list = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path): continue
            for file in os.listdir(year_path):
                if not file.endswith('.json'): continue
                quarter = file.split('.')[0]
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        data = json.load(f)
                    except:
                        continue
                    if 'data' in data and data['data']:
                        if 'pincodes' in data['data'] and data['data']['pincodes']:
                            for item in data['data']['pincodes']:
                                entity_name = item.get('entityName')
                                metric = item.get('metric', {})
                                data_list.append({
                                    'State': state,
                                    'Year': int(year),
                                    'Quarter': int(quarter),
                                    'Pincode': entity_name,
                                    'Transaction_count': metric.get('count', 0),
                                    'Transaction_amount': metric.get('amount', 0.0)
                                })
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    # Resolve paths relative to project root (one level up from src/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pulse_data_dir = os.path.join(project_root, "pulse-master", "data")
    print(f"Project root: {project_root}")
    print("Extracting data into dataframes...")
    
    df_agg_trans = extract_aggregated_transaction(pulse_data_dir)
    df_agg_user = extract_aggregated_user(pulse_data_dir)
    df_agg_ins = extract_aggregated_insurance(pulse_data_dir)
    
    df_map_trans = extract_map_transaction(pulse_data_dir)
    df_map_user = extract_map_user(pulse_data_dir)
    df_map_ins = extract_map_insurance(pulse_data_dir)
    
    df_top_trans = extract_top_transaction(pulse_data_dir)
    df_top_user = extract_top_user(pulse_data_dir)
    df_top_ins = extract_top_insurance(pulse_data_dir)
    
    print(f"Dataframes created! Sample shapes: Agg_Trans: {df_agg_trans.shape}, Map_User: {df_map_user.shape}")
    
    # Save to SQLite database in project root
    db_path = os.path.join(project_root, "phonepe_pulse.db")
    print(f"Saving dataframes to SQLite database: {db_path}...")
    
    conn = sqlite3.connect(db_path)
    if not df_agg_trans.empty: df_agg_trans.to_sql("Aggregated_transaction", conn, if_exists='replace', index=False)
    if not df_agg_user.empty: df_agg_user.to_sql("Aggregated_user", conn, if_exists='replace', index=False)
    if not df_agg_ins.empty: df_agg_ins.to_sql("Aggregated_insurance", conn, if_exists='replace', index=False)
    
    if not df_map_trans.empty: df_map_trans.to_sql("Map_transaction", conn, if_exists='replace', index=False)
    if not df_map_user.empty: df_map_user.to_sql("Map_user", conn, if_exists='replace', index=False)
    if not df_map_ins.empty: df_map_ins.to_sql("Map_insurance", conn, if_exists='replace', index=False)
    
    if not df_top_trans.empty: df_top_trans.to_sql("Top_transaction", conn, if_exists='replace', index=False)
    if not df_top_user.empty: df_top_user.to_sql("Top_user", conn, if_exists='replace', index=False)
    if not df_top_ins.empty: df_top_ins.to_sql("Top_insurance", conn, if_exists='replace', index=False)
    
    conn.close()
    print("ETL complete! Database populated.")
