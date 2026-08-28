from __future__ import annotations

CATEGORIES = [
    {
        "code": "mobility",
        "name": "이동·생활보조",
        "short": "이동보조",
        "subs": ["보행기", "휠체어", "전동침대", "목욕보조", "식사보조"],
        "tone": "#1864ab",
        "blurb": "보행기·휠체어·침대",
    },
    {
        "code": "home",
        "name": "주거환경개선",
        "short": "주거안전",
        "subs": ["안전손잡이", "미끄럼방지", "경사로", "낙상예방", "욕실", "조명"],
        "tone": "#0b7285",
        "blurb": "손잡이·경사로·낙상",
    },
    {
        "code": "health",
        "name": "건강·간병",
        "short": "건강간병",
        "subs": ["기저귀", "욕창", "건강기기", "간병", "동행"],
        "tone": "#2b8a3e",
        "blurb": "간병용품·방문요양",
    },
    {
        "code": "life",
        "name": "생활관리",
        "short": "생활관리",
        "subs": ["청소", "방제", "유지보수"],
        "tone": "#5c4b7a",
        "blurb": "청소·방제·점검",
    },
    {
        "code": "emergency",
        "name": "긴급안전",
        "short": "긴급안전",
        "subs": ["단말기", "센서", "구독"],
        "tone": "#c92a2a",
        "blurb": "안심버튼·긴급알림",
    },
]

NAV_ITEMS = [
    ("/", "홈"),
    ("/catalog", "상품비교"),
    ("/support", "정부지원"),
    ("/consult", "돌봄상담"),
    ("/compare", "비교함"),
    ("/login", "로그인"),
]


def category_by_code(code: str) -> dict | None:
    for item in CATEGORIES:
        if item["code"] == code:
            return item
    return None
