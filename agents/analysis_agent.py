def analyze_risk_exposure(portfolio_data: dict):
    """
    Dummy analysis returning risk commentary based on allocation.
    """
    allocation_str = portfolio_data.get("asia_tech_allocation", "0%").replace("%", "")
    allocation = float(allocation_str)

    if allocation > 20:
        risk_comment = "neutral with cautionary tilt due to rising yields"
    else:
        risk_comment = "low risk with stable outlook"

    return {"risk_comment": risk_comment}
