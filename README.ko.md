[English](README.md) | [한국어](README.ko.md)

# AI 앱 아이콘 생성기

SVG 코드로 프로덕션 레디 앱 아이콘을 생성하고, **모든 주요 플랫폼**용으로 패키징합니다 — [Claude Code](https://claude.ai/code) 기반.

```
SVG 코드 → 1024x1024 PNG → Windows / macOS / Android / iOS / Web
```

## 주요 기능

- **AI 기반 디자인** — Claude Code가 SVG XML을 직접 작성, 디자인 툴 불필요
- **5개 플랫폼 패키징** — Windows ICO, macOS iconset, Android mipmap, iOS AppIcon, Web (favicon + PWA + OG)
- **투명 둥근 모서리** — RGBA + 4x 슈퍼샘플링 안티앨리어싱 엣지
- **일반 모드** — 12개 아이콘 변형 + 대화형 피드백 루프
- **하이퍼 모드** — 560개 변형 (7방향 × 4디자인 × 10색 × 2스타일)
- **HTML 프리뷰** — 모든 후보를 브라우저에서 나란히 비교

## 요구 사항

- Python 3.10+
- [Claude Code](https://claude.ai/code) CLI

## 설치

```bash
git clone https://github.com/unims77/claude-appicon-generation-skill.git
cd claude-appicon-generation-skill

pip install -r requirements.txt
playwright install chromium
```

## 빠른 시작

### Claude Code 커맨드

```bash
# 원스톱: 자료조사 → 디자인 → 패키징 (12개 변형)
/_icon-auto MyApp

# 하이퍼 모드: 560개 변형 + 5플랫폼 패키징
/_icon-auto-hyper MyApp

# 피드백 루프 포함 디자인
/_icon-generate MyApp

# 기존 1024x1024 PNG 패키징
/_icon-package path/to/icon_1024.png
```

### 출력 결과

생성된 모든 파일은 `output/{timestamp}/` 폴더에 저장됩니다:

```
output/20260325_143052/
├── candidates/          # SVG & PNG 아이콘 후보
│   ├── *.svg
│   └── *.png
├── preview.html         # 브라우저에서 열어 모든 후보 비교
└── package/             # 5플랫폼 패키징된 아이콘 (확정 후)
    ├── windows/
    ├── macos/
    ├── android/
    ├── ios/
    └── web/
```

아이콘 생성 후, 브라우저에서 **`preview.html`**을 열어 모든 후보를 나란히 비교한 뒤 원하는 아이콘을 선택하여 패키징하세요.

### Python API

```python
from src.converter import svg_to_png, svg_string_to_png, batch_convert
from src.packager import package_all
from src.validator import validate_svg, validate_package

# 단일 SVG → PNG
svg_to_png("icon.svg", "icon.png")

# SVG 문자열 → PNG
svg_string_to_png('<svg viewBox="0 0 1024 1024">...</svg>', "icon.png")

# 디렉토리 내 모든 SVG 일괄 변환
batch_convert("svg_dir/", "png_dir/")

# 5개 플랫폼 패키징
package_all("icon_1024.png", "output/")

# 검증
validate_svg("icon.svg")
validate_package("output/")
```

## 아키텍처

```
SVG XML (Claude Code가 작성)
  ↓ converter.py — Playwright Chromium 렌더링
  ↓               — 4x 슈퍼샘플링 둥근 마스크 (CORNER_RADIUS=200)
icon_1024.png (RGBA, 투명 둥근 모서리)
  ↓ resizer.py — Pillow LANCZOS 리사이즈
  ↓ packager.py — 플랫폼별 패키징
  ├── windows/app.ico          (16~256px 멀티사이즈 ICO)
  ├── macos/icon.iconset/      (16~1024px 레티나 페어)
  ├── android/mipmap-*/        (48~192px + 512px 플레이스토어)
  ├── ios/AppIcon.appiconset/  (20~1024px + Contents.json)
  └── web/                     (favicon, PWA, apple-touch, OG 이미지)
```

## 프로젝트 구조

```
AI_AppIcon/
├── src/
│   ├── config.py       # 플랫폼 사이즈, Material 색상, 상수
│   ├── converter.py    # SVG → PNG (Playwright Chromium)
│   ├── hyper.py        # 하이퍼 모드 변형 생성
│   ├── packager.py     # 5플랫폼 패키징
│   ├── preview.py      # HTML 프리뷰 생성
│   ├── resizer.py      # PNG 리사이즈
│   └── validator.py    # SVG/PNG/패키지 검증
├── .claude/
│   ├── agents/         # AI 에이전트 정의 (리서처, 디자이너, 리뷰어, 패키저)
│   └── commands/       # 파이프라인 커맨드 정의
├── CLAUDE.md           # Claude Code 프로젝트 지침
├── _SPEC.md            # 기술 스펙
└── requirements.txt
```

## 파이프라인 모드

### 일반 모드 (`/_icon-generate`)

1. **자료조사** — AI가 앱 컨셉, 트렌드, 색상, 심볼 분석
2. **사용자 선택** — 리서치 브리프에서 디자인 방향 선택
3. **디자인** — 12개 SVG 변형 (Flat×3, Gradient×3, Outlined×2, Bold×2, Emoji×2)
4. **프리뷰** — HTML 프리뷰로 나란히 비교
5. **피드백 루프** — 수정 또는 확정 → PNG 변환 + 검증

### 하이퍼 모드 (`/_icon-auto-hyper`)

1. **자료조사** — 상위 5개 테마 + 2개 이모지 방향 자동 선택
2. **디자인** — 28개 베이스 SVG (7방향 × 4변형)
3. **변형 생성** — 28 × 10색 × 2스타일 = **560개 SVG 변형**
4. **프리뷰** — 방향별 그룹, 10컬럼 색상 그리드
5. **패키징** — 모든 변형을 5개 플랫폼으로 패키징

## AI 에이전트

| 에이전트 | 역할 |
|----------|------|
| **icon-researcher** | 앱 분석, 트렌드/색상/심볼 조사, 디자인 브리프 |
| **icon-designer** | SVG 코드로 아이콘 변형 생성 |
| **icon-reviewer** | SVG 유효성, PNG 품질, 소형 렌더링 검증 |
| **icon-packager** | 5플랫폼 패키징 |

## SVG 규칙

아이콘은 올바른 렌더링을 위해 다음 규칙을 따라야 합니다:

- `viewBox="0 0 1024 1024"` — 필수
- 외부 리소스 금지 (URL, 폰트) — 모든 요소 인라인
- `<text>` 태그 금지 — 텍스트는 `<path>`로 변환
- `src/config.py`의 `MATERIAL_COLORS` (일반) 또는 `HYPER_COLORS` (하이퍼) 색상 사용

## 라이선스

MIT
