def get_zone_ranges(close: int, base_range=(20000, 21000)) -> tuple:
    low, high = base_range
    interval = (high - low) // 5
    zones = [(low + i * interval + 1, low + (i + 1) * interval) for i in range(5)]
    return zones[::-1]

def get_zone_index(close: int, zones: list) -> int:
    for idx, (low, high) in enumerate(zones):
        if low <= close <= high:
            return idx + 1
    return -1