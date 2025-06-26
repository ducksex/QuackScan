import json
import csv

def export_results(subs, out):
    if out.endswith('.json'):
        with open(out, 'w') as f:
            json.dump(subs, f, indent=2)
    elif out.endswith('.csv'):
        keys = subs[0].keys() if subs else []
        with open(out, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(subs)
    else:
        raise ValueError('Unsupported format: .json or .csv only')
