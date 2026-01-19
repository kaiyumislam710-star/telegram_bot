import ta

def calculate_indicators(df):
    """
    Input: df with 'close' prices
    Output: df with indicators + call_percent, put_percent
    """

    # ================= Indicators =================
    df['ema9'] = ta.trend.ema_indicator(df['close'], 9)
    df['ema21'] = ta.trend.ema_indicator(df['close'], 21)
    df['rsi'] = ta.momentum.rsi(df['close'], 14)

    # ================= Scores =================
    call_score = 0
    put_score = 0

    # 1️⃣ EMA Trend
    if df['ema9'].iloc[-1] > df['ema21'].iloc[-1]:
        call_score += 40
    elif df['ema9'].iloc[-1] < df['ema21'].iloc[-1]:
        put_score += 40

    # 2️⃣ RSI
    if df['rsi'].iloc[-1] > 55:
        call_score += 30
    elif df['rsi'].iloc[-1] < 45:
        put_score += 30

    # 3️⃣ Candle direction
    if df['close'].iloc[-1] > df['close'].iloc[-2]:
        call_score += 30
    elif df['close'].iloc[-1] < df['close'].iloc[-2]:
        put_score += 30

    # ================= Normalize =================
    total = call_score + put_score

    if total == 0:
        call_percent = 50
        put_percent = 50
    else:
        call_percent = int((call_score / total) * 100)
        put_percent = int((put_score / total) * 100)

    # ================= Clamp (NO 0 / 100) =================
    MIN_PCT = 20
    MAX_PCT = 80

    if call_percent < MIN_PCT:
        call_percent = MIN_PCT
        put_percent = 100 - MIN_PCT

    elif call_percent > MAX_PCT:
        call_percent = MAX_PCT
        put_percent = 100 - MAX_PCT

    if put_percent < MIN_PCT:
        put_percent = MIN_PCT
        call_percent = 100 - MIN_PCT

    elif put_percent > MAX_PCT:
        put_percent = MAX_PCT
        call_percent = 100 - MAX_PCT

    # ================= Attach to df =================
    df['call_score'] = call_score
    df['put_score'] = put_score
    df['call_percent'] = call_percent
    df['put_percent'] = put_percent

    return df