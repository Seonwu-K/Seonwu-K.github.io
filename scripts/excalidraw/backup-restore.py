"""사례 05: 장애 시나리오 기반 복구 흐름.
① 기존 백업 → ② 백업 재설계 → ③ EC2 소실 가정 복구 리허설 → ④ 측정 결과
"""
from exlib import *

c = Canvas()
TOP, H = 20, 510


def col(i, x, w, title, uc):
    c.frame(i, x, TOP, w, H)
    c.text(i + 't', x + 18, TOP + 16, title, 19)
    c.uline(i + 'u', x + 18, TOP + 46, twidth(title, 19) - 4, uc)


# ① before
col('c1', 20, 250, '① 기존 백업', PINK)
c.box('b1', 45, 100, 200, 64, 'EC2 Docker\nPostgres', None, fs=17)
c.arrow('ba1', 145, 164, [[0, 0], [0, 70]])
c.text('ba1t', 157, 178, '하루 1회\npg_dump', 15)
c.box('b2', 45, 234, 200, 56, 'S3', None, fs=17)
c.box('b3', 45, 340, 200, 90, '최대 24시간\n데이터 손실\n복원 여부 미검증', PINK, PINKF, fs=16)

# ② redesigned backup
col('c2', 300, 260, '② 백업 재설계', LAV2)
c.box('d1', 330, 100, 200, 64, 'EC2 Docker\nPostgres', None, fs=17)
c.arrow('da1', 430, 164, [[0, 0], [0, 40]])
c.box('d2', 330, 204, 200, 110, 'pgBackRest\n전체 주 1회\n증분 매일\nWAL 5분 이내', LAV, fs=16)
c.arrow('da2', 430, 314, [[0, 0], [0, 40]])
c.box('d3', 330, 354, 200, 64, 'S3\n(영구 삭제 불가)', None, fs=16)

# ③ disaster rehearsal
col('c3', 590, 270, '③ EC2 소실 가정 리허설', LAV2)
c.box('e0', 615, 92, 220, 44, '기존 EC2 없음', PINK, PINKF, fs=16)
steps = [('새 EC2 기동', '17초'), ('부트스트랩', '60초'), ('설정, 이미지', '18초'), ('DB 복원', '18초'), ('백엔드 배포', '29초')]
y = 156
for n, (name, sec) in enumerate(steps):
    sh, fill = (LAV2, LAVF) if name == 'DB 복원' else (LAV, '#ffffff')
    c.box(f'e{n + 1}', 615, y, 220, 42, f'{name}  {sec}', sh, fill, fs=15)
    c.arrow(f'ea{n}', 725, y - 20, [[0, 0], [0, 20]])
    y += 62
c.arrow('eah', 725, y - 20, [[0, 0], [0, 20]])
c.box('e9', 615, y, 220, 42, 'health 확인', None, fs=15)

# ④ results
col('c4', 890, 250, '④ 측정 결과', LAV2)
c.box('r1', 912, 100, 206, 96, '데이터 손실 한도\n24시간 → 5분\n(실측 132초)', LAV2, LAVF, fs=16)
c.box('r2', 912, 226, 206, 64, 'DB 복원\n약 10초', LAV2, LAVF, fs=16)
c.box('r3', 912, 320, 206, 64, '전체 복구\n약 2분 20초', LAV2, LAVF, fs=16)

for i, x1, x2 in (('g1', 270, 300), ('g2', 560, 590), ('g3', 860, 890)):
    c.arrow(i, x1, TOP + H / 2, [[0, 0], [x2 - x1, 0]])

c.text('note', 30, TOP + H + 18,
       '첫 리허설 실제 소요 7분 13초: 저장소 인증 실패, 복원본 WAL의 운영 백업 오염을 발견해 복구 절차서에 반영 (막힌 시간을 뺀 순수 실행 2분 20초)',
       15, MUTED)
print(c.dump())
