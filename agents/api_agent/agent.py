import pandas as pd
from typing import Optional, Dict

def analyze_portfolio(csv_path: str) -> Optional[Dict[str, float]]:
    """
    Analyze portfolio CSV for total AUM and Asia Tech allocation percentage.
    
    Args:
        csv_path (str): Path to portfolio CSV file.
        
    Returns:
        Optional[Dict[str, float]]: Dictionary with total AUM and Asia Tech %,
        or None if error or invalid data.
    """
    try:
        df = pd.read_csv(csv_path)
        total_aum = df['AUM'].sum()
        if total_aum == 0:
            return None

        asia_tech = df[(df['Region'] == 'Asia') & (df['Sector'] == 'Tech')]
        asia_tech_aum = asia_tech['AUM'].sum()
        asia_tech_pct = (asia_tech_aum / total_aum) * 100

        return {
            "total_aum": total_aum,
            "asia_tech_pct": round(asia_tech_pct, 2)
        }
    except Exception as e:
        print(f"Error analyzing portfolio: {e}")
        return None
