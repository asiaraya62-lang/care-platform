CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
  background: #f3f5f7 !important;
  color: #212529;
  font-family: "Noto Sans KR", "Malgun Gothic", sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], header[data-testid="stHeader"] {
  display: none !important;
}
[data-testid="stSidebar"] { display: none !important; }
.block-container, .stMainBlockContainer, [data-testid="stMainBlockContainer"] {
  padding: 0 !important;
  max-width: 100% !important;
}
.stApp > footer, footer { display: none !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }

:root {
  --blue: #1864ab;
  --blue-2: #1c7ed6;
  --price: #c92a2a;
  --green: #087f5b;
  --ad: #e8590c;
  --line: #dee2e6;
  --muted: #868e96;
  --text: #212529;
  --bg: #f3f5f7;
  --width: 1240px;
}

a { color: inherit; }
.wrap { width: min(var(--width), calc(100% - 24px)); margin: 0 auto; }

.topbar {
  background: #fff;
  border-bottom: 1px solid var(--line);
  font-size: 12px;
  color: #495057;
}
.topbar-inner, .header-inner, .nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  width: min(var(--width), calc(100% - 24px)); margin: 0 auto;
}
.topbar-inner { height: 34px; gap: 16px; }
.topbar a { color: #495057; text-decoration: none; margin-left: 12px; }
.topbar a:hover { color: var(--blue); }

.header { background: #fff; }
.header-inner { height: 92px; gap: 24px; }
.logo {
  display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--blue);
  min-width: 190px;
}
.logo-mark {
  width: 42px; height: 42px; border-radius: 8px; background: var(--blue); color: #fff;
  display: grid; place-items: center; font-weight: 700; font-size: 15px;
}
.logo-text { display: flex; flex-direction: column; line-height: 1.15; }
.logo-text b { font-size: 22px; letter-spacing: -0.04em; }
.logo-text span { font-size: 11px; color: #868e96; font-weight: 400; }

.search-form { flex: 1; display: flex; max-width: 640px; }
.search-form input {
  flex: 1; height: 48px; border: 2px solid var(--blue); border-right: 0;
  border-radius: 4px 0 0 4px; padding: 0 16px; font-size: 16px; outline: none;
  font-family: inherit;
}
.search-form button {
  width: 88px; height: 48px; border: 0; background: var(--blue); color: #fff;
  font-size: 16px; font-weight: 700; border-radius: 0 4px 4px 0; cursor: pointer;
  font-family: inherit;
}
.header-utils { display: flex; gap: 18px; align-items: center; font-size: 13px; }
.header-utils a { text-decoration: none; color: #343a40; }
.header-utils a:hover { color: var(--blue); }
.util-strong { font-weight: 700; color: var(--blue) !important; }

.nav {
  background: #fff; border-top: 1px solid var(--line); border-bottom: 2px solid var(--blue);
}
.nav-inner { height: 46px; }
.nav-left { display: flex; align-items: center; gap: 4px; }
.cat-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--blue); color: #fff !important; text-decoration: none;
  height: 46px; padding: 0 16px; font-weight: 700; font-size: 14px; margin-left: -12px;
}
.nav-links { display: flex; gap: 8px; margin-left: 8px; }
.nav-links a {
  text-decoration: none; color: #212529; font-size: 14px; font-weight: 600;
  padding: 8px 10px; border-radius: 4px;
}
.nav-links a:hover, .nav-links a.active { color: var(--blue); }
.nav-right { font-size: 13px; color: var(--green); font-weight: 600; }

.hero {
  display: grid; grid-template-columns: 220px 1fr 260px; gap: 12px;
  width: min(var(--width), calc(100% - 24px)); margin: 12px auto 0;
}
.panel { background: #fff; border: 1px solid var(--line); border-radius: 4px; }
.cat-panel { padding: 8px 0; }
.cat-item {
  display: flex; align-items: center; gap: 10px; padding: 9px 14px;
  text-decoration: none; color: #212529; font-size: 14px;
}
.cat-item:hover { background: #e7f5ff; color: var(--blue); }
.cat-dot {
  width: 28px; height: 28px; border-radius: 50%; color: #fff; font-size: 11px;
  display: grid; place-items: center; font-weight: 700; flex-shrink: 0;
}
.cat-item small { display: block; color: #868e96; font-size: 11px; font-weight: 400; }

.banners { display: grid; grid-template-columns: 1.5fr 1fr; grid-template-rows: 168px 110px; gap: 8px; }
.banner {
  border-radius: 4px; padding: 22px 24px; color: #fff; text-decoration: none;
  display: flex; flex-direction: column; justify-content: flex-end; overflow: hidden;
}
.banner b { font-size: 22px; letter-spacing: -0.04em; line-height: 1.25; }
.banner span { font-size: 13px; opacity: 0.92; margin-top: 8px; }
.b1 { background: #1864ab; grid-row: 1 / 2; }
.b2 { background: #0b7285; }
.b3 { background: #2b8a3e; grid-column: 1 / 2; }
.b4 { background: #c92a2a; }

.side-box { padding: 16px; }
.side-box h3 { margin: 0 0 8px; font-size: 15px; }
.side-box p { margin: 0; font-size: 13px; color: #495057; line-height: 1.5; }
.login-actions { display: flex; gap: 8px; margin-top: 12px; }
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  height: 36px; padding: 0 12px; border-radius: 4px; text-decoration: none;
  font-size: 13px; font-weight: 700;
}
.btn-blue { background: var(--blue); color: #fff !important; flex: 1; }
.btn-line { border: 1px solid var(--line); color: #212529; flex: 1; background: #fff; }
.quick-list { list-style: none; margin: 12px 0 0; padding: 0; }
.quick-list li { border-top: 1px solid #f1f3f5; }
.quick-list a {
  display: block; padding: 10px 0; font-size: 13px; text-decoration: none; color: #343a40;
}
.quick-list a:hover { color: var(--blue); }

.section {
  width: min(var(--width), calc(100% - 24px)); margin: 18px auto 0; background: #fff;
  border: 1px solid var(--line); border-radius: 4px; padding: 16px 18px 20px;
}
.section-head {
  display: flex; align-items: baseline; justify-content: space-between;
  margin-bottom: 14px; gap: 12px;
}
.section-head h2 { margin: 0; font-size: 18px; letter-spacing: -0.03em; }
.section-head a { font-size: 13px; color: #495057; text-decoration: none; }
.section-head a:hover { color: var(--blue); }
.sub-links { display: flex; flex-wrap: wrap; gap: 8px; }
.sub-links a {
  font-size: 12px; color: #495057; text-decoration: none; padding: 4px 8px;
  background: #f8f9fa; border-radius: 3px;
}
.sub-links a:hover { color: var(--blue); background: #e7f5ff; }

.grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
.grid-6 { grid-template-columns: repeat(6, 1fr); }

.card {
  border: 1px solid #f1f3f5; border-radius: 4px; text-decoration: none; color: inherit;
  display: flex; flex-direction: column; min-height: 100%;
}
.card:hover { border-color: var(--blue); }
.thumb {
  height: 132px; display: grid; place-items: center; color: #fff; font-weight: 700;
  font-size: 14px; letter-spacing: -0.03em; position: relative;
}
.badges { position: absolute; left: 8px; top: 8px; display: flex; gap: 4px; flex-wrap: wrap; }
.badge {
  font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 2px; color: #fff;
}
.badge.ad { background: var(--ad); }
.badge.gov { background: var(--green); }
.badge.pop { background: var(--blue); }
.badge.sub { background: #5c4b7a; }
.card-body { padding: 10px 10px 12px; }
.card-name {
  font-size: 13px; line-height: 1.4; height: 36px; overflow: hidden;
  font-weight: 500;
}
.card-brand { font-size: 11px; color: var(--muted); margin-bottom: 4px; }
.card-price { margin-top: 8px; color: var(--price); font-size: 16px; font-weight: 700; }
.card-meta { margin-top: 4px; font-size: 11px; color: #868e96; }
.card-actions { display: flex; gap: 6px; margin-top: 8px; }
.card-actions a {
  flex: 1; text-align: center; font-size: 12px; padding: 6px 0; border: 1px solid var(--line);
  border-radius: 3px; text-decoration: none; color: #343a40;
}
.card-actions a:hover { border-color: var(--blue); color: var(--blue); }

.program-list { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.program {
  border: 1px solid #f1f3f5; padding: 12px; text-decoration: none; color: inherit; display: block;
}
.program:hover { border-color: var(--blue); }
.program b { font-size: 14px; }
.program p { margin: 6px 0 0; font-size: 12px; color: #495057; line-height: 1.45; }
.program .src { margin-top: 8px; font-size: 11px; color: var(--muted); }

.page-title {
  width: min(var(--width), calc(100% - 24px)); margin: 16px auto 0; font-size: 22px;
}
.filter-bar {
  width: min(var(--width), calc(100% - 24px)); margin: 10px auto 0; background: #fff;
  border: 1px solid var(--line); padding: 12px 16px; display: flex; gap: 16px;
  align-items: center; flex-wrap: wrap; font-size: 13px;
}
.filter-bar a { color: #495057; text-decoration: none; }
.filter-bar a.on { color: var(--blue); font-weight: 700; }

.product-hero {
  width: min(var(--width), calc(100% - 24px)); margin: 16px auto; background: #fff;
  border: 1px solid var(--line); display: grid; grid-template-columns: 360px 1fr; gap: 28px;
  padding: 24px;
}
.product-hero .big {
  height: 280px; display: grid; place-items: center; color: #fff; font-size: 22px; font-weight: 700;
}
.notice {
  background: #fff9db; border: 1px solid #ffe066; padding: 10px 12px; font-size: 13px;
  margin-top: 14px; line-height: 1.45;
}
.spec { margin-top: 12px; font-size: 14px; line-height: 1.7; color: #343a40; }
.compare-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.compare-table th, .compare-table td {
  border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top;
}
.compare-table th { background: #f8f9fa; }

.tray {
  position: sticky; bottom: 0; background: #212529; color: #fff;
  padding: 10px 0; margin-top: 28px;
}
.tray-inner {
  width: min(var(--width), calc(100% - 24px)); margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}
.tray a { color: #fff; }
.tray-items { display: flex; gap: 8px; flex-wrap: wrap; font-size: 13px; }
.tray-items span {
  background: #495057; padding: 4px 8px; border-radius: 3px;
}

.footer {
  background: #fff; border-top: 1px solid var(--line); margin-top: 0; padding: 28px 0 40px;
  font-size: 12px; color: #868e96; line-height: 1.7;
}
.footer-inner { width: min(var(--width), calc(100% - 24px)); margin: 0 auto; }
.footer b { color: #495057; }

[data-testid="stForm"] {
  background: #fff;
  border: 2px solid #1864ab !important;
  border-radius: 4px;
  padding: 4px 8px !important;
}
[data-testid="stForm"] [data-testid="stTextInput"] input {
  font-size: 16px !important;
}
[data-testid="stFormSubmitButton"] button {
  background: #1864ab !important;
  color: #fff !important;
  border: 0 !important;
  height: 42px !important;
  font-weight: 700 !important;
}
.login-card {
  width: min(420px, calc(100% - 24px)); margin: 40px auto; background: #fff;
  border: 1px solid var(--line); padding: 28px 28px 12px;
}
.login-card h2 { margin: 0 0 8px; }
.hint { font-size: 13px; color: #495057; background: #f8f9fa; padding: 12px; margin: 8px 0 16px; }

.empty { padding: 40px; text-align: center; color: #868e96; }

@media (max-width: 1100px) {
  .hero { grid-template-columns: 1fr; }
  .banners { grid-template-columns: 1fr 1fr; grid-template-rows: 140px 100px; }
  .grid, .grid-4, .grid-6 { grid-template-columns: repeat(3, 1fr); }
  .program-list, .product-hero { grid-template-columns: 1fr; }
}
@media (max-width: 720px) {
  .header-inner { height: auto; flex-wrap: wrap; padding: 12px 0; }
  .search-form { max-width: none; order: 3; width: 100%; }
  .grid, .grid-4, .grid-6 { grid-template-columns: repeat(2, 1fr); }
  .nav-links { display: none; }
}
</style>
"""
