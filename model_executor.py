from range_config import get_zone_ranges, get_zone_index

zone_to_strategy = {
    1: ("**偏空操作**", 500),
    2: ("**略偏空操作**", 400),
    3: ("**中性操作（雙向）**", 300),
    4: ("**略偏多操作**", 400),
    5: ("**偏多操作**", 500),
}

def run_strategy(data: dict) -> str:
    close = data["TXF1"]["close"]
    base_range = (20000, 21000)
    zones = get_zone_ranges(close, base_range)
    zone_idx = get_zone_index(close, zones)

    if zone_idx == -1:
        return f"收盤價 {close} 超出區間範圍 {base_range}"

    strategy, profit_target = zone_to_strategy[zone_idx]

    output = (
        f"【收盤價】{close}\n"
        f"【所屬區間】第{zone_idx}區：{zones[zone_idx - 1][0]}–{zones[zone_idx - 1][1]}\n"
        f"【建議方向】{strategy}\n"
        f"【停利點數】{profit_target} 點"
    )
    return output