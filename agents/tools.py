import pandas as pd
import requests
import io
import json
from crewai.tools import tool

# Simple in-memory cache to stay within request scope or avoid redundant downloads
_DATASET_CACHE = {}

@tool("read_dataset_content")
def read_dataset_content(dataset_url: str):
    """
    Reads a dataset from a URL (CSV or Excel) and returns a comprehensive summary.
    This tool is cached; calling it multiple times for the same URL will return the cached result.
    """
    if dataset_url in _DATASET_CACHE:
        print(f"CACHE HIT: Returning cached summary for {dataset_url}")
        return _DATASET_CACHE[dataset_url]

    try:
        print(f"CACHE MISS: Fetching dataset from {dataset_url}")
        response = requests.get(dataset_url)
        response.raise_for_status()
        
        # Determine file type
        if dataset_url.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(response.content))
        else:
            # Assume CSV
            df = pd.read_csv(io.BytesIO(response.content))
        
        # Generate summary
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        
        # Truncate summary statistics to avoid massive JSON blobs
        stats = df.describe(include='all').to_dict()
        if len(stats.keys()) > 50: # If many columns, just show a subset
            subset_keys = list(stats.keys())[:50]
            stats = {k: stats[k] for k in subset_keys}
            stats["_msg"] = "Truncated: Only showing first 50 columns of statistics."

        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()[:100], # Limit column names
            "data_types": df.dtypes.apply(lambda x: str(x)).head(100).to_dict(),
            "missing_values": df.isnull().sum().head(100).to_dict(),
            "summary_statistics": stats,
            "head_rows": df.head(3).to_dict(orient='records') # Only 3 rows
        }
        
        result = f"Dataset Summary (Optimized):\n{json.dumps(summary, indent=2, default=str)}\n\nDetailed Info (Header):\n{info_str[:2000]}"
        
        # Save to cache
        _DATASET_CACHE[dataset_url] = result
        return result
        
    except Exception as e:
        return f"Error reading dataset: {str(e)}"
