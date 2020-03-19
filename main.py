from fastapi import FastAPI
import mysql.connector as mysql
import requests
import json
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Message": "This is the BoomBox API - Docs at http://37.120.178.44:8000/docs"}

@app.get("/chat/check")
def registernewuser(uuid: str, name: str):
    db = mysql.connect(host="localhost",user='chat', password='placeholder', database='chat')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chatuser WHERE uuid=%s", (uuid,))
    result = cursor.fetchall()
    lines = cursor.rowcount
    if lines == 0:
        cursor.execute("INSERT INTO chatuser(`name`,`uuid`,`ban`) VALUES ('{0}','{1}','0')".format(name,uuid))
        db.commit()
        db.close()
        return {"status":"0"}
    if lines == 1:
            for row in result:
                return {"status": row[2]}

@app.get("/live/song")
async def current_song():
    url = "https://api.spotify.com/v1/me/player/currently-playing"

    payload = {}
    headers = {
      'Authorization': 'Bearer BQBUj0Y-Emq-DgUG2EfxQtiB6HhAL8SZ8p56J2WIhlEArmQFBCZWmeWSY-XrTWeQOId-phW1scQq6pt6q8AZiPTUHwWcT4XLYDTwhfE2QzpqWBGYzrdoWtDwsKl-KFmjFGME_G5Ecg_Sm7XwG0W7M-nqtS8'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    rep = json.loads(response.text.encode('utf8'))
    img = rep['item']['album']['images'][1]['url']

    artist = json.loads(json.dumps(rep['item']['artists']))
    return{"song":rep['item']['name'], "artist":artist[0]['name'], "image": img}
