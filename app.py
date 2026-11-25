import os, hmac, hashlib, json, time
from urllib.parse import parse_qsl
from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BOT_TOKEN=os.environ.get("BOT_TOKEN", "")
app=FastAPI(title="POLUS SKINS API")

def verify_init_data(init_data: str):
    if not BOT_TOKEN or not init_data: raise HTTPException(401,"Telegram authentication required")
    data=dict(parse_qsl(init_data, keep_blank_values=True))
    received=data.pop("hash",None)
    if not received: raise HTTPException(401,"Invalid initData")
    check="\n".join(f"{k}={v}" for k,v in sorted(data.items()))
    secret=hmac.new(b"WebAppData",BOT_TOKEN.encode(),hashlib.sha256).digest()
    expected=hmac.new(secret,check.encode(),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,received): raise HTTPException(401,"Invalid Telegram signature")
    auth_date=int(data.get("auth_date","0"))
    if abs(time.time()-auth_date)>86400: raise HTTPException(401,"Expired initData")
    user=json.loads(data.get("user","{}"))
    if not user.get("id"): raise HTTPException(401,"Telegram user missing")
    return user

@app.get("/api/health")
def health(): return {"ok":True,"service":"POLUS SKINS"}

@app.get("/api/me")
def me(x_telegram_init_data: str=Header(default="")):
    user=verify_init_data(x_telegram_init_data)
    return {"id":user["id"],"first_name":user.get("first_name","")}

@app.get("/api/catalog")
def catalog():
    return {"items":[{"id":"classic","name":"Classic","price":229,"deadline_days":2},{"id":"classic_plus","name":"Classic+","price":329,"deadline_days":2},{"id":"future","name":"Future","price":389,"deadline_days":2},{"id":"vip","name":"VIP","price":589,"deadline_days":2},{"id":"vip_plus","name":"VIP+","price":789,"deadline_days":1}]}

app.mount("/",StaticFiles(directory=Path(__file__).parent.parent/"webapp",html=True),name="webapp")
