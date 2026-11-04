export interface Item { id: string; name: string; use: string; price: string; image: string }
export interface ItemsResponse { items: Item[]; is_admin: boolean }

interface TgWebApp {
  initData: string;
  ready(): void;
  expand(): void;
  openTelegramLink(url: string): void;
  showConfirm(msg: string, cb: (ok: boolean) => void): void;
  showAlert(msg: string): void;
}
declare global { interface Window { Telegram?: { WebApp: TgWebApp } } }

export const tg = window.Telegram?.WebApp;
const headers = (): HeadersInit => ({ "X-Init-Data": tg?.initData ?? "" });

export const confirmBox = (msg: string, cb: (ok: boolean) => void) =>
  tg ? tg.showConfirm(msg, cb) : cb(window.confirm(msg));
export const alertBox = (msg: string) => (tg ? tg.showAlert(msg) : window.alert(msg));

export async function getItems(): Promise<ItemsResponse> {
  const r = await fetch("/api/items", { headers: headers() });
  if (!r.ok) throw new Error("Ma'lumotni yuklab bo'lmadi");
  return r.json();
}
export async function addItem(f: FormData): Promise<void> {
  const r = await fetch("/api/items", { method: "POST", headers: headers(), body: f });
  if (!r.ok) throw new Error((await r.text()) || "Xatolik");
}
export async function deleteItem(id: string): Promise<void> {
  const r = await fetch(`/api/items/${id}`, { method: "DELETE", headers: headers() });
  if (!r.ok) throw new Error("O'chirib bo'lmadi");
}
