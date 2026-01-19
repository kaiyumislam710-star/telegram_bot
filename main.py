import time
from datetime import datetime

from data import get_candles
from indicator_module import calculate_indicators
from bot import decision
from telegram import send

# ================= SETTINGS =================
PAIR = "EURUSDT"
TIMEFRAME = "1m"

MAX_TRADE = 8
TRADE_COUNT = 0

UPCOMING_DELAY = 20 * 60     # 20 minutes
CHECK_INTERVAL = 60          # 1 minute

LOSS_COUNT = 0
MAX_LOSS = 2

CALL_PUT_MAX = 100           # CALL + PUT কখনো 100 এর বেশি হবে না
MIN_SIGNAL = 75              # minimum % for signal

# ================= TIME FILTER =================
def trading_time():
    hour = datetime.now().hour
    return 10 <= hour < 22   # সকাল ১০টা – রাত ১০টা

# ================= MAIN LOOP =================
while True:
    now = datetime.now()

    # ⏰ Trading hour check
    if not trading_time():
        print(f"[{now}] Outside trading hours")
        time.sleep(60)
        continue

    # ⛔ Max trade reached
    if TRADE_COUNT >= MAX_TRADE:
        send("⛔ আজকের ট্রেড শেষ (8/8)")
        break

    # ⛔ 2 loss rule
    if LOSS_COUNT >= MAX_LOSS:
        send("⛔ 2 loss হয়েছে — আজকের ট্রেড বন্ধ")
        break

    # ================= ANALYSIS =================
    df = get_candles()
    df = calculate_indicators(df)

    result, call, put = decision(df)

    # 🔧 Normalize (CALL + PUT = 100)
    total = call + put
    if total > 0:
        call = int(call * CALL_PUT_MAX / total)
        put = CALL_PUT_MAX - call

    # ================= UPCOMING =================
    if result in ["CALL", "PUT"] and max(call, put) >= MIN_SIGNAL:
        send(f"""
⏳ UPCOMING SIGNAL

PAIR: {PAIR}
TIMEFRAME: {TIMEFRAME}

Expected trade in 20 minutes
CALL: {call}%
PUT: {put}%
""")

        print("Upcoming sent → continuous analysis started")

        # ⏳ Upcoming সময়েও analysis চলবে
        start = time.time()
        while time.time() - start < UPCOMING_DELAY:
            df = get_candles()
            df = calculate_indicators(df)
            r, c, p = decision(df)

            total = c + p
            if total > 0:
                c = int(c * CALL_PUT_MAX / total)
                p = CALL_PUT_MAX - c

            print(datetime.now(), "Live check:", r, c, p)
            time.sleep(CHECK_INTERVAL)

        # ================= FINAL CONFIRM =================
        df = get_candles()
        df = calculate_indicators(df)
        final_result, call, put = decision(df)

        total = call + put
        if total > 0:
            call = int(call * CALL_PUT_MAX / total)
            put = CALL_PUT_MAX - call

        if final_result in ["CALL", "PUT"] and max(call, put) >= MIN_SIGNAL:
            send(f"""
✅ FINAL SIGNAL

PAIR: {PAIR}
TIMEFRAME: {TIMEFRAME}

DECISION: {final_result}
CALL: {call}%
PUT: {put}%
ENTRY: Next candle
""")
            TRADE_COUNT += 1
            LOSS_COUNT = 0   # এখানে real trade হলে result অনুযায়ী বাড়াবে
        else:
            send("⚠️ Market weak — trade skipped")

        time.sleep(1800)  # 30 min gap

    else:
        print(f"[{now}] No strong signal")
        time.sleep(60)