import json, os, sys, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = "http://localhost:8000"
def call(m, path, body=None, tok=None, form=None, timeout=1800):
    h = {}
    if tok: h["Authorization"] = "Bearer " + tok
    data = urllib.parse.urlencode(form).encode() if form else (json.dumps(body).encode() if body is not None else (b"" if m == "POST" else None))
    if body is not None: h["Content-Type"] = "application/json"
    try:
        r = urllib.request.urlopen(urllib.request.Request(B + path, method=m, data=data, headers=h), timeout=timeout); return r.status, r.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
def login():
    return json.loads(call("POST", "/auth/login", form={"username": os.environ.get("LOOM_USER","admin"), "password": os.environ["LOOM_PASSWORD"]})[1])["access_token"]
def sse(r, log=None, mostrar=("inicio", "item_listo", "completado", "error")):
    eventos = []
    for l in r.decode("utf-8").split("\n\n"):
        if l.startswith("data:"):
            e = json.loads(l[5:]); eventos.append(e)
            if e["tipo"] in mostrar: print(f"  [{e['tipo']}]", (e.get("mensaje") or "")[:200])
    if log:
        open(log, "w", encoding="utf-8").write(json.dumps(eventos, ensure_ascii=False, indent=1))
    return eventos
