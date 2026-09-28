# 김선우 포트폴리오

GitHub Pages로 제공하는 정적 HTML 포트폴리오입니다. 별도 패키지 설치나 빌드가 필요하지 않습니다.

## 로컬 미리보기

저장소 폴더에서 다음 명령을 실행하고 `http://localhost:4173`을 엽니다.

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

## 수정할 파일

- `index.html`: 소개, 문제 해결 사례, 프로젝트, 경력 등의 내용
- `assets/styles.css`: 레이아웃, 글꼴, 반응형 화면, 인쇄 스타일
- `assets/site.js`: 목차, 현재 읽는 위치 표시, 이미지 확대 창
- `assets/diagrams/*.png`: 본문에 삽입하는 가로 2,000px 다이어그램 이미지
- `assets/diagrams/*.svg`: 별도로 열거나 편집할 수 있는 벡터 원본
- `scripts/build_diagrams.py`: 다이어그램의 노드, 글자, 연결선을 만드는 코드

## 디자인 기준

흰 바탕과 검정 글자를 기본으로 사용합니다. 과도한 카드, 그림자, 배지 대신 글자 크기와 여백, 얇은 구분선으로 정보의 순서를 표현합니다. 사례의 제목은 짧게, 요약은 별도 문단으로 두며, 본문은 그림 → 문제 원인 → 해결 과정 → 결과 순으로 읽습니다.

다이어그램은 사이트 스타일과 독립된 이미지입니다. 사각형 노드와 직각 연결선, diagrams.net 계열의 절제된 색상을 사용합니다. 모바일에서는 그림이나 ‘크게 보기’를 누르면 확대 창이 열립니다. 확대 창은 키보드로 조작할 수 있으며 Esc로 닫습니다. JavaScript가 꺼져 있어도 이미지 링크로 원본을 열 수 있습니다.

## 다이어그램 갱신

SVG 생성은 Python 표준 라이브러리만 사용합니다.

```sh
python3 scripts/build_diagrams.py
```

PNG는 SVG를 브라우저에서 2배 해상도로 렌더링한 파일입니다. `agent-browser`가 설치되어 있고 로컬 서버가 실행 중이면 다음과 같이 다시 생성할 수 있습니다.

```sh
bash scripts/export_diagrams.sh
```

한글을 지원하는 글꼴이 있는 환경에서 내보내세요. SVG를 바꾼 뒤 PNG도 갱신해야 본문에 반영됩니다.

## 콘텐츠

디자인 개편에서는 기존 사례의 문제 원인, 해결 과정, 결과를 유지했습니다. 소개, 사례 제목과 요약은 새 레이아웃에 맞춰 줄였으며 프로젝트의 중복 상세 설명은 정리했습니다. 기술적 사실과 성과 수치는 별도의 콘텐츠 수정 단계에서 검토할 수 있습니다.

## Excalidraw 다이어그램 (2026-09-28부터)

새 사례 그림은 Excalidraw 스타일로 그린다. 사례마다 알맞은 그림 형태(흐름도, 시퀀스 등)가 다르므로 그림마다 원본을 따로 만든다.

- `scripts/excalidraw/<이름>.py`: 그림 요소를 만드는 코드. 실행하면 `<이름>.json`을 출력한다
- `scripts/excalidraw/render.html`, `server.py`: Excalidraw 공식 라이브러리로 JSON을 PNG(2배)로 렌더링하고 저장한다

```sh
cd scripts/excalidraw
python3 ingredient-admin.py > ingredient-admin.json
python3 server.py "$PWD" &   # 127.0.0.1:4180
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --virtual-time-budget=60000 --dump-dom "http://127.0.0.1:4180/render.html?n=ingredient-admin"
cp ingredient-admin.png ../../assets/diagrams/
```

그림 규칙: 상자에는 이름 한 줄만, 설명은 본문에서. 흰 상자와 검정 선, 색은 상자 뒤 그림자로만(연분홍 문제, 연보라 새 흐름, 진보라 핵심 결과물, 노랑 예외, 회색 사람과 보조 저장소). 묶음은 회색 점선 테두리.

그림을 바꾼 뒤에는 `index.html`의 이미지 주소 뒤 `?v=` 값을 새 파일의 해시로 바꾼다(GitHub Pages가 이미지를 10분간 캐시하므로, 주소가 같으면 방문자가 예전 그림을 볼 수 있다).

```sh
python3 - <<'PY'
import re,hashlib
from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
s=re.sub(r'((?:src|href)=")(assets/diagrams/[\w-]+\.png)(?:\?v=\w+)?"', lambda m: f'{m.group(1)}{m.group(2)}?v={hashlib.md5(Path(m.group(2)).read_bytes()).hexdigest()[:8]}"', s)
p.write_text(s,encoding='utf-8')
PY
```
