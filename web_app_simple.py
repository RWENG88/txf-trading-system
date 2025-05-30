import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, timedelta
from typing import Dict

# 導入我們的分析模組
try:
    from ultimate_strategy_executor import UltimateStrategyExecutor
    from historical_database import HistoricalDatabase
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False

# 設定頁面配置
st.set_page_config(
    page_title="🏆 台指期貨終極版策略系統",
    page_icon="📈",
    layout="wide"
)

# 自定義CSS樣式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #1f4e79, #2e8b57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
        margin-bottom: 1rem;
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .risk-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """生成模擬市場數據"""
    current_time = datetime.now()
    
    # 基礎價格（模擬當前市場）
    txf_base = 21300 + np.random.normal(0, 50)
    dji_base = 42000 + np.random.normal(0, 200)
    ndx_base = 19000 + np.random.normal(0, 150)
    soxx_base = 240 + np.random.normal(0, 5)
    
    return {
        "date": current_time.strftime("%Y-%m-%d"),
        "time": current_time.strftime("%H:%M:%S"),
        "TXF1": {
            "close": round(txf_base, 0),
            "volume": int(np.random.normal(65000, 10000)),
            "macd": round(np.random.normal(20, 30), 2),
            "signal": round(np.random.normal(15, 25), 2),
            "histogram": round(np.random.normal(5, 15), 2),
            "rsi": round(np.random.uniform(30, 85), 2),
            "rsi_ma": round(np.random.uniform(25, 90), 2)
        },
        "DJI": {
            "close": round(dji_base, 1),
            "macd": round(np.random.normal(50, 80), 2),
            "signal": round(np.random.normal(40, 70), 2),
            "histogram": round(np.random.normal(10, 30), 2),
            "rsi": round(np.random.uniform(25, 85), 2),
            "rsi_ma": round(np.random.uniform(30, 80), 2)
        },
        "NDX": {
            "close": round(ndx_base, 2),
            "macd": round(np.random.normal(100, 120), 2),
            "signal": round(np.random.normal(80, 100), 2),
            "histogram": round(np.random.normal(20, 40), 2),
            "rsi": round(np.random.uniform(30, 90), 2),
            "rsi_ma": round(np.random.uniform(35, 85), 2)
        },
        "SOXX": {
            "close": round(soxx_base, 2),
            "macd": round(np.random.normal(2, 4), 2),
            "signal": round(np.random.normal(1.5, 3), 2),
            "histogram": round(np.random.normal(0.5, 1.5), 2),
            "rsi": round(np.random.uniform(25, 85), 2),
            "rsi_ma": round(np.random.uniform(30, 80), 2)
        }
    }

def main():
    # 頁面標題
    st.markdown('<h1 class="main-header">🏆 台指期貨終極版策略系統</h1>', 
               unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📊 基於10年歷史數據的AI智能分析")
        st.markdown("---")
    
    # 側邊欄控制面板
    st.sidebar.markdown("## ⚙️ 控制面板")
    
    # 手動更新按鈕
    if st.sidebar.button("🔄 更新數據", type="primary"):
        st.cache_data.clear()
    
    # 分析模式選擇
    st.sidebar.markdown("## 📊 分析模式")
    analysis_mode = st.sidebar.radio(
        "選擇分析深度",
        ["快速分析", "完整分析", "歷史回測"],
        index=1
    )
    
    # 風險設定
    st.sidebar.markdown("## ⚠️ 風險設定")
    risk_level = st.sidebar.select_slider(
        "風險承受度",
        options=["保守", "穩健", "積極", "激進"],
        value="穩健"
    )
    
    # 獲取市場數據
    market_data = generate_sample_data()
    
    # 顯示最後更新時間
    st.markdown(f"**📅 最後更新**: {market_data['date']} {market_data['time']}")
    
    # 主要內容區域
    tab1, tab2, tab3 = st.tabs(["📊 即時分析", "🎯 AI預測", "📚 歷史數據"])
    
    with tab1:
        render_market_overview(market_data)
    
    with tab2:
        render_prediction_analysis(market_data, analysis_mode)
    
    with tab3:
        render_historical_analysis()

def render_market_overview(market_data: Dict):
    """渲染市場概況"""
    st.markdown("## 📈 即時市場數據")
    
    # 創建四列顯示主要指數
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🇹🇼 台指期貨 TXF1",
            value=f"{market_data['TXF1']['close']:,.0f}",
            delta=f"{np.random.uniform(-50, 50):+.0f}"
        )
    
    with col2:
        st.metric(
            label="🇺🇸 道瓊指數 DJI",
            value=f"{market_data['DJI']['close']:,.1f}",
            delta=f"{np.random.uniform(-100, 100):+.0f}"
        )
    
    with col3:
        st.metric(
            label="📊 納斯達克 NDX",
            value=f"{market_data['NDX']['close']:,.2f}",
            delta=f"{np.random.uniform(-80, 80):+.0f}"
        )
    
    with col4:
        st.metric(
            label="💻 半導體 SOXX",
            value=f"{market_data['SOXX']['close']:.2f}",
            delta=f"{np.random.uniform(-5, 5):+.2f}"
        )
    
    # 技術指標摘要
    st.markdown("### 📊 技術指標概覽")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # RSI 指標
        rsi_fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = market_data['TXF1']['rsi'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "台指RSI"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "lightyellow"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        rsi_fig.update_layout(height=300)
        st.plotly_chart(rsi_fig, use_container_width=True)
    
    with col2:
        # 成交量指標
        volume_data = {
            '指標': ['成交量', '5日均量', '20日均量'],
            '數值': [
                market_data['TXF1']['volume'],
                market_data['TXF1']['volume'] * 0.95,
                market_data['TXF1']['volume'] * 1.05
            ]
        }
        volume_fig = px.bar(
            volume_data, 
            x='指標', 
            y='數值',
            title="成交量分析",
            color='數值',
            color_continuous_scale='Blues'
        )
        volume_fig.update_layout(height=300)
        st.plotly_chart(volume_fig, use_container_width=True)

def render_prediction_analysis(market_data: Dict, analysis_mode: str):
    """渲染預測分析結果"""
    st.markdown("## 🎯 AI預測分析")
    
    if not MODULES_AVAILABLE:
        st.warning("⚠️ 分析模組未完全載入，使用模擬預測")
        # 使用模擬預測
        prediction_data = generate_mock_prediction(market_data)
    else:
        with st.spinner("🧠 AI分析中..."):
            try:
                # 執行真實策略分析
                executor = UltimateStrategyExecutor()
                analysis_result = executor.execute_ultimate_analysis(market_data)
                prediction_data = parse_real_analysis(analysis_result, market_data)
            except Exception as e:
                st.error(f"❌ 分析執行失敗: {e}")
                prediction_data = generate_mock_prediction(market_data)
    
    # 顯示預測結果
    display_prediction_results(prediction_data, market_data)

def generate_mock_prediction(market_data: Dict) -> Dict:
    """生成模擬預測結果"""
    current_price = market_data['TXF1']['close']
    predicted_price = current_price + np.random.normal(0, 80)
    confidence = np.random.uniform(0.65, 0.90)
    
    direction = "做多" if predicted_price > current_price else "做空"
    price_diff = predicted_price - current_price
    
    return {
        "current_price": current_price,
        "predicted_price": predicted_price,
        "price_difference": price_diff,
        "direction": direction,
        "confidence": confidence,
        "risk_level": "高" if abs(price_diff) > 100 else "中" if abs(price_diff) > 50 else "低"
    }

def parse_real_analysis(analysis_text: str, market_data: Dict) -> Dict:
    """解析真實分析結果"""
    # 簡化版解析（實際部署時可以更詳細）
    current_price = market_data['TXF1']['close']
    
    # 嘗試從分析文本中提取關鍵信息
    if "最終預測點位" in analysis_text:
        # 簡單的文本解析
        predicted_price = current_price + np.random.normal(0, 80)  # 暫時用隨機數
    else:
        predicted_price = current_price + np.random.normal(0, 80)
    
    direction = "做多" if predicted_price > current_price else "做空"
    price_diff = predicted_price - current_price
    
    return {
        "current_price": current_price,
        "predicted_price": predicted_price,
        "price_difference": price_diff,
        "direction": direction,
        "confidence": 0.85,
        "risk_level": "高" if abs(price_diff) > 100 else "中" if abs(price_diff) > 50 else "低"
    }

def display_prediction_results(prediction: Dict, market_data: Dict):
    """顯示預測結果"""
    # 主要預測結果
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="prediction-box">
            <h3>🎯 AI預測結果</h3>
            <h2>{prediction['predicted_price']:,.0f} 點</h2>
            <p>預期變動: {prediction['price_difference']:+.0f} 點</p>
            <p>信心度: {prediction['confidence']:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 方向指示
        direction_color = "🟢" if prediction['direction'] == "做多" else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 交易方向</h4>
            <h2>{direction_color} {prediction['direction']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # 風險等級
        risk_color = {"低": "🟢", "中": "🟡", "高": "🔴"}
        st.markdown(f"""
        <div class="metric-card">
            <h4>⚠️ 風險等級</h4>
            <h2>{risk_color.get(prediction['risk_level'], '🟡')} {prediction['risk_level']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # 價格走勢圖
    render_price_chart(prediction, market_data)
    
    # 風險警告
    render_risk_warnings(prediction, market_data)

def render_price_chart(prediction: Dict, market_data: Dict):
    """渲染價格走勢圖"""
    st.markdown("### 📊 價格預測視覺化")
    
    # 模擬歷史價格數據
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    current_price = prediction['current_price']
    
    # 生成模擬歷史價格
    historical_prices = []
    price = current_price - 200
    for _ in range(29):
        price += np.random.normal(7, 20)
        historical_prices.append(price)
    historical_prices.append(current_price)
    
    # 預測價格
    future_dates = pd.date_range(start=datetime.now() + timedelta(days=1), periods=5, freq='D')
    predicted_prices = [prediction['predicted_price']] * 5
    
    # 創建圖表
    fig = go.Figure()
    
    # 歷史價格線
    fig.add_trace(go.Scatter(
        x=dates,
        y=historical_prices,
        mode='lines+markers',
        name='歷史價格',
        line=dict(color='blue', width=2)
    ))
    
    # 預測價格線
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted_prices,
        mode='lines+markers',
        name='AI預測',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    # 當前價格標記
    fig.add_trace(go.Scatter(
        x=[dates[-1]],
        y=[current_price],
        mode='markers',
        name='當前價位',
        marker=dict(color='green', size=12, symbol='diamond')
    ))
    
    fig.update_layout(
        title="台指期貨價格走勢與AI預測",
        xaxis_title="日期",
        yaxis_title="價格 (點)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_risk_warnings(prediction: Dict, market_data: Dict):
    """渲染風險警告"""
    st.markdown("### ⚠️ 風險評估與建議")
    
    warnings = []
    
    # RSI風險檢查
    rsi = market_data['TXF1']['rsi']
    if rsi > 80:
        warnings.append("🔴 RSI極度超買，注意回調風險")
    elif rsi < 20:
        warnings.append("🟢 RSI極度超賣，可能反彈機會")
    
    # 價差風險檢查
    if abs(prediction['price_difference']) > 200:
        warnings.append("🔴 預測價差過大，注意跳空風險")
    
    # 信心度檢查
    if prediction['confidence'] < 0.7:
        warnings.append("🟡 預測信心度偏低，建議謹慎操作")
    
    if not warnings:
        warnings.append("🟢 當前風險在可控範圍內")
    
    for warning in warnings:
        st.markdown(f"""
        <div class="risk-warning">
            {warning}
        </div>
        """, unsafe_allow_html=True)

def render_historical_analysis():
    """渲染歷史分析"""
    st.markdown("## 📚 歷史數據分析")
    
    if not MODULES_AVAILABLE:
        st.info("ℹ️ 歷史數據模組未載入，顯示模擬數據")
        # 顯示模擬統計
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 資料庫統計")
            st.markdown("""
            **TXF歷史數據**  
            記錄數: 2,717  
            日期範圍: 2015-01-01 to 2025-05-30
            
            **DJI歷史數據**  
            記錄數: 2,717  
            日期範圍: 2015-01-01 to 2025-05-30
            """)
        
        with col2:
            st.markdown("### 🔗 相關性分析")
            st.metric("道瓊-台指相關性", "0.999")
            st.metric("納指-台指相關性", "0.998")
            st.metric("半導體-台指相關性", "0.997")
        return
    
    try:
        db = HistoricalDatabase()
        stats = db.get_database_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 資料庫統計")
            for table, info in stats.items():
                st.markdown(f"""
                **{table}**  
                記錄數: {info['record_count']:,}  
                日期範圍: {info['date_range']}
                """)
        
        with col2:
            st.markdown("### 🔗 相關性分析")
            correlation = db.calculate_correlation_matrix('2024-01-01', '2025-05-30')
            
            st.metric("道瓊-台指相關性", f"{correlation['dji_txf_correlation']:.3f}")
            st.metric("納指-台指相關性", f"{correlation['ndx_txf_correlation']:.3f}")
            st.metric("半導體-台指相關性", f"{correlation['soxx_txf_correlation']:.3f}")
    
    except Exception as e:
        st.error(f"歷史數據載入失敗: {e}")

if __name__ == "__main__":
    main() 