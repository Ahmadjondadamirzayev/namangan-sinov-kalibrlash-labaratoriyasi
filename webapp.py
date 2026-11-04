import hashlib, hmac, json, os, time, uuid
from pathlib import Path
from urllib.parse import parse_qsl

from aiohttp import web

BASE = Path(__file__).parent
DIST = BASE / "miniapp" / "dist"  # npm run build natijasi
DATA = BASE / "data"
UPLOADS = DATA / "uploads"
DB = DATA / "items.json"

# Admin: Telegram username (kichik harflarda, @ belgisisiz). Bir nechta qo'shish mumkin.
ADMINS = {"dmya_4779"}

# Ruxsat etilgan rasm turlari
ALLOWED = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    ".bmp": "image/bmp", ".avif": "image/avif",
}


def load():
    return json.loads(DB.read_text("utf-8")) if DB.exists() else []


def save(items):
    DB.write_text(json.dumps(items, ensure_ascii=False, indent=1), "utf-8")


def is_admin(request) -> bool:
    """Telegram initData imzosini tekshiradi (soxtalashtirib bo'lmaydi)."""
    raw = request.headers.get("X-Init-Data", "")
    if not raw:
        return False
    d = dict(parse_qsl(raw, keep_blank_values=True))
    got = d.pop("hash", "")
    check = "\n".join(f"{k}={v}" for k, v in sorted(d.items()))
    secret = hmac.new(b"WebAppData", request.app["token"].encode(), hashlib.sha256).digest()
    calc = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calc, got):
        return False
    if time.time() - int(d.get("auth_date", "0") or 0) > 86400:
        return False
    try:
        user = json.loads(d.get("user", "{}"))
    except ValueError:
        return False
    return (user.get("username") or "").lower() in ADMINS


async def index(_):
    return web.FileResponse(DIST / "index.html")


async def items(request):
    return web.json_response({"items": load(), "is_admin": is_admin(request)})


async def add(request):
    if not is_admin(request):
        raise web.HTTPForbidden()
    f = await request.post()
    name = str(f.get("name", "")).strip()[:100]
    use = str(f.get("use", "")).strip()[:500]
    price = str(f.get("price", "")).strip()[:60]
    img = f.get("image")
    if not name or img is None or not hasattr(img, "file"):
        raise web.HTTPBadRequest(text="Nom va rasm kerak")
    ext = Path(img.filename or "").suffix.lower()
    if ext not in ALLOWED:
        raise web.HTTPBadRequest(text="Rasm turi qo'llab-quvvatlanmaydi")
    fname = uuid.uuid4().hex + ext
    (UPLOADS / fname).write_bytes(img.file.read())
    data = load()
    data.insert(0, {"id": uuid.uuid4().hex, "name": name, "use": use, "price": price, "image": fname})
    save(data)
    return web.json_response({"ok": True})


async def delete(request):
    if not is_admin(request):
        raise web.HTTPForbidden()
    iid = request.match_info["id"]
    data = load()
    for it in data:
        if it["id"] == iid:
            (UPLOADS / it["image"]).unlink(missing_ok=True)
    save([it for it in data if it["id"] != iid])
    return web.json_response({"ok": True})


async def upload(request):
    p = UPLOADS / Path(request.match_info["name"]).name
    if not p.is_file():
        raise web.HTTPNotFound()
    return web.FileResponse(p, headers={
        "Content-Type": ALLOWED.get(p.suffix.lower(), "application/octet-stream"),
        "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
        "X-Content-Type-Options": "nosniff",
    })


async def start_web(token: str):
    UPLOADS.mkdir(parents=True, exist_ok=True)
    app = web.Application(client_max_size=6 * 1024 * 1024)
    app["token"] = token
    app.add_routes([
        web.get("/", index),
        web.get("/api/items", items),
        web.post("/api/items", add),
        web.delete("/api/items/{id}", delete),
        web.get("/uploads/{name}", upload),
        web.static("/", DIST),
    ])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "8080"))
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"Mini app serveri ishga tushdi: http://localhost:{port}")