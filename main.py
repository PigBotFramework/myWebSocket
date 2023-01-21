import websocket, json, requests, traceback

CLIENT_ID = "123"
CLIENT_SECRET = "123"
HTTP_URL = "http://173.82.136.177:4376"

class myWebSocket:
    def __init__(self, client_id, client_secret, client_url="wss://socket.xzynb.top/ws"):
        self.ws = websocket.WebSocket()
        self.ws.connect(client_url)
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_url = client_url
        self.send("init")

    def send(self, type, data={}, flag="flag"):
        params = {
            "type": type,
            "data": data,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "flag": flag
        }
        self.ws.send(json.dumps(params))
    
    def recv(self, echo=None):
        return json.loads(self.ws.recv())

if __name__ == "__main__":
    ws = myWebSocket(CLIENT_ID, CLIENT_SECRET)
    while True:
        recv = ws.recv()
        print(recv)
        try:
            if recv.get("type") == "execute":
                name = recv.get("data").get("name")
                params = recv.get("data").get("params")
                data = requests.post(f"{HTTP_URL}/{name}", params).json()
                data['flag'] = recv.get("flag")
                ws.send("return", data, recv.get("flag"))
        except Exception as e:
            print("There is an error:"+str(e))
            ws.send("error", {"msg":str(e),"detail":traceback.format_exc()}, recv.get("flag"))