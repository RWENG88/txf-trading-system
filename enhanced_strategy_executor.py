import json
from typing import Dict
from adaptive_range_config import AdaptiveRangeConfig, enhanced_strategy_analysis
from advanced_prediction_engine import AdvancedPredictionEngine

class EnhancedStrategyExecutor:
    def __init__(self):
        self.adaptive_config = AdaptiveRangeConfig()
        self.prediction_engine = AdvancedPredictionEngine()
        
    def execute_comprehensive_analysis(self, market_data: Dict) -> str:
        """執行綜合分析：區間策略 + 預測邏輯"""
        
        # 1. 基礎區間策略分析
        zone_analysis = enhanced_strategy_analysis(market_data)
        
        # 2. 高級預測分析
        prediction_result = self.prediction_engine.generate_comprehensive_prediction(market_data)
        
        # 3. 生成綜合報告
        report = self._generate_comprehensive_report(market_data, prediction_result, zone_analysis)
        
        return report
    
    def _generate_comprehensive_report(self, market_data: Dict, prediction: Dict, zone_analysis: str) -> str:
        """生成綜合分析報告"""
        
        current_price = market_data["TXF1"]["close"]
        dji_close = market_data["DJI"]["close"]
        
        # 報告標題
        report_lines = [
            "=" * 80,
            "🎯 【台指期貨綜合策略分析報告】",
            "=" * 80,
            ""
        ]
        
        # 當前市場狀況
        report_lines.extend([
            "📊 【當前市場狀況】",
            f"台指期貨 TXF1：{current_price:,} 點",
            f"道瓊指數 DJI：{dji_close:,} 點",
            f"分析時間：{market_data.get('date', 'N/A')}",
            ""
        ])
        
        # 道瓊轉換分析
        dji_pred = prediction["dji_based_prediction"]
        report_lines.extend([
            "🇺🇸 【道瓊指數轉換台指期貨精準點位】",
            f"基礎轉換點位：{dji_pred['base_prediction']:,} 點",
            f"MACD調整：{dji_pred['macd_adjustment']:+} 點",
            f"RSI調整：{dji_pred['rsi_adjustment']:+} 點",
            f"道瓊預測結果：{dji_pred['final_prediction']:,} 點",
            f"預測信心度：{dji_pred['confidence']:.1%}",
            ""
        ])
        
        # 美國期貨風氣分析
        us_sentiment = prediction["us_futures_sentiment"]
        report_lines.extend([
            "🏛️ 【美國期貨買賣風氣分析】",
            f"綜合風氣評分：{us_sentiment['sentiment_score']}/10",
            f"風氣描述：{us_sentiment['description']}",
            f"綜合RSI：{us_sentiment['combined_rsi']:.2f}",
            f"總動能(MACD)：{us_sentiment['total_momentum']:+.2f}",
            f"對台指影響：{us_sentiment['txf_impact']:+} 點",
            ""
        ])
        
        # 台指期貨風氣分析
        txf_sentiment = prediction["txf_sentiment"]
        report_lines.extend([
            "🇹🇼 【台指期貨買賣風氣分析】",
            f"綜合風氣評分：{txf_sentiment['sentiment_score']}/10",
            f"風氣描述：{txf_sentiment['description']}",
            f"成交量：{txf_sentiment['volume']:,} 口",
            f"量能情緒：{txf_sentiment['volume_sentiment']:.2f}/10",
            f"RSI情緒：{txf_sentiment['rsi_sentiment']:.2f}/10", 
            f"MACD情緒：{txf_sentiment['macd_sentiment']:.2f}/10",
            f"風氣點位影響：{txf_sentiment['txf_impact']:+} 點",
            ""
        ])
        
        # 綜合預測結果
        recommendation = prediction["recommendation"]
        report_lines.extend([
            "🎯 【綜合預測結果】",
            f"最終預測點位：{prediction['final_prediction']:,} 點",
            f"預測區間：{prediction['prediction_range']['lower']:,} - {prediction['prediction_range']['upper']:,} 點",
            f"與當前價差：{prediction['price_difference']:+} 點",
            "",
            "📈 【交易建議】",
            f"建議方向：{recommendation['direction']}",
            f"信心等級：{recommendation['confidence']}",
            f"進場策略：{recommendation['entry_strategy']}",
            f"預期移動：{recommendation['expected_move']}",
            f"風險等級：{recommendation['risk_level']}",
            ""
        ])
        
        # 區間策略分析
        report_lines.extend([
            "🎪 【區間策略分析】",
            zone_analysis.replace("🎯 【台指期貨策略分析】\n", ""),
            ""
        ])
        
        # 風險提醒
        report_lines.extend([
            "⚠️ 【風險提醒】",
            self._generate_risk_warnings(market_data, prediction),
            ""
        ])
        
        # 總結建議
        report_lines.extend([
            "💡 【策略總結】",
            self._generate_strategy_summary(prediction, recommendation),
            "=" * 80
        ])
        
        return "\n".join(report_lines)
    
    def _generate_risk_warnings(self, market_data: Dict, prediction: Dict) -> str:
        """生成風險警告"""
        warnings = []
        
        txf_rsi = market_data["TXF1"]["rsi"]
        us_sentiment = prediction["us_futures_sentiment"]["sentiment_score"]
        txf_sentiment = prediction["txf_sentiment"]["sentiment_score"]
        price_diff = abs(prediction["price_difference"])
        
        # RSI風險
        if txf_rsi > 80:
            warnings.append("🔴 台指RSI極度超買(>80)，注意回調風險")
        elif txf_rsi < 20:
            warnings.append("🔴 台指RSI極度超賣(<20)，注意反彈風險")
            
        # 情緒極端風險
        if us_sentiment > 8:
            warnings.append("🟡 美國市場情緒過度樂觀，提防獲利了結")
        elif us_sentiment < 2:
            warnings.append("🟡 美國市場情緒過度悲觀，可能超跌反彈")
            
        if txf_sentiment > 8:
            warnings.append("🟡 台指情緒過度狂熱，散戶追高風險高")
        elif txf_sentiment < 2:
            warnings.append("🟡 台指情緒過度恐慌，可能形成底部")
            
        # 價格跳空風險
        if price_diff > 200:
            warnings.append("🔴 預測價差過大(>200點)，注意跳空風險")
        
        if not warnings:
            warnings.append("🟢 當前風險等級相對溫和，但仍需謹慎操作")
            
        return "\n".join([f"• {warning}" for warning in warnings])
    
    def _generate_strategy_summary(self, prediction: Dict, recommendation: Dict) -> str:
        """生成策略總結"""
        direction = recommendation["direction"]
        confidence = recommendation["confidence"]
        price_diff = prediction["price_difference"]
        
        if direction in ["做多", "偏多"]:
            if price_diff > 100:
                return "強烈建議做多，但分批進場控制風險，設定合理停損停利"
            else:
                return "溫和看多，可適度配置多單，密切關注技術指標變化"
        elif direction in ["做空", "偏空"]:
            if price_diff < -100:
                return "強烈建議做空，但分批進場控制風險，設定合理停損停利"
            else:
                return "溫和看空，可適度配置空單，密切關注支撐位表現"
        else:
            return "建議觀望為主，等待更明確的方向信號再進場操作"

def run_enhanced_strategy(data_path: str = "data/sample_input.json") -> str:
    """執行增強版策略分析"""
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            market_data = json.load(f)
        
        executor = EnhancedStrategyExecutor()
        result = executor.execute_comprehensive_analysis(market_data)
        return result
        
    except Exception as e:
        return f"❌ 策略執行錯誤：{str(e)}"

if __name__ == "__main__":
    result = run_enhanced_strategy()
    print(result) 