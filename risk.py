def calculate_amount(balance, risk_percent=1):
    return round(balance * risk_percent / 100, 2)