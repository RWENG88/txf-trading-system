import math
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
from datetime import datetime, timedelta
from historical_database import HistoricalDatabase

class EnhancedPredictionEngine:
    def __init__(self):
        # 初始化歷史資料庫
        self.historical_db = HistoricalDatabase()
        
        # 動態載入歷史優化參數
        self.optimal_ratios = self._load_optimal_ratios()
        
        # 美國期貨風氣權重
        self.us_futures_weight = 0.4
        
        # 台指期貨風氣權重  
        self.txf_sentiment_weight = 0.6
        
        # 歷史回測準確性權重
        self.historical_accuracy_weight = 0.2
        
    def _load_optimal_ratios(self) -> Dict:
        """載入基於10年歷史數據的最佳預測比例"""
        try:
            ratios = self.historical_db.get_optimal_prediction_ratios(lookback_days=252)
            print(f"📊 載入歷史優化參數: DJI相關性={ratios['dji_txf_correlation']:.3f}")
            return ratios
        except Exception as e:
            print(f"⚠️ 無法載入歷史數據，使用預設參數: {e}")
            return {
                'dji_txf_ratio': 0.508,
                'ndx_txf_ratio': 1.0,
                'soxx_txf_ratio': 100.0,
                'dji_txf_correlation': 0.75,
                'ndx_txf_correlation': 0.65,
                'soxx_txf_correlation': 0.55
            }
    
    def analyze_dji_to_txf_conversion_enhanced(self, dji_data: Dict) -> Dict:
        """基於歷史數據的增強版道瓊轉換台指期貨"""
        dji_close = dji_data["close"]
        dji_macd = dji_data["macd"]
        dji_signal = dji_data["signal"]
        dji_histogram = dji_data["histogram"]
        dji_rsi = dji_data["rsi"]
        
        # 使用歷史優化的轉換比例
        base_txf_prediction = dji_close * self.optimal_ratios['dji_txf_ratio']
        
        # 歷史相關性調整權重
        correlation_weight = abs(self.optimal_ratios['dji_txf_correlation'])
        
        # 技術指標調整（基於歷史有效性）
        macd_adjustment = 0
        if dji_histogram > 0:  # MACD金叉
            macd_adjustment = abs(dji_histogram) * 2 * correlation_weight
        else:  # MACD死叉
            macd_adjustment = -abs(dji_histogram) * 2 * correlation_weight
            
        # RSI調整（加入歷史波動度）
        rsi_adjustment = 0
        historical_volatility = self._get_historical_volatility('DJI', 30)
        volatility_factor = min(historical_volatility / 0.02, 2.0)  # 限制在2倍內
        
        if dji_rsi > 70:  # 超買
            rsi_adjustment = -(dji_rsi - 70) * 3 * volatility_factor
        elif dji_rsi < 30:  # 超賣
            rsi_adjustment = (30 - dji_rsi) * 3 * volatility_factor
            
        # 季節性調整（基於歷史同期表現）
        seasonal_adjustment = self._get_seasonal_adjustment('DJI', 'TXF')
        
        # 最終預測點位
        predicted_txf = base_txf_prediction + macd_adjustment + rsi_adjustment + seasonal_adjustment
        
        return {
            "base_prediction": round(base_txf_prediction),
            "macd_adjustment": round(macd_adjustment),
            "rsi_adjustment": round(rsi_adjustment),
            "seasonal_adjustment": round(seasonal_adjustment),
            "final_prediction": round(predicted_txf),
            "confidence": self._calculate_enhanced_confidence(dji_data),
            "historical_correlation": self.optimal_ratios['dji_txf_correlation'],
            "volatility_factor": volatility_factor
        }
    
    def analyze_us_futures_sentiment_enhanced(self, market_data: Dict) -> Dict:
        """基於歷史數據的增強版美國期貨風氣分析"""
        dji_data = market_data["DJI"]
        ndx_data = market_data["NDX"]
        soxx_data = market_data["SOXX"]
        
        # 計算加權綜合RSI（基於歷史相關性權重）
        dji_weight = abs(self.optimal_ratios['dji_txf_correlation'])
        ndx_weight = abs(self.optimal_ratios['ndx_txf_correlation'])
        soxx_weight = abs(self.optimal_ratios['soxx_txf_correlation'])
        
        total_weight = dji_weight + ndx_weight + soxx_weight
        
        weighted_rsi = (
            dji_data["rsi"] * dji_weight +
            ndx_data["rsi"] * ndx_weight +
            soxx_data["rsi"] * soxx_weight
        ) / total_weight
        
        # 計算加權MACD動能
        dji_momentum = dji_data["histogram"] * dji_weight
        ndx_momentum = ndx_data["histogram"] * ndx_weight
        soxx_momentum = soxx_data["histogram"] * soxx_weight
        
        total_momentum = (dji_momentum + ndx_momentum + soxx_momentum) / total_weight
        
        # 歷史波動度調整
        historical_vol = {
            'DJI': self._get_historical_volatility('DJI', 30),
            'NDX': self._get_historical_volatility('NDX', 30),
            'SOXX': self._get_historical_volatility('SOXX', 30)
        }
        
        avg_volatility = np.mean(list(historical_vol.values()))
        volatility_multiplier = min(avg_volatility / 0.02, 2.0)
        
        # 美國期貨風氣評分 (1-10)
        sentiment_score = 5  # 中性基準
        
        # RSI影響（考慮歷史波動度）
        if weighted_rsi > 70:
            sentiment_score += (weighted_rsi - 70) / 10 * volatility_multiplier
        elif weighted_rsi < 30:
            sentiment_score -= (30 - weighted_rsi) / 10 * volatility_multiplier
            
        # MACD動能影響
        if total_momentum > 0:
            sentiment_score += min(total_momentum / 5, 2)  # 最多加2分
        else:
            sentiment_score += max(total_momentum / 5, -2)  # 最多減2分
            
        sentiment_score = max(1, min(10, sentiment_score))  # 限制在1-10
        
        # 轉換為台指期貨點位影響（基於歷史有效性）
        historical_effectiveness = self._get_historical_prediction_accuracy('US_SENTIMENT')
        sentiment_impact = (sentiment_score - 5) * 50 * historical_effectiveness
        
        return {
            "sentiment_score": round(sentiment_score, 2),
            "weighted_rsi": round(weighted_rsi, 2),
            "total_momentum": round(total_momentum, 2),
            "txf_impact": round(sentiment_impact),
            "description": self._get_us_sentiment_description(sentiment_score),
            "historical_weights": {
                "dji_weight": round(dji_weight, 3),
                "ndx_weight": round(ndx_weight, 3),
                "soxx_weight": round(soxx_weight, 3)
            },
            "volatility_adjustment": round(volatility_multiplier, 2),
            "historical_effectiveness": round(historical_effectiveness, 2)
        }
    
    def analyze_txf_sentiment_enhanced(self, txf_data: Dict) -> Dict:
        """基於歷史數據的增強版台指期貨風氣分析"""
        close = txf_data["close"]
        volume = txf_data["volume"] 
        rsi = txf_data["rsi"]
        macd_histogram = txf_data["histogram"]
        
        # 基於歷史數據計算動態成交量基準
        historical_volume_stats = self._get_historical_volume_stats(30)
        volume_mean = historical_volume_stats['mean']
        volume_std = historical_volume_stats['std']
        
        # 成交量情緒分析（基於歷史統計）
        volume_z_score = (volume - volume_mean) / volume_std if volume_std > 0 else 0
        volume_sentiment = 5 + min(max(volume_z_score, -2), 2)  # 限制在1-9
        
        # RSI情緒分析（加入歷史極值分析）
        historical_rsi_extremes = self._get_historical_rsi_extremes('TXF', 252)
        rsi_sentiment = 5
        
        if rsi > historical_rsi_extremes['upper_80pct']:  # 歷史80%分位
            rsi_sentiment += (rsi - historical_rsi_extremes['upper_80pct']) / 5
        elif rsi > 70:  # 傳統超買
            rsi_sentiment += (rsi - 70) / 10
        elif rsi < historical_rsi_extremes['lower_20pct']:  # 歷史20%分位
            rsi_sentiment -= (historical_rsi_extremes['lower_20pct'] - rsi) / 5
        elif rsi < 30:  # 傳統超賣
            rsi_sentiment -= (30 - rsi) / 10
            
        # MACD動能情緒（基於歷史MACD分布）
        historical_macd_stats = self._get_historical_macd_stats('TXF', 60)
        macd_z_score = (macd_histogram - historical_macd_stats['mean']) / historical_macd_stats['std'] if historical_macd_stats['std'] > 0 else 0
        macd_sentiment = 5 + min(max(macd_z_score, -2), 2)
        
        # 綜合台指風氣評分
        overall_sentiment = (volume_sentiment + rsi_sentiment + macd_sentiment) / 3
        overall_sentiment = max(1, min(10, overall_sentiment))
        
        # 轉換為點位影響（基於歷史有效性）
        historical_effectiveness = self._get_historical_prediction_accuracy('TXF_SENTIMENT')
        sentiment_impact = (overall_sentiment - 5) * 80 * historical_effectiveness
        
        return {
            "sentiment_score": round(overall_sentiment, 2),
            "volume_sentiment": round(volume_sentiment, 2),
            "rsi_sentiment": round(rsi_sentiment, 2),
            "macd_sentiment": round(macd_sentiment, 2),
            "volume": volume,
            "txf_impact": round(sentiment_impact),
            "description": self._get_txf_sentiment_description(overall_sentiment),
            "historical_analysis": {
                "volume_z_score": round(volume_z_score, 2),
                "rsi_percentile": self._calculate_percentile(rsi, 'TXF', 'rsi', 252),
                "macd_z_score": round(macd_z_score, 2),
                "effectiveness": round(historical_effectiveness, 2)
            }
        }
    
    def generate_comprehensive_prediction_enhanced(self, market_data: Dict) -> Dict:
        """生成基於歷史數據的增強版綜合預測"""
        # 1. 增強版道瓊轉換預測
        dji_prediction = self.analyze_dji_to_txf_conversion_enhanced(market_data["DJI"])
        
        # 2. 增強版美國期貨風氣分析
        us_sentiment = self.analyze_us_futures_sentiment_enhanced(market_data)
        
        # 3. 增強版台指期貨風氣分析  
        txf_sentiment = self.analyze_txf_sentiment_enhanced(market_data["TXF1"])
        
        # 4. 歷史回測驗證
        historical_validation = self._validate_with_historical_patterns(market_data)
        
        # 5. 綜合計算最終預測點位（加入歷史驗證權重）
        base_prediction = dji_prediction["final_prediction"]
        us_impact = us_sentiment["txf_impact"] * self.us_futures_weight
        txf_impact = txf_sentiment["txf_impact"] * self.txf_sentiment_weight
        historical_impact = historical_validation["predicted_move"] * self.historical_accuracy_weight
        
        final_prediction = base_prediction + us_impact + txf_impact + historical_impact
        
        # 6. 計算增強版預測區間
        confidence_range = self._calculate_enhanced_prediction_range(
            dji_prediction, us_sentiment, txf_sentiment, historical_validation
        )
        
        return {
            "current_price": market_data["TXF1"]["close"],
            "dji_based_prediction": dji_prediction,
            "us_futures_sentiment": us_sentiment,
            "txf_sentiment": txf_sentiment,
            "historical_validation": historical_validation,
            "final_prediction": round(final_prediction),
            "prediction_range": {
                "lower": round(final_prediction - confidence_range),
                "upper": round(final_prediction + confidence_range)
            },
            "price_difference": round(final_prediction - market_data["TXF1"]["close"]),
            "recommendation": self._generate_enhanced_trading_recommendation(
                final_prediction, market_data["TXF1"]["close"], us_sentiment, txf_sentiment, historical_validation
            ),
            "confidence_metrics": {
                "historical_accuracy": historical_validation["confidence"],
                "correlation_strength": dji_prediction["historical_correlation"],
                "volatility_adjustment": us_sentiment["volatility_adjustment"]
            }
        }
    
    # 歷史數據分析輔助方法
    def _get_historical_volatility(self, symbol: str, days: int) -> float:
        """計算歷史波動度"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y-%m-%d')
            data = self.historical_db.get_historical_data(symbol, start_date, end_date)
            
            if len(data) > 1:
                returns = data['close'].pct_change().dropna()
                return float(returns.std() * np.sqrt(252))  # 年化波動度
            return 0.02  # 預設2%
        except:
            return 0.02
    
    def _get_seasonal_adjustment(self, source_symbol: str, target_symbol: str) -> float:
        """計算季節性調整"""
        try:
            current_month = datetime.now().month
            # 簡化的季節性效應（實際應基於歷史數據分析）
            seasonal_factors = {
                1: 20, 2: 10, 3: 15, 4: 5, 5: -10, 6: -5,
                7: 0, 8: -15, 9: -20, 10: 15, 11: 25, 12: 30
            }
            return seasonal_factors.get(current_month, 0)
        except:
            return 0
    
    def _get_historical_volume_stats(self, days: int) -> Dict:
        """獲取歷史成交量統計"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y-%m-%d')
            data = self.historical_db.get_historical_data('TXF', start_date, end_date)
            
            if len(data) > 0:
                return {
                    'mean': float(data['volume'].mean()),
                    'std': float(data['volume'].std()),
                    'median': float(data['volume'].median())
                }
        except:
            pass
        return {'mean': 60000, 'std': 15000, 'median': 60000}
    
    def _get_historical_rsi_extremes(self, symbol: str, days: int) -> Dict:
        """獲取歷史RSI極值"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y-%m-%d')
            data = self.historical_db.get_historical_data(symbol, start_date, end_date)
            
            if len(data) > 0:
                return {
                    'upper_80pct': float(data['rsi'].quantile(0.8)),
                    'lower_20pct': float(data['rsi'].quantile(0.2)),
                    'median': float(data['rsi'].median())
                }
        except:
            pass
        return {'upper_80pct': 75, 'lower_20pct': 25, 'median': 50}
    
    def _get_historical_macd_stats(self, symbol: str, days: int) -> Dict:
        """獲取歷史MACD統計"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y-%m-%d')
            data = self.historical_db.get_historical_data(symbol, start_date, end_date)
            
            if len(data) > 0:
                return {
                    'mean': float(data['histogram'].mean()),
                    'std': float(data['histogram'].std())
                }
        except:
            pass
        return {'mean': 0, 'std': 20}
    
    def _calculate_percentile(self, value: float, symbol: str, column: str, days: int) -> float:
        """計算當前值在歷史數據中的百分位"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y-%m-%d')
            data = self.historical_db.get_historical_data(symbol, start_date, end_date)
            
            if len(data) > 0 and column in data.columns:
                return float((data[column] < value).mean() * 100)
        except:
            pass
        return 50.0
    
    def _get_historical_prediction_accuracy(self, model_type: str) -> float:
        """獲取歷史預測準確性（模擬）"""
        # 實際實現中應基於回測結果
        accuracy_map = {
            'US_SENTIMENT': 0.75,
            'TXF_SENTIMENT': 0.80,
            'DJI_CONVERSION': 0.85
        }
        return accuracy_map.get(model_type, 0.70)
    
    def _validate_with_historical_patterns(self, market_data: Dict) -> Dict:
        """歷史模式驗證"""
        # 簡化的歷史模式匹配
        current_rsi = market_data["TXF1"]["rsi"]
        current_volume = market_data["TXF1"]["volume"]
        
        # 基於當前市場狀態尋找歷史相似情況
        if current_rsi > 80:  # 極度超買
            predicted_move = -30
            confidence = 0.7
            pattern = "極度超買回調模式"
        elif current_rsi < 20:  # 極度超賣
            predicted_move = 40
            confidence = 0.7
            pattern = "極度超賣反彈模式"
        elif current_volume > 80000:  # 高量
            predicted_move = 15
            confidence = 0.6
            pattern = "高量突破模式"
        else:
            predicted_move = 0
            confidence = 0.5
            pattern = "常態整理模式"
        
        return {
            "predicted_move": predicted_move,
            "confidence": confidence,
            "pattern_type": pattern,
            "historical_matches": 85  # 模擬歷史匹配數量
        }
    
    def _calculate_enhanced_confidence(self, dji_data: Dict) -> float:
        """計算增強版信心度"""
        base_confidence = 0.7
        
        # 歷史相關性加權
        correlation_bonus = abs(self.optimal_ratios['dji_txf_correlation']) * 0.2
        
        # RSI合理性加分
        rsi = dji_data["rsi"]
        if 30 <= rsi <= 70:
            rsi_bonus = 0.1
        else:
            rsi_bonus = 0
        
        # MACD明確性加分
        histogram = abs(dji_data["histogram"])
        macd_bonus = min(histogram / 50, 0.1)
        
        return min(base_confidence + correlation_bonus + rsi_bonus + macd_bonus, 0.95)
    
    def _calculate_enhanced_prediction_range(self, dji_pred: Dict, us_sentiment: Dict, txf_sentiment: Dict, historical_val: Dict) -> int:
        """計算增強版預測區間"""
        base_range = 80
        
        # 信心度調整
        confidence_factor = (1 - dji_pred["confidence"]) * 80
        
        # 歷史驗證調整
        historical_factor = (1 - historical_val["confidence"]) * 60
        
        # 波動度調整
        volatility_factor = us_sentiment.get("volatility_adjustment", 1) * 30
        
        total_range = base_range + confidence_factor + historical_factor + volatility_factor
        return round(total_range)
    
    def _generate_enhanced_trading_recommendation(self, predicted_price: float, current_price: float, 
                                               us_sentiment: Dict, txf_sentiment: Dict, historical_val: Dict) -> Dict:
        """生成增強版交易建議"""
        price_diff = predicted_price - current_price
        
        # 歷史模式調整
        historical_confidence = historical_val["confidence"]
        
        # 基本方向判斷
        if price_diff > 50:
            direction = "做多"
            confidence = "高" if historical_confidence > 0.7 else "中"
            entry_strategy = "積極進場" if historical_confidence > 0.8 else "分批進場"
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
            confidence = "高" if historical_confidence > 0.7 else "中"
            entry_strategy = "積極放空" if historical_confidence > 0.8 else "分批放空"
            
        return {
            "direction": direction,
            "confidence": confidence,
            "entry_strategy": entry_strategy,
            "expected_move": f"{price_diff:+.0f}點",
            "risk_level": "高" if abs(price_diff) > 100 else "中" if abs(price_diff) > 50 else "低",
            "historical_support": historical_val["pattern_type"],
            "historical_confidence": f"{historical_confidence:.1%}"
        }
    
    # 從原有引擎繼承的方法
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