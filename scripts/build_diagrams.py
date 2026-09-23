"""Build the portfolio's standalone SVG diagrams (Python standard library only).

The drawing vocabulary deliberately follows diagrams.net: square nodes, orthogonal
connectors and restrained semantic colors. Exported PNGs are the site's images.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'diagrams'
OUT.mkdir(parents=True, exist_ok=True)
COLORS = {
    'plain': ('#ffffff', '#91979f'),
    'blue': ('#dae8fc', '#6c8ebf'),
    'green': ('#d5e8d4', '#82b366'),
    'red': ('#f8cecc', '#b85450'),
    'yellow': ('#fff2cc', '#d6b656'),
}


class Diagram:
    def __init__(self, name, height, title, description):
        self.name, self.height = name, height
        self.items = [f'<title>{escape(title)}</title><desc>{escape(description)}</desc>',
                      '<rect width="1000" height="%s" fill="white"/>' % height,
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#58616b"/></marker></defs>']

    def text(self, x, y, value, size=16, weight=400, anchor='start', color='#26313b'):
        self.items.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')

    def box(self, x, y, w, h, label, sub='', color='plain'):
        fill, stroke = COLORS[color]
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.text(x+w/2, y+h/2-3 if sub else y+h/2+6, label, 16, 500, 'middle')
        if sub:
            self.text(x+w/2, y+h/2+19, sub, 13, 400, 'middle', '#46515c')

    def group(self, x, y, w, h, label):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fafbfc" stroke="#aeb4ba" stroke-width="1.2" stroke-dasharray="6 4"/>')
        self.text(x+16, y+27, label, 14, 600)

    def arrow(self, path, dashed=False, head=True):
        dash = ' stroke-dasharray="5 4"' if dashed else ''
        marker = ' marker-end="url(#arrow)"' if head else ''
        self.items.append(f'<path d="{path}" fill="none" stroke="#58616b" stroke-width="1.5"{dash}{marker}/>')

    def rule(self, y):
        self.items.append(f'<path d="M32 {y}H968" stroke="#e0e3e6"/>')

    def save(self):
        content = '\n'.join(self.items)
        (OUT / f'{self.name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{self.height}" viewBox="0 0 1000 {self.height}" role="img" font-family="Arial, Apple SD Gothic Neo, Malgun Gothic, sans-serif">\n{content}\n</svg>\n')


d = Diagram('poudy-infrastructure', 650, 'Poudy 배포와 데이터 복구 경로', '웹과 Android 앱 요청을 Nginx가 Next.js와 Spring Boot로 전달한다. CodeDeploy가 두 EC2를 배포하고 S3 데이터는 검증 후 반영하며 실패 시 롤백한다.')
d.text(32, 32, '01  요청 흐름', 14, 600)
d.group(240, 52, 266, 275, '프론트 EC2')
d.group(652, 52, 316, 275, '백엔드 EC2')
d.box(32, 106, 156, 58, '웹 브라우저')
d.box(32, 207, 156, 64, 'Android 앱', 'WebView')
d.arrow('M188 135H215V139H262')
d.arrow('M188 239H215V139H262')
d.box(262, 106, 222, 66, 'Nginx :443', 'HTTPS 진입점', 'blue')
d.arrow('M373 172V235')
d.box(262, 235, 222, 66, 'Next.js standalone', ':3000 / systemd')
d.arrow('M484 139H674')
d.text(579, 122, '/api/*', 14, 400, 'middle')
d.text(579, 163, '사설 IP', 13, 400, 'middle', '#58616b')
d.box(674, 106, 272, 66, 'Spring Boot :8080', 'systemd 자동 재시작', 'blue')
d.box(674, 235, 272, 66, '런타임 JSON', '/opt/poudy/data')
d.arrow('M810 235V172')
d.rule(361)
d.text(32, 394, '02  애플리케이션 배포', 14, 600)
d.box(32, 416, 155, 66, 'CodeBuild', '빌드 번들')
d.arrow('M187 449H227')
d.box(227, 416, 215, 66, 'CodeDeploy', '배포 훅 / health 검증', 'green')
d.arrow('M335 416V327', True)
d.arrow('M442 449H570V311H652', True)
d.text(32, 516, '기동 후 health를 확인하고 릴리즈', 14)
d.text(652, 394, '03  데이터 동기화', 14, 600)
d.box(652, 416, 110, 66, 'S3', '원본 JSON')
d.arrow('M762 449H801')
d.box(801, 416, 167, 66, 'data-sync timer', '약 5분 주기', 'yellow')
d.arrow('M884 416V301')
d.text(652, 516, '구조 검증 → 데이터 교체 → 재시작', 14)
d.text(652, 541, 'health 실패 시 이전 데이터로 복구', 14, 600)
d.rule(572)
d.text(32, 610, '운영 관측', 14, 600)
d.text(156, 610, 'journald  /  CloudWatch Agent  /  Grafana HTTPS 체크', 14)
d.save()

d = Diagram('ingredient-review', 654, '역할을 분리한 성분 데이터 검수', '근거 수집과 판정 후 태그와 설명을 각각 생성하고 독립 검증한다. 규칙 기반 게이트에서 자동 반영 후보, 사람 검토, 보류로 나눈다.')
d.text(32, 32, '01  근거 확보', 14, 600)
d.box(32, 54, 232, 70, '식약처 원료성분', '22,013건 스냅샷')
d.arrow('M264 89H338')
d.box(338, 54, 254, 70, '근거 수집', '출처와 적용 경로 확인', 'blue')
d.arrow('M592 89H670')
d.box(670, 54, 298, 70, '근거 판정', '피부 적용 근거 우선', 'blue')
d.group(32, 184, 936, 252, '')
d.text(244, 211, '02  생성과 독립 검증', 14, 600)
d.arrow('M819 124V155H155V259H244')
d.arrow('M155 259V363H244')
d.box(244, 227, 242, 64, '태그 제안', '카탈로그 코드만 사용', 'blue')
d.arrow('M486 259H563')
d.box(563, 227, 262, 64, '태그 검증', '별도 역할에서 독립 판정', 'green')
d.box(244, 331, 242, 64, '설명 작성', '승인된 근거만 사용', 'blue')
d.arrow('M486 363H563')
d.box(563, 331, 262, 64, '설명 검증', '주장별 근거 대조', 'green')
d.arrow('M825 259H895V477H590')
d.arrow('M825 363H895', head=False)
d.box(338, 449, 252, 62, '규칙 기반 게이트', '코드 / 근거 / 위험도', 'yellow')
d.arrow('M464 511V542H175V565')
d.arrow('M464 542H500V565')
d.arrow('M500 542H826V565')
d.box(32, 565, 286, 64, '자동 반영 후보', '태그 추가만', 'green')
d.box(357, 565, 286, 64, '사람 검토 큐', '삭제 / 충돌 / 낮은 확신', 'yellow')
d.box(682, 565, 286, 64, '보류 기록', '근거 부족 / 오류', 'red')
d.text(32, 469, '역할별 CLI 호출', 14, 600)
d.text(32, 491, 'Codex / Claude Code', 13)
d.text(32, 513, 'JSON Schema 응답 계약', 13)
d.save()

d = Diagram('concurrent-likes', 640, '동시 요청의 경합과 멱등 처리', '변경 전에는 동시에 좋아요를 추가해 unique 제약 위반이 발생한다. 변경 후에는 User 행 잠금으로 요청을 직렬화하고 멱등 PUT 요청으로 재시도 시 상태를 유지한다.')
d.text(32, 36, '변경 전', 18, 600)
d.text(534, 36, '변경 후', 18, 600)
d.items.append('<path d="M500 24V612" stroke="#e0e3e6"/>')
for x in (32, 264):
    d.box(x, 68, 204, 64, 'POST /toggle', '동시 요청 A' if x == 32 else '동시 요청 B')
    d.arrow(f'M{x+102} 132V184')
    d.box(x, 184, 204, 64, '좋아요 조회', '두 요청 모두 없음')
    d.arrow(f'M{x+102} 248V281H250V311')
d.box(32, 311, 436, 64, '두 요청 모두 INSERT', '같은 사용자와 게시글 조합', 'red')
d.arrow('M250 375V427')
d.box(32, 427, 436, 64, 'Unique 제약 위반 → 500', '동시 요청으로 경합 발생', 'red')
d.text(32, 547, '재시도에도 같은 문제가 남음', 14, 600)
d.text(32, 575, '토글 요청이 한 번 더 실행되면', 14)
d.text(32, 598, '처음 추가한 좋아요가 다시 삭제됨', 14)
for x in (534, 766):
    d.box(x, 68, 202, 64, 'PUT /like', 'liked: true')
    d.arrow(f'M{x+101} 132V161H750V184')
d.box(534, 184, 434, 64, 'User 행 비관적 락', 'SELECT … FOR UPDATE', 'blue')
d.arrow('M635 248V311')
d.arrow('M867 248V311')
d.box(534, 311, 202, 64, 'A: 먼저 실행', '없음 → INSERT')
d.box(766, 311, 202, 64, 'B: 대기 후 실행', '이미 있음 → no-op')
d.arrow('M635 375V401H750V427')
d.arrow('M867 375V401H750', head=False)
d.box(534, 427, 434, 64, 'likeCount = 1', '같은 요청을 반복해도 같은 상태', 'green')
d.text(534, 547, '동시성과 재시도를 함께 처리', 14, 600)
d.text(534, 575, '행 잠금으로 같은 사용자의 요청을 직렬화', 14)
d.text(534, 598, '멱등 API로 재시도해도 결과 유지', 14)
d.save()

d = Diagram('database-consistency', 588, '테스트와 배포 데이터베이스의 차이', 'H2에서 통과한 null 검색 파라미터가 PostgreSQL에서는 bytea로 추론되었다. 빈 문자열로 정규화하고 방언에 민감한 테스트를 실제 PostgreSQL로 옮겼다.')
d.text(32, 36, '변경 전', 18, 600)
d.box(32, 88, 220, 76, 'GalleryService', 'search = null')
d.arrow('M252 126H308')
d.box(308, 88, 312, 76, 'JPQL 검색 조건', ':search is null or lower(…)')
d.arrow('M620 108H669V90H710')
d.arrow('M620 144H669V190H710')
d.box(710, 57, 258, 66, '로컬 / CI: H2', '테스트 통과', 'green')
d.box(710, 157, 258, 66, '배포: PostgreSQL', '500 오류', 'red')
d.text(308, 217, 'null 파라미터를 bytea로 추론', 14)
d.text(308, 244, 'ERROR: function lower(bytea) does not exist', 14, 500, color='#97423e')
d.rule(286)
d.text(32, 327, '변경 후', 18, 600)
d.box(32, 380, 220, 76, 'normalizeSearch()', 'null → 빈 문자열', 'blue')
d.arrow('M252 418H308')
d.box(308, 380, 312, 76, 'JPQL 고정 타입 비교', ":search = '' or lower(…)", 'blue')
d.arrow('M620 400H669V378H710')
d.arrow('M620 435H669V485H710')
d.box(710, 345, 258, 66, '배포: PostgreSQL', '정상 조회', 'green')
d.box(710, 448, 258, 76, 'Testcontainers', 'PostgreSQL 통합 테스트', 'green')
d.text(32, 557, '방언에 민감한 테스트는 실제 DB로 옮기고, 나머지는 H2를 유지', 14)
d.save()

d = Diagram('rag-pipeline', 548, '뉴스 검색과 근거 기반 응답 흐름', '뉴스를 전처리하고 임베딩하여 ChromaDB에 저장한다. 사용자 질문으로 관련 기사를 검색한 뒤 프롬프트와 Solar LLM을 거쳐 답변하고 정확도, 관련성, 환각률을 평가한다.')
d.text(32, 36, '01  색인 준비', 14, 600)
for x, label, sub, color in [(32, 'IT 뉴스 수집', '3,385건', 'plain'), (282, '전처리', '본문 정리', 'plain'), (532, 'Upstage 임베딩', '벡터 변환', 'blue'), (782, 'ChromaDB', '벡터 저장소', 'blue')]:
    d.box(x, 67, 186, 70, label, sub, color)
for x in (218, 468, 718):
    d.arrow(f'M{x} 102H{x+64}')
d.rule(192)
d.text(32, 230, '02  질문과 검색', 14, 600)
d.box(32, 269, 186, 70, '사용자 질문')
d.arrow('M218 304H282')
d.box(282, 269, 186, 70, '관련 기사 검색', '근거 문서 확보', 'blue')
d.arrow('M875 137V246H375V269')
d.text(632, 232, '벡터 유사도 검색', 13, 400, 'middle')
d.arrow('M468 304H532')
d.box(532, 269, 186, 70, '프롬프트 구성', '질문 + 검색 근거')
d.arrow('M718 304H782')
d.box(782, 269, 186, 70, 'Solar LLM', '근거 기반 답변')
d.arrow('M875 339V429H718')
d.box(282, 396, 436, 66, '정량 평가', '정확도 / 관련성 / 환각률', 'green')
d.text(32, 513, 'RAG 적용 전후를 동일한 테스트셋으로 비교', 14)
d.save()

print(f'Generated 5 SVG diagrams in {OUT}')
