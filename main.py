from data_loader import load_market_json
from model_executor import run_strategy
from latest_news import get_latest_news

# 新增：增強版策略系統
try:
    from enhanced_strategy_executor import run_enhanced_strategy
    USE_ENHANCED = True
except ImportError:
    USE_ENHANCED = False
    print("警告：無法載入增強版策略模組，使用基礎策略")

# 新增：終極版策略系統（含10年歷史資料庫）
try:
    from ultimate_strategy_executor import run_ultimate_strategy
    USE_ULTIMATE = True
except ImportError:
    USE_ULTIMATE = False
    print("警告：無法載入終極版策略模組")

# 新增：實時數據獲取
try:
    from enhanced_data_loader import EnhancedDataLoader
    USE_REALTIME = True
except ImportError:
    USE_REALTIME = False
    print("警告：無法載入實時數據模組，使用本地數據")

# 新增：歷史資料庫初始化
try:
    from historical_database import initialize_historical_database
    USE_HISTORICAL_DB = True
except ImportError:
    USE_HISTORICAL_DB = False
    print("警告：無法載入歷史資料庫模組")

def main():
    print("🚀 台指期貨策略系統啟動中...")
    print("=" * 80)
    
    # 初始化歷史資料庫
    if USE_HISTORICAL_DB:
        print("🗄️ 初始化10年歷史資料庫...")
        try:
            db = initialize_historical_database()
            print("✅ 歷史資料庫準備就緒")
        except Exception as e:
            print(f"⚠️ 歷史資料庫初始化失敗: {e}")
        print("-" * 60)
    
    if USE_ULTIMATE:
        print("🏆 使用終極版策略系統：")
        print("✅ 基於10年歷史數據的智能分析")
        print("✅ 動態相關性權重調整")
        print("✅ 道瓊指數轉換台指期貨精準點位")
        print("✅ 美國期貨買賣風氣分析")
        print("✅ 台指期貨買賣風氣分析")
        print("✅ 歷史模式匹配驗證")
        print("✅ 歷史回測驗證分析")
        print("✅ 自適應區間策略")
        print("✅ 多維度風險控制")
        print("✅ 季節性效應調整")
        print("=" * 80)
        
        # 執行終極版策略
        result = run_ultimate_strategy()
        print(result)
        
    elif USE_ENHANCED:
        print("📊 使用增強版策略系統：")
        print("✅ 道瓊指數轉換台指期貨精準點位")
        print("✅ 美國期貨買賣風氣分析")
        print("✅ 台指期貨買賣風氣分析")
        print("✅ 自適應區間策略")
        print("✅ 綜合風險評估")
        print("=" * 80)
        
        # 執行增強版策略
        result = run_enhanced_strategy()
        print(result)
        
    else:
        print("📁 使用基礎策略系統...")
        
        if USE_REALTIME:
            # 使用實時數據
            print("🔄 獲取實時數據中...")
            data_loader = EnhancedDataLoader()
            data_loader.start_realtime_feed()
            
            # 等待數據載入
            import time
            time.sleep(3)
            
            market_data = data_loader.get_latest_txf_data()
        else:
            # 使用本地數據
            json_path = "data/sample_input.json"
            market_data = load_market_json(json_path)

        # 執行基礎策略分析
        result = run_strategy(market_data)
        print("📊 基礎策略分析結果：")
        print(result)
        
        # 獲取最新消息
        try:
            news = get_latest_news()
            print("\n📰 相關新聞：")
            print(news)
        except:
            print("\n⚠️ 無法獲取最新新聞")

    print("\n" + "=" * 80)
    print("📋 系統版本與功能對比：")
    print()
    
    if USE_ULTIMATE:
        print("🏆 【當前版本：終極版】")
        print("📊 資料來源：10年歷史資料庫 (2015-2025)")
        print("🧠 分析深度：多層次歷史驗證")
        print("🎯 預測精度：歷史回測優化")
        print("⚡ 反應速度：實時動態調整")
        print("🛡️ 風險控制：歷史統計風險評估")
    elif USE_ENHANCED:
        print("📊 【當前版本：增強版】")  
        print("📊 資料來源：實時市場數據")
        print("🧠 分析深度：多維度情緒分析")
        print("🎯 預測精度：技術指標優化")
        print("⚡ 反應速度：即時分析")
        print("🛡️ 風險控制：動態風險警告")
    else:
        print("📁 【當前版本：基礎版】")
        print("📊 資料來源：本地樣本數據")
        print("🧠 分析深度：基礎技術分析")
        print("🎯 預測精度：傳統指標")
        print("⚡ 反應速度：靜態分析")
        print("🛡️ 風險控制：基本風險提醒")
    
    print()
    print("🔧 核心功能模組：")
    print("1. 🎯 道瓊轉換：基於美股走勢預測台指期貨點位")
    print("2. 🇺🇸 美國風氣：綜合道瓊、納指、半導體指數情緒")
    print("3. 🇹🇼 台指風氣：基於成交量、RSI、MACD的情緒評估")
    print("4. 🎪 區間策略：5層價格區間的分層交易策略")
    print("5. ⚠️ 風險控制：RSI超買超賣警告、動態停利調整")
    print("6. 📈 交易建議：綜合多維度分析的精準操作建議")
    
    if USE_HISTORICAL_DB:
        print("7. 🗄️ 歷史資料庫：10年市場數據智能分析")
        print("8. 📊 相關性分析：動態權重調整系統")
        print("9. 🔍 模式匹配：歷史情況相似度驗證")
        print("10. 📈 回測驗證：歷史成功率統計分析")

if __name__ == "__main__":
    main()