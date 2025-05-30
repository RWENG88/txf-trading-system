import math
from typing import Tuple, List

class AdaptiveRangeConfig:
    def __init__(self, base_range: Tuple[int, int] = (20000, 21000)):
        self.base_range = base_range
        self.zone_count = 5
        
    def calculate_dynamic_range(self, current_price: int, buffer_ratio: float = 0.1) -> Tuple[int, int]:
        """根據當前價格動態調整區間範圍"""
        low, high = self.base_range
        range_size = high - low
        
        # 如果價格超出範圍，動態調整
        if current_price < low:
            # 價格過低，向下擴展
            new_low = current_price - int(range_size * buffer_ratio)
            new_high = new_low + range_size
        elif current_price > high:
            # 價格過高，向上擴展  
            new_high = current_price + int(range_size * buffer_ratio)
            new_low = new_high - range_size
        else:
            # 價格在範圍內，保持原範圍
            new_low, new_high = low, high
            
        return (new_low, new_high)
    
    def get_adaptive_zones(self, current_price: int) -> List[Tuple[int, int]]:
        """獲取自適應區間"""
        dynamic_range = self.calculate_dynamic_range(current_price)
        low, high = dynamic_range
        interval = (high - low) // self.zone_count
        
        zones = []
        for i in range(self.zone_count):
            zone_low = low + i * interval
            zone_high = low + (i + 1) * interval
            if i == self.zone_count - 1:  # 最後一個區間包含上邊界
                zone_high = high
            zones.append((zone_low, zone_high))
            
        return zones[::-1]  # 反轉，讓高價區間在前
    
    def get_zone_index_adaptive(self, close: int, zones: List[Tuple[int, int]]) -> int:
        """獲取價格所在的區間索引"""
        for idx, (low, high) in enumerate(zones):
            if low <= close <= high:
                return idx + 1
        return -1
    
    def get_strategy_intensity(self, zone_idx: int, rsi: float = None) -> Tuple[str, int, str]:
        """根據區間和技術指標調整策略強度"""
        base_strategies = {
            1: ("偏多操作", 500),
            2: ("略偏多操作", 400),
            3: ("中性操作", 300),
            4: ("略偏空操作", 400),
            5: ("偏空操作", 500),
        }
        
        strategy_name, profit_target = base_strategies[zone_idx]
        risk_warning = ""
        
        # 根據RSI調整策略
        if rsi is not None:
            if rsi > 80:  # 超買
                if zone_idx <= 2:  # 在高價區且超買
                    risk_warning = "⚠️ RSI超買，建議減少多單力度"
                    profit_target = int(profit_target * 0.8)  # 減少停利目標
            elif rsi < 20:  # 超賣
                if zone_idx >= 4:  # 在低價區且超賣
                    risk_warning = "⚠️ RSI超賣，建議減少空單力度"
                    profit_target = int(profit_target * 0.8)
        
        return strategy_name, profit_target, risk_warning

# 使用範例
def enhanced_strategy_analysis(data: dict) -> str:
    """增強版策略分析"""
    close = data["TXF1"]["close"]
    rsi = data["TXF1"].get("rsi", None)
    
    # 初始化自適應配置
    adaptive_config = AdaptiveRangeConfig()
    
    # 獲取自適應區間
    zones = adaptive_config.get_adaptive_zones(close)
    zone_idx = adaptive_config.get_zone_index_adaptive(close, zones)
    
    if zone_idx == -1:
        return f"❌ 無法確定價格區間，當前價格：{close}"
    
    # 獲取策略建議
    strategy_name, profit_target, risk_warning = adaptive_config.get_strategy_intensity(
        zone_idx, rsi
    )
    
    current_zone = zones[zone_idx - 1]
    dynamic_range = adaptive_config.calculate_dynamic_range(close)
    
    output = [
        f"🎯 【台指期貨策略分析】",
        f"📊 收盤價：{close:,} 點",
        f"📏 動態區間：{dynamic_range[0]:,} - {dynamic_range[1]:,}",
        f"🎪 所屬區間：第{zone_idx}區 ({current_zone[0]:,} - {current_zone[1]:,})",
        f"📈 建議方向：{strategy_name}",
        f"🎯 停利目標：{profit_target} 點"
    ]
    
    if rsi:
        output.append(f"📊 RSI指標：{rsi:.2f}")
    
    if risk_warning:
        output.append(f"{risk_warning}")
    
    return "\n".join(output) 