import json
from adaptive_range_config import enhanced_strategy_analysis

def test_enhanced_strategy():
    # 載入實際數據
    with open('data/sample_input.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 50)
    print("🚀 增強版台指期貨策略分析")
    print("=" * 50)
    
    # 執行增強版策略分析
    result = enhanced_strategy_analysis(data)
    print(result)
    
    print("\n" + "=" * 50)
    print("📋 策略特點說明:")
    print("✅ 自動調整價格區間範圍")
    print("✅ 整合RSI技術指標")
    print("✅ 動態風險警告機制")
    print("✅ 適應市場價格變化")

if __name__ == "__main__":
    test_enhanced_strategy() 