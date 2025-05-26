import pandas as pd
from typing import Optional

def compare_aum(csv_today: str, csv_yesterday: str) -> Optional[str]:
    """
    Compare Asia Tech AUM percentage between today and yesterday.
    
    Args:
        csv_today (str): Path to today's portfolio CSV.
        csv_yesterday (str): Path to yesterday's portfolio CSV.
        
    Returns:
        Optional[str]: Formatted string with AUM % comparison or None if error.
    """
    try:
        df_today = pd.read_csv(csv_today)
        df_yesterday = pd.read_csv(csv_yesterday)

        today_asia_tech = df_today[(df_today['Region'] == 'Asia') & (df_today['Sector'] == 'Tech')]['AUM'].sum()
        yesterday_asia_tech = df_yesterday[(df_yesterday['Region'] == 'Asia') & (df_yesterday['Sector'] == 'Tech')]['AUM'].sum()

        total_today = df_today['AUM'].sum()
        total_yesterday = df_yesterday['AUM'].sum()

        if total_today == 0 or total_yesterday == 0:
            return None

        pct_today = (today_asia_tech / total_today) * 100
        pct_yesterday = (yesterday_asia_tech / total_yesterday) * 100

        return f"{pct_today:.2f}% of AUM, up from {pct_yesterday:.2f}%"

    except Exception as e:
        print(f"Error comparing AUM: {e}")
        return None
