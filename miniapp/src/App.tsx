import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";
import { addItem, alertBox, confirmBox, deleteItem, getItems, tg, type Item } from "./api";

const ADMIN = "DMYA_4779";
const TYPES = /\.(png|jpe?g|gif|webp|svg|bmp|avif)$/i;
const MAX_BYTES = 5 * 1024 * 1024;

function Home() {
  return (
    <section>
      <h2>Laboratoriya haqida</h2>
      <p>"Namangan sinov va kalibrlash laboratoriyasi" MChJ — qiyoslash laboratoriyasi. O'zbekiston akkreditatsiya markazi (O'ZAK) tomonidan akkreditatsiyadan o'tgan.</p>
      <div className="info">
        <b>Akkreditatsiya</b><br />
        Reestr raqami: O'ZAK.QL.0149<br />
        Standart: O'z DSt 3444:2020<br />
        Akkreditatsiya sanasi: 14.07.2025<br />
        Amal qilish muddati: 16.07.2030
      </div>
      <h3 className="sec">Faoliyat sohasi</h3>
      <div className="info">
        <ul>
          <li>Gorizontal silindrik po'latli rezervuarlar: 0 dan 200 m³ gacha (geometrik usul), 0 dan 25 m³ gacha (hajmiy usul)</li>
          <li>Vertikal silindrik po'latli rezervuarlar: 0 dan 10 000 m³ gacha (geometrik usul)</li>
          <li>AYQSH, AGKSH va neftbazalarda ishlatiladigan rezervuarlarni sotish</li>
        </ul>
      </div>
      <h3 className="sec">Bog'lanish / Profil</h3>
      <div className="info">
        <b>Telegram:</b> @DMYA_4779<br />
        <b>Telefon:</b> +998996904779<br />
        <b>Email:</b> muhammadyusufdadamirzayev@gmail.com<br />
        <b>Telegram kanal:</b> <a href="https://t.me/Namangan_sinov_kalibrlash" target="_blank" rel="noreferrer">t.me/Namangan_sinov_kalibrlash</a><br />
        <b>Instagram:</b> <a href="https://instagram.com/namangan_skl" target="_blank" rel="noreferrer">@namangan_skl</a><br />
        <b>Manzil:</b> Namangan shahri, Nodira ko'chasi, 9-uy
      </div>
      <a className="pr" href="tel:+998996904779">📞 Qo'ng'iroq qilish (+998996904779)</a>
      <button className="pr" style={{ marginTop: "8px" }} onClick={() => tg?.openTelegramLink(`https://t.me/${ADMIN}`)}>💬 Telegram orqali yozish (@DMYA_4779)</button>
      <a className="pr" style={{ marginTop: "8px", background: "#E1306C" }} href="https://instagram.com/namangan_skl" target="_blank" rel="noreferrer">📸 Instagram sahifamiz</a>
      <a className="pr" style={{ marginTop: "8px", background: "#4b5563" }} href="mailto:muhammadyusufdadamirzayev@gmail.com">📧 Email orqali yozish</a>
      <h3 className="sec">Akkreditatsiya guvohnomasi</h3>
      <img className="cert" src="/guvohnoma.png" alt="Akkreditatsiya guvohnomasi" />
    </section>
  );
}

function ItemCard({ item, admin, onDelete }: { item: Item; admin: boolean; onDelete: (i: Item) => void }) {
  const order = () =>
    tg?.openTelegramLink(`https://t.me/${ADMIN}?text=${encodeURIComponent(`Salom! "${item.name}" haqida ma'lumot olmoqchiman.`)}`);
  return (
    <div className="card">
      <img src={`/uploads/${item.image}`} alt={item.name} loading="lazy" />
      <div className="b">
        <h3>{item.name}</h3>
        {item.use && <p>{item.use}</p>}
        <div className="price">{item.price || "Narxi so'raladi"}</div>
        <button className="pr" onClick={order}>Buyurtma berish</button>
        {admin && <button className="del" onClick={() => onDelete(item)}>O'chirish</button>}
      </div>
    </div>
  );
}

function AddForm({ onAdded }: { onAdded: () => void }) {
  const [name, setName] = useState("");
  const [use, setUse] = useState("");
  const [price, setPrice] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [key, setKey] = useState(0);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const preview = useMemo(() => (file ? URL.createObjectURL(file) : ""), [file]);
  useEffect(() => () => { if (preview) URL.revokeObjectURL(preview); }, [preview]);

  const pick = (f: File | null) => {
    setErr("");
    if (f && !TYPES.test(f.name)) return setErr("Bu rasm turi qo'llab-quvvatlanmaydi");
    if (f && f.size > MAX_BYTES) return setErr("Rasm hajmi 5 MB dan oshmasin");
    setFile(f);
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) return setErr("Rasm tanlang");
    setBusy(true);
    setErr("");
    try {
      const fd = new FormData();
      fd.append("name", name); fd.append("use", use); fd.append("price", price); fd.append("image", file);
      await addItem(fd);
      setName(""); setUse(""); setPrice(""); setFile(null); setKey((k) => k + 1);
      onAdded();
    } catch (x) {
      setErr((x as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit}>
      <b>Uskuna qo'shish (admin)</b>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Uskuna nomi" required />
      <textarea value={use} onChange={(e) => setUse(e.target.value)} rows={3} placeholder="Nima uchun ishlatiladi?" />
      <input value={price} onChange={(e) => setPrice(e.target.value)} placeholder="Narxi (masalan: 1 500 000 so'm)" />
      <input key={key} type="file" accept="image/*,.svg" onChange={(e) => pick(e.target.files?.[0] ?? null)} />
      {preview && <img className="prev" src={preview} alt="Ko'rinish" />}
      {err && <div className="err">{err}</div>}
      <button className="pr" type="submit" disabled={busy}>{busy ? "Yuklanmoqda..." : "Qo'shish"}</button>
    </form>
  );
}

export default function App() {
  const [tab, setTab] = useState<"home" | "shop">("home");
  const [items, setItems] = useState<Item[]>([]);
  const [admin, setAdmin] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [q, setQ] = useState("");

  const load = useCallback(async () => {
    try {
      const d = await getItems();
      setItems(d.items); setAdmin(d.is_admin); setError("");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { tg?.ready(); tg?.expand(); load(); }, [load]);

  const shown = useMemo(() => {
    const s = q.trim().toLowerCase();
    return s ? items.filter((i) => `${i.name} ${i.use}`.toLowerCase().includes(s)) : items;
  }, [items, q]);

  const remove = (it: Item) =>
    confirmBox(`"${it.name}" o'chirilsinmi?`, async (ok) => {
      if (!ok) return;
      try { await deleteItem(it.id); load(); } catch (e) { alertBox((e as Error).message); }
    });

  return (
    <>
      <header>
        <img src="/logo.png" alt="" />
        <h1>Namangan sinov va kalibrlash laboratoriyasi</h1>
      </header>
      <nav>
        <button className={tab === "home" ? "on" : ""} onClick={() => setTab("home")}>Asosiy</button>
        <button className={tab === "shop" ? "on" : ""} onClick={() => setTab("shop")}>Uskunalar</button>
      </nav>
      <main>
        {tab === "home" ? <Home /> : (
          <section>
            {admin && <AddForm onAdded={load} />}
            <input className="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Uskuna qidirish..." />
            {loading && <div className="empty">Yuklanmoqda...</div>}
            {error && <div className="empty">{error} <button className="pr" onClick={load}>Qayta urinish</button></div>}
            {!loading && !error && shown.length === 0 && <div className="empty">{q ? "Hech narsa topilmadi" : "Hozircha uskunalar yo'q"}</div>}
            <div className="grid">
              {shown.map((it) => <ItemCard key={it.id} item={it} admin={admin} onDelete={remove} />)}
            </div>
          </section>
        )}
      </main>
    </>
  );
}
