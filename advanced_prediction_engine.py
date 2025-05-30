import math
from typing import Dict, Tuple, List
from datetime import datetime

class AdvancedPredictionEngine:
    def __init__(self):
        # 道瓊與台指的歷史相關係數 (可根據實際數據調整)
        self.dji_txf_correlation = 0.75
        self.dji_txf_ratio = 0.508  # 台指/道瓊的平均比例 (約21000/42000)
        
        # 美國期貨風氣權重
        self.us_futures_weight = 0.4
        
        # 台指期貨風氣權重  
        self.txf_sentiment_weight = 0.6
        
    def analyze_dji_to_txf_conversion(self, dji_data: Dict) -> Dict:
        """道瓊指數轉換台指期貨精準點位"""
        dji_close = dji_data["close"]
        dji_macd = dji_data["macd"]
        dji_signal = dji_data["signal"]
        dji_histogram = dji_data["histogram"]
        dji_rsi = dji_data["rsi"]
        
        # 基礎轉換點位
        base_txf_prediction = dji_close * self.dji_txf_ratio
        
        # 技術指標調整
        macd_adjustment = 0
        if dji_histogram > 0:  # MACD金叉
            macd_adjustment = abs(dji_histogram) * 2
        else:  # MACD死叉
            macd_adjustment = -abs(dji_histogram) * 2
            
        # RSI調整
        rsi_adjustment = 0
        if dji_rsi > 70:  # 超買
            rsi_adjustment = -(dji_rsi - 70) * 3
        elif dji_rsi < 30:  # 超賣
            rsi_adjustment = (30 - dji_rsi) * 3
            
        # 最終預測點位
        predicted_txf = base_txf_prediction + macd_adjustment + rsi_adjustment
        
        return {
            "base_prediction": round(base_txf_prediction),
            "macd_adjustment": round(macd_adjustment),
            "rsi_adjustment": round(rsi_adjustment),
            "final_prediction": round(predicted_txf),
            "confidence": self._calculate_dji_confidence(dji_data)
        }
    
    def analyze_us_futures_sentiment(self, market_data: Dict) -> Dict:
        """分析美國期貨買賣風氣"""
        dji_data = market_data["DJI"]
        ndx_data = market_data["NDX"]
        soxx_data = market_data["SOXX"]
        
        # 計算綜合RSI (道瓊 + 納指 + 半導體)
        combined_rsi = (dji_data["rsi"] + ndx_data["rsi"] + soxx_data["rsi"]) / 3
        
        # 計算MACD動能
        dji_momentum = dji_data["histogram"]
        ndx_momentum = ndx_data["histogram"] 
        soxx_momentum = soxx_data["histogram"]
        
        total_momentum = dji_momentum + ndx_momentum + soxx_momentum
        
        # 美國期貨風氣評分 (1-10)
        sentiment_score = 5  # 中性基準
        
        # RSI影響
        if combined_rsi > 70:
            sentiment_score += (combined_rsi - 70) / 10  # 超買增加樂觀
        elif combined_rsi < 30:
            sentiment_score -= (30 - combined_rsi) / 10  # 超賣增加悲觀
            
        # MACD動能影響
        if total_momentum > 0:
            sentiment_score += min(total_momentum / 5, 2)  # 最多加2分
        else:
            sentiment_score += max(total_momentum / 5, -2)  # 最多減2分
            
        sentiment_score = max(1, min(10, sentiment_score))  # 限制在1-10
        
        # 轉換為台指期貨點位影響
        sentiment_impact = (sentiment_score - 5) * 50  # 每分影響50點
        
        return {
            "sentiment_score": round(sentiment_score, 2),
            "combined_rsi": round(combined_rsi, 2),
            "total_momentum": round(total_momentum, 2),
            "txf_impact": round(sentiment_impact),
            "description": self._get_us_sentiment_description(sentiment_score)
        }
    
    def analyze_txf_sentiment(self, txf_data: Dict) -> Dict:
        """分析台指期貨買賣風氣"""
        close = txf_data["close"]
        volume = txf_data["volume"] 
        rsi = txf_data["rsi"]
        macd_histogram = txf_data["histogram"]
        
        # 成交量分析 (假設正常量能為50000-80000)
        normal_volume_min = 50000
        normal_volume_max = 80000
        
        volume_sentiment = 5  # 中性
        if volume > normal_volume_max:
            volume_sentiment += min((volume - normal_volume_max) / 10000, 3)
        elif volume < normal_volume_min:
            volume_sentiment -= min((normal_volume_min - volume) / 5000, 2)
            
        # RSI情緒分析
        rsi_sentiment = 5
        if rsi > 80:  # 極度超買，恐慌性追高
            rsi_sentiment += (rsi - 80) / 5
        elif rsi > 70:  # 超買，樂觀情緒
            rsi_sentiment += (rsi - 70) / 10
        elif rsi < 20:  # 極度超賣，恐慌性拋售
            rsi_sentiment -= (20 - rsi) / 5
        elif rsi < 30:  # 超賣，悲觀情緒
            rsi_sentiment -= (30 - rsi) / 10
            
        # MACD動能情緒
        macd_sentiment = 5
        if macd_histogram > 0:
            macd_sentiment += min(macd_histogram / 5, 2)
        else:
            macd_sentiment += max(macd_histogram / 5, -2)
            
        # 綜合台指風氣評分
        overall_sentiment = (volume_sentiment + rsi_sentiment + macd_sentiment) / 3
        overall_sentiment = max(1, min(10, overall_sentiment))
        
        # 轉換為點位影響
        sentiment_impact = (overall_sentiment - 5) * 80  # 每分影響80點
        
        return {
            "sentiment_score": round(overall_sentiment, 2),
            "volume_sentiment": round(volume_sentiment, 2),
            "rsi_sentiment": round(rsi_sentiment, 2),
            "macd_sentiment": round(macd_sentiment, 2),
            "volume": volume,
            "txf_impact": round(sentiment_impact),
            "description": self._get_txf_sentiment_description(overall_sentiment)
        }
    
    def generate_comprehensive_prediction(self, market_data: Dict) -> Dict:
        """生成綜合預測結果"""
        # 1. 道瓊轉換預測
        dji_prediction = self.analyze_dji_to_txf_conversion(market_data["DJI"])
        
        # 2. 美國期貨風氣分析
        us_sentiment = self.analyze_us_futures_sentiment(market_data)
        
        # 3. 台指期貨風氣分析  
        txf_sentiment = self.analyze_txf_sentiment(market_data["TXF1"])
        
        # 4. 綜合計算最終預測點位
        base_prediction = dji_prediction["final_prediction"]
        us_impact = us_sentiment["txf_impact"] * self.us_futures_weight
        txf_impact = txf_sentiment["txf_impact"] * self.txf_sentiment_weight
        
        final_prediction = base_prediction + us_impact + txf_impact
        
        # 5. 計算預測區間
        confidence_range = self._calculate_prediction_range(
            dji_prediction["confidence"], 
            us_sentiment["sentiment_score"], 
            txf_sentiment["sentiment_score"]
        )
        
        return {
            "current_price": market_data["TXF1"]["close"],
            "dji_based_prediction": dji_prediction,
            "us_futures_sentiment": us_sentiment,
            "txf_sentiment": txf_sentiment,
            "final_prediction": round(final_prediction),
            "prediction_range": {
                "lower": round(final_prediction - confidence_range),
                "upper": round(final_prediction + confidence_range)
            },
            "price_difference": round(final_prediction - market_data["TXF1"]["close"]),
            "recommendation": self._generate_trading_recommendation(
                final_prediction, market_data["TXF1"]["close"], us_sentiment, txf_sentiment
            )
        }
    
    def _calculate_dji_confidence(self, dji_data: Dict) -> float:
        """計算道瓊預測的信心度"""
        # 基於RSI和MACD的一致性
        rsi = dji_data["rsi"]
        histogram = dji_data["histogram"]
        
        confidence = 0.7  # 基礎信心度
        
        # RSI在合理範圍內增加信心度
        if 30 <= rsi <= 70:
            confidence += 0.2
        
        # MACD信號明確增加信心度
        if abs(histogram) > 10:
            confidence += 0.1
            
        return min(confidence, 0.95)
    
    def _calculate_prediction_range(self, dji_confidence: float, us_sentiment: float, txf_sentiment: float) -> int:
        """計算預測區間範圍"""
        base_range = 100
        
        # 信心度越低，區間越大
        confidence_factor = (1 - dji_confidence) * 100
        
        # 情緒極端程度影響區間
        us_extreme = abs(us_sentiment - 5) * 20
        txf_extreme = abs(txf_sentiment - 5) * 30
        
        total_range = base_range + confidence_factor + us_extreme + txf_extreme
        return round(total_range)
    
    def _get_us_sentiment_description(self, score: float) -> str:
        """美國期貨風氣描述"""
        if score >= 8:
            return "🔥 極度樂觀 - 強勁上漲動能"
        elif score >= 7:
            return "📈 樂觀 - 上漲趨勢明確"
        elif score >= 6:
            return "🟢 偏樂觀 - 溫和上漲"
        elif score >= 4:
            return "😐 中性 - 方向不明"
        elif score >= 3:
            return "🟡 偏悲觀 - 溫和下跌"
        elif score >= 2:
            return "📉 悲觀 - 下跌壓力明顯"
        else:
            return "❄️ 極度悲觀 - 恐慌性拋售"
    
    def _get_txf_sentiment_description(self, score: float) -> str:
        """台指期貨風氣描述"""
        if score >= 8:
            return "🚀 瘋狂追高 - 散戶FOMO情緒"
        elif score >= 7:
            return "💪 積極做多 - 買盤踴躍"
        elif score >= 6:
            return "👍 偏多氣氛 - 逢低承接"
        elif score >= 4:
            return "😶 觀望氣氛 - 量縮整理"
        elif score >= 3:
            return "😟 偏空氣氛 - 賣壓出現"
        elif score >= 2:
            return "😰 恐慌拋售 - 殺盤湧現"
        else:
            return "💀 絕望性拋售 - 無量下跌"
    
    def _generate_trading_recommendation(self, predicted_price: float, current_price: float, 
                                       us_sentiment: Dict, txf_sentiment: Dict) -> Dict:
        """生成交易建議"""
        price_diff = predicted_price - current_price
        
        if price_diff > 50:
            direction = "做多"
            confidence = "高"
            entry_strategy = "積極進場"
        elif price_diff > 20:
            direction = "偏多"
            confidence = "中"
            entry_strategy = "分批進場"
        elif price_diff > -20:
            direction = "觀望"
            confidence = "低"
            entry_strategy = "等待明確信號"
        elif price_diff > -50:
            direction = "偏空"
            confidence = "中"
            entry_strategy = "分批放空"
        else:
            direction = "做空"
            confidence = "高"
            entry_strategy = "積極放空"
            
        return {
            "direction": direction,
            "confidence": confidence,
            "entry_strategy": entry_strategy,
            "expected_move": f"{price_diff:+.0f}點",
            "risk_level": "高" if abs(price_diff) > 100 else "中" if abs(price_diff) > 50 else "低"
        } 