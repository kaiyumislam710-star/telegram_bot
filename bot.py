def decision(df):
    call = df['call_percent'].iloc[-1]
    put = df['put_percent'].iloc[-1]

    THRESHOLD = 76  # strong signal

    if call >= THRESHOLD and call > put:
        return "CALL", int(call), int(put)
    elif put >= THRESHOLD and put > call:
        return "PUT", int(call), int(put)
    else:
        return "NONE", int(call), int(put)