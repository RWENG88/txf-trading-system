import websocket
import json
import threading
import time
import random
import string

class TradingViewDataFetcher:
    def __init__(self):
        self.ws = None
        self.session_id = self._generate_session_id()
        self.quote_session_id = self._generate_session_id()
        self.is_connected = False
        
    def _generate_session_id(self):
        """生成隨機的session ID"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    def _create_message(self, func, params=None):
        """創建WebSocket消息格式"""
        if params is None:
            params = []
        return f"~m~{len(str({'m': func, 'p': params}))}~m~{json.dumps({'m': func, 'p': params})}"
    
    def on_message(self, ws, message):
        """處理收到的消息"""
        try:
            # TradingView的消息格式需要解析
            if "~m~" in message:
                parts = message.split("~m~")
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts):
                        try:
                            data = json.loads(parts[i + 1])
                            if 'm' in data and data['m'] == 'qsd':
                                # 處理報價數據
                                self._process_quote_data(data)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"處理消息時發生錯誤: {e}")
    
    def _process_quote_data(self, data):
        """處理報價數據"""
        if 'p' in data and len(data['p']) > 1:
            quote_data = data['p'][1]
            if isinstance(quote_data, dict):
                print(f"收到TXF1!數據: {quote_data}")
                # 這裡可以將數據傳遞給您的策略
                self._update_strategy_data(quote_data)
    
    def _update_strategy_data(self, quote_data):
        """更新策略數據"""
        # 提取需要的數據
        if 'v' in quote_data:
            for key, value in quote_data['v'].items():
                if key == 'lp':  # last price
                    print(f"台指期貨最新價格: {value}")
                elif key == 'volume':
                    print(f"成交量: {value}")
                elif key == 'ch':  # change
                    print(f"漲跌: {value}")
    
    def on_error(self, ws, error):
        print(f"WebSocket錯誤: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket連接已關閉")
        self.is_connected = False
    
    def on_open(self, ws):
        print("WebSocket連接已建立")
        self.is_connected = True
        
        # 發送初始化消息
        self._send_initial_messages()
        
        # 訂閱台指期貨數據
        self._subscribe_to_txf()
    
    def _send_initial_messages(self):
        """發送初始化消息"""
        # 設置會話
        self.ws.send(self._create_message("set_auth_token", ["unauthorized_user_token"]))
        self.ws.send(self._create_message("quote_create_session", [self.quote_session_id]))
        
    def _subscribe_to_txf(self):
        """訂閱台指期貨數據"""
        # 訂閱TXF1! (台指期貨)
        symbol = "TAIFEX:TXF1!"
        self.ws.send(self._create_message("quote_add_symbols", [
            self.quote_session_id,
            symbol,
            {"flags": ["force_permission"]}
        ]))
        print(f"已訂閱 {symbol}")
    
    def connect(self):
        """建立WebSocket連接"""
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            "wss://data.tradingview.com/socket.io/websocket",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # 在新線程中運行
        self.ws.run_forever()
    
    def start(self):
        """啟動數據獲取"""
        thread = threading.Thread(target=self.connect)
        thread.daemon = True
        thread.start()
        return thread

# 使用範例
def main():
    fetcher = TradingViewDataFetcher()
    
    print("正在連接TradingView...")
    thread = fetcher.start()
    
    try:
        # 保持程序運行
        while True:
            time.sleep(1)
            if not fetcher.is_connected:
                print("連接斷開，嘗試重新連接...")
                thread = fetcher.start()
                time.sleep(5)
    except KeyboardInterrupt:
        print("程序已停止")

if __name__ == "__main__":
    main() 