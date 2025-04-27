import pandas as pd
import io

def process_job_file(file_storage):
    """
    Accepts a Flask FileStorage (text or CSV) and returns list of job dicts.
    """
    content = file_storage.read()
    try:
        # Try reading as CSV
        df = pd.read_csv(io.BytesIO(content))
    except Exception:
        # Fallback: parse text (assume newline-separated fields)
        text = content.decode('utf-8')
        lines = text.strip().splitlines()
        # Example parsing: assume '|' delimited
        data = [line.split('|') for line in lines if line]
        # Convert to list of dicts (header in first row)
        header = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=header)
    # Convert DataFrame rows to dicts
    jobs = df.to_dict(orient='records')
    return jobs
