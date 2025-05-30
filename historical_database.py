import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import sqlite3
from pathlib import Path

class HistoricalDatabase:
    def __init__(self, db_path: str = "data/historical_futures.db"):
        self.db_path = db_path
        self.ensure_database_exists()
        
    def ensure_database_exists(self):
        """確保資料庫存在並創建必要的表格"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 創建台指期貨歷史數據表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS txf_history (
                    date TEXT PRIMARY KEY,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    macd REAL,
                    signal REAL,
                    histogram REAL,
                    rsi REAL,
                    rsi_ma REAL
                )
            ''')
            
            # 創建道瓊指數歷史數據表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dji_history (
                    date TEXT PRIMARY KEY,
                    close REAL,
                    macd REAL,
                    signal REAL,
                    histogram REAL,
                    rsi REAL,
                    rsi_ma REAL
                )
            ''')
            
            # 創建納指歷史數據表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ndx_history (
                    date TEXT PRIMARY KEY,
                    close REAL,
                    macd REAL,
                    signal REAL,
                    histogram REAL,
                    rsi REAL,
                    rsi_ma REAL
                )
            ''')
            
            # 創建半導體指數歷史數據表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS soxx_history (
                    date TEXT PRIMARY KEY,
                    close REAL,
                    macd REAL,
                    signal REAL,
                    histogram REAL,
                    rsi REAL,
                    rsi_ma REAL
                )
            ''')
            
            # 創建相關性分析表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS correlation_analysis (
                    date_from TEXT,
                    date_to TEXT,
                    dji_txf_correlation REAL,
                    ndx_txf_correlation REAL,
                    soxx_txf_correlation REAL,
                    created_at TEXT,
                    PRIMARY KEY (date_from, date_to)
                )
            ''')
            
            conn.commit()
    
    def insert_sample_data(self):
        """插入樣本歷史數據（模擬近10年數據）"""
        print("📊 正在生成近10年歷史數據樣本...")
        
        # 生成從2015年到現在的數據
        start_date = datetime(2015, 1, 1)
        end_date = datetime.now()
        
        # 基礎價格設定
        txf_base = 9000  # 2015年台指期約9000點
        dji_base = 18000  # 2015年道瓊約18000點
        ndx_base = 4000   # 2015年納指約4000點
        soxx_base = 90    # 2015年半導體約90點
        
        data_points = []
        current_date = start_date
        
        while current_date <= end_date:
            # 計算天數進展（用於模擬長期上升趨勢）
            days_from_start = (current_date - start_date).days
            trend_factor = 1 + (days_from_start / 3650) * 1.2  # 10年上升約120%
            
            # 加入隨機波動
            daily_volatility = np.random.normal(0, 0.02)  # 2%日波動
            
            # 計算各指數價格
            txf_price = txf_base * trend_factor * (1 + daily_volatility)
            dji_price = dji_base * trend_factor * (1 + daily_volatility * 0.8)
            ndx_price = ndx_base * trend_factor * (1 + daily_volatility * 1.2)
            soxx_price = soxx_base * trend_factor * (1 + daily_volatility * 1.5)
            
            # 生成技術指標（模擬）
            rsi_txf = 50 + np.random.normal(0, 20)
            rsi_dji = 50 + np.random.normal(0, 15)
            rsi_ndx = 50 + np.random.normal(0, 18)
            rsi_soxx = 50 + np.random.normal(0, 25)
            
            # 限制RSI範圍
            rsi_txf = max(10, min(90, rsi_txf))
            rsi_dji = max(10, min(90, rsi_dji))
            rsi_ndx = max(10, min(90, rsi_ndx))
            rsi_soxx = max(10, min(90, rsi_soxx))
            
            # MACD指標
            macd_txf = np.random.normal(0, 50)
            histogram_txf = np.random.normal(0, 20)
            
            macd_dji = np.random.normal(0, 200)
            histogram_dji = np.random.normal(0, 50)
            
            macd_ndx = np.random.normal(0, 300)
            histogram_ndx = np.random.normal(0, 80)
            
            macd_soxx = np.random.normal(0, 5)
            histogram_soxx = np.random.normal(0, 2)
            
            # 成交量（TXF）
            volume = int(np.random.normal(60000, 15000))
            volume = max(20000, volume)
            
            data_point = {
                'date': current_date.strftime('%Y-%m-%d'),
                'txf': {
                    'open': round(txf_price * 0.999, 0),
                    'high': round(txf_price * 1.01, 0),
                    'low': round(txf_price * 0.99, 0),
                    'close': round(txf_price, 0),
                    'volume': volume,
                    'macd': round(macd_txf, 2),
                    'signal': round(macd_txf - histogram_txf, 2),
                    'histogram': round(histogram_txf, 2),
                    'rsi': round(rsi_txf, 2),
                    'rsi_ma': round(rsi_txf, 2)
                },
                'dji': {
                    'close': round(dji_price, 1),
                    'macd': round(macd_dji, 2),
                    'signal': round(macd_dji - histogram_dji, 2),
                    'histogram': round(histogram_dji, 2),
                    'rsi': round(rsi_dji, 2),
                    'rsi_ma': round(rsi_dji, 2)
                },
                'ndx': {
                    'close': round(ndx_price, 2),
                    'macd': round(macd_ndx, 2),
                    'signal': round(macd_ndx - histogram_ndx, 2),
                    'histogram': round(histogram_ndx, 2),
                    'rsi': round(rsi_ndx, 2),
                    'rsi_ma': round(rsi_ndx, 2)
                },
                'soxx': {
                    'close': round(soxx_price, 2),
                    'macd': round(macd_soxx, 2),
                    'signal': round(macd_soxx - histogram_soxx, 2),
                    'histogram': round(histogram_soxx, 2),
                    'rsi': round(rsi_soxx, 2),
                    'rsi_ma': round(rsi_soxx, 2)
                }
            }
            
            data_points.append(data_point)
            current_date += timedelta(days=1)
            
            # 跳過週末
            if current_date.weekday() >= 5:
                current_date += timedelta(days=2)
        
        # 批次插入數據
        self._batch_insert_data(data_points)
        print(f"✅ 已生成 {len(data_points)} 個交易日的歷史數據")
    
    def _batch_insert_data(self, data_points: List[Dict]):
        """批次插入歷史數據"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for data in data_points:
                date = data['date']
                
                # 插入TXF數據
                cursor.execute('''
                    INSERT OR REPLACE INTO txf_history 
                    (date, open, high, low, close, volume, macd, signal, histogram, rsi, rsi_ma)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date, data['txf']['open'], data['txf']['high'], data['txf']['low'],
                    data['txf']['close'], data['txf']['volume'], data['txf']['macd'],
                    data['txf']['signal'], data['txf']['histogram'], data['txf']['rsi'], data['txf']['rsi_ma']
                ))
                
                # 插入DJI數據
                cursor.execute('''
                    INSERT OR REPLACE INTO dji_history 
                    (date, close, macd, signal, histogram, rsi, rsi_ma)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date, data['dji']['close'], data['dji']['macd'], data['dji']['signal'],
                    data['dji']['histogram'], data['dji']['rsi'], data['dji']['rsi_ma']
                ))
                
                # 插入NDX數據
                cursor.execute('''
                    INSERT OR REPLACE INTO ndx_history 
                    (date, close, macd, signal, histogram, rsi, rsi_ma)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date, data['ndx']['close'], data['ndx']['macd'], data['ndx']['signal'],
                    data['ndx']['histogram'], data['ndx']['rsi'], data['ndx']['rsi_ma']
                ))
                
                # 插入SOXX數據
                cursor.execute('''
                    INSERT OR REPLACE INTO soxx_history 
                    (date, close, macd, signal, histogram, rsi, rsi_ma)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date, data['soxx']['close'], data['soxx']['macd'], data['soxx']['signal'],
                    data['soxx']['histogram'], data['soxx']['rsi'], data['soxx']['rsi_ma']
                ))
            
            conn.commit()
    
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """獲取指定期間的歷史數據"""
        table_map = {
            'TXF': 'txf_history',
            'DJI': 'dji_history', 
            'NDX': 'ndx_history',
            'SOXX': 'soxx_history'
        }
        
        table_name = table_map.get(symbol.upper())
        if not table_name:
            raise ValueError(f"不支持的指數: {symbol}")
        
        query = f"""
            SELECT * FROM {table_name} 
            WHERE date >= ? AND date <= ?
            ORDER BY date
        """
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            df['date'] = pd.to_datetime(df['date'])
            return df
    
    def calculate_correlation_matrix(self, start_date: str, end_date: str) -> Dict:
        """計算指定期間的相關性矩陣"""
        # 獲取各指數數據
        txf_data = self.get_historical_data('TXF', start_date, end_date)
        dji_data = self.get_historical_data('DJI', start_date, end_date)
        ndx_data = self.get_historical_data('NDX', start_date, end_date)
        soxx_data = self.get_historical_data('SOXX', start_date, end_date)
        
        # 創建價格變化率數據框
        price_changes = pd.DataFrame({
            'TXF': txf_data['close'].pct_change(),
            'DJI': dji_data['close'].pct_change(),
            'NDX': ndx_data['close'].pct_change(),
            'SOXX': soxx_data['close'].pct_change()
        }).dropna()
        
        # 計算相關性
        correlation_matrix = price_changes.corr()
        
        result = {
            'dji_txf_correlation': correlation_matrix.loc['DJI', 'TXF'],
            'ndx_txf_correlation': correlation_matrix.loc['NDX', 'TXF'],
            'soxx_txf_correlation': correlation_matrix.loc['SOXX', 'TXF'],
            'period': f"{start_date} to {end_date}",
            'data_points': len(price_changes),
            'full_matrix': correlation_matrix.to_dict()
        }
        
        # 儲存相關性分析結果
        self._save_correlation_analysis(start_date, end_date, result)
        
        return result
    
    def _save_correlation_analysis(self, start_date: str, end_date: str, result: Dict):
        """儲存相關性分析結果"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO correlation_analysis 
                (date_from, date_to, dji_txf_correlation, ndx_txf_correlation, soxx_txf_correlation, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                start_date, end_date,
                result['dji_txf_correlation'],
                result['ndx_txf_correlation'], 
                result['soxx_txf_correlation'],
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def get_optimal_prediction_ratios(self, lookback_days: int = 252) -> Dict:
        """基於歷史數據計算最佳預測比例"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=lookback_days * 2)).strftime('%Y-%m-%d')
        
        # 獲取歷史相關性
        correlation_data = self.calculate_correlation_matrix(start_date, end_date)
        
        # 計算動態轉換比例
        dji_txf_ratio = self._calculate_dynamic_ratio('DJI', 'TXF', start_date, end_date)
        ndx_txf_ratio = self._calculate_dynamic_ratio('NDX', 'TXF', start_date, end_date)
        soxx_txf_ratio = self._calculate_dynamic_ratio('SOXX', 'TXF', start_date, end_date)
        
        return {
            'dji_txf_ratio': dji_txf_ratio,
            'ndx_txf_ratio': ndx_txf_ratio,
            'soxx_txf_ratio': soxx_txf_ratio,
            'dji_txf_correlation': correlation_data['dji_txf_correlation'],
            'ndx_txf_correlation': correlation_data['ndx_txf_correlation'],
            'soxx_txf_correlation': correlation_data['soxx_txf_correlation'],
            'lookback_period': lookback_days,
            'calculated_at': datetime.now().isoformat()
        }
    
    def _calculate_dynamic_ratio(self, source_symbol: str, target_symbol: str, start_date: str, end_date: str) -> float:
        """計算兩個指數之間的動態比例"""
        source_data = self.get_historical_data(source_symbol, start_date, end_date)
        target_data = self.get_historical_data(target_symbol, start_date, end_date)
        
        if len(source_data) == 0 or len(target_data) == 0:
            # 如果沒有歷史數據，使用預設比例
            default_ratios = {
                ('DJI', 'TXF'): 0.508,
                ('NDX', 'TXF'): 1.0,
                ('SOXX', 'TXF'): 100.0
            }
            return default_ratios.get((source_symbol, target_symbol), 1.0)
        
        # 計算平均比例
        ratios = target_data['close'] / source_data['close']
        return float(ratios.mean())
    
    def get_database_stats(self) -> Dict:
        """獲取資料庫統計信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            tables = ['txf_history', 'dji_history', 'ndx_history', 'soxx_history']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*), MIN(date), MAX(date) FROM {table}")
                count, min_date, max_date = cursor.fetchone()
                stats[table] = {
                    'record_count': count,
                    'date_range': f"{min_date} to {max_date}" if min_date else "No data"
                }
            
            return stats

# 使用範例和測試函數
def initialize_historical_database():
    """初始化歷史資料庫"""
    print("🗄️ 初始化歷史資料庫...")
    db = HistoricalDatabase()
    
    # 檢查是否需要生成樣本數據
    stats = db.get_database_stats()
    if stats['txf_history']['record_count'] == 0:
        print("📊 資料庫為空，生成歷史樣本數據...")
        db.insert_sample_data()
    
    # 計算近期相關性
    print("📈 計算近期市場相關性...")
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    correlation_result = db.calculate_correlation_matrix(start_date, end_date)
    
    print("✅ 歷史資料庫初始化完成")
    print(f"📊 資料庫統計: {stats}")
    print(f"📈 近一年相關性分析: {correlation_result}")
    
    return db

if __name__ == "__main__":
    db = initialize_historical_database() 