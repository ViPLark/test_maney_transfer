def parse_inns(value: str):
    inns = set()
    last_inn = []
    for symbol in value:
        if symbol.isdigit():
            last_inn.append(symbol)
        elif last_inn:
            inns.add(int(''.join(last_inn)))
            last_inn.clear()
    if last_inn:
        inns.add(int(''.join(last_inn)))
    return inns
