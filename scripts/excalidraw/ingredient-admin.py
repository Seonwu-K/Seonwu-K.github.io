"""사례 01: 변경 전 파일 수동 관리, 변경 후 승인과 검증 단계를 거치는 관리자 시스템."""
from exlib import *

c = Canvas()
c.frame('fb', 20, 20, 1120, 250, '변경 전  흩어진 파일과 수동 반영', PINK)


def stack(i, x, y, w, h, label):
    """여러 버전 파일: 뒤에 두 장을 겹쳐 그린다."""
    for k, d in (('2', 16), ('1', 8)):
        c.E.append({"type": "rectangle", "id": i + 'k' + k, "x": x + d, "y": y - d, "width": w, "height": h,
                    "backgroundColor": '#ffffff', "fillStyle": "solid", "strokeColor": INK, "strokeWidth": 1,
                    "roundness": {"type": 3}})
    c.box(i, x, y, w, h, label, None, fs=16)


def hmsg(i, x1, x2, y, label, fs=14):
    """수동 작업을 강조하는 화살표 라벨: 글자 아래 연분홍 밑줄."""
    tw = twidth(label, fs)
    c.arrow(i, x1, y, [[0, 0], [x2 - x1, 0]])
    c.ctext(i + 't', (x1 + x2) / 2, y - 32, label, fs)
    c.uline(i + 'u', (x1 + x2) / 2 - tw / 2, y - 10, tw * 0.86, PINK)


stack('p1', 40, 104, 190, 56, '사람마다 각자 관리한\n엑셀 파일')
stack('p2', 40, 190, 190, 56, 'AI가 검수한\n엑셀, JSON 파일')
c.arrow('pj1', 246, 132, [[0, 0], [24, 41]], head=None)
c.arrow('pj2', 246, 218, [[0, 0], [24, -45]], head=None)
hmsg('pa1', 270, 395, 173, '사람이 수동 통합')
c.box('p3', 395, 145, 115, 56, '통합한 엑셀', PINK, fs=16)
c.msg('pa2', 510, 640, 173, '변환 스크립트', fs=14)
c.box('p4', 640, 145, 120, 56, '서버용 JSON', None, fs=16)
hmsg('pa3', 760, 890, 173, '사람이 업로드')
c.box('p5', 890, 145, 60, 56, 'S3', None, fs=17)
c.arrow('pa4', 950, 173, [[0, 0], [55, 0]])
c.box('p6', 1005, 145, 110, 56, '운영 EC2', None, fs=16)
c.text('p6n', 935, 214, 'systemd가 복사,\n시작 시 Spring이 읽음', 14, MUTED)

c.frame('fa', 20, 300, 1120, 570, '변경 후  승인과 검증 단계를 거치는 관리자 시스템', LAV2)
# main flow: left to right, then straight down on the right
c.box('q1', 40, 400, 135, 60, '관리자 화면', fs=18)
c.box('q2', 205, 400, 155, 60, '변경 요청 API', LAV, fs=18)
c.box('q3', 385, 365, 210, 130, '요청 검증\n(버전, 멱등 키)', YEL, shape='diamond', fs=16)
c.box('q4', 635, 400, 150, 60, '승인 대기', YEL)
c.box('q5', 835, 400, 170, 60, '반영 전 재검사', LAV, fs=18)
c.box('r2', 820, 535, 200, 70, '확정 데이터\n(DuckDB, 이력)', LAV2, LAVF, fs=18)
c.box('r3', 820, 655, 200, 70, '릴리스 파일\n(CSV, manifest)', LAV, fs=18)
c.box('r4', 805, 775, 230, 70, '서비스 DB\n(검증용 PostgreSQL)', GRAY, fs=17)
c.arrow('qa1', 175, 430, [[0, 0], [30, 0]])
c.arrow('qa2', 360, 430, [[0, 0], [25, 0]])
c.msg('qa3', 595, 635, 430, '통과')
c.msg('qa4', 785, 835, 430, '승인')
c.arrow('ra1', 920, 460, [[0, 0], [0, 75]], label='통과')
c.arrow('ra2', 920, 605, [[0, 0], [0, 50]])
c.arrow('ra3', 920, 725, [[0, 0], [0, 50]])
# branches
c.box('x1', 290, 545, 140, 50, '거절', PINK, PINKF, fs=18)
c.box('x2', 460, 545, 170, 50, '기존 결과 반환', GRAY, fs=17, dashed=True)
c.arrow('xa1', 465, 478, [[0, 0], [-100, 67]], label='버전 불일치')
c.arrow('xa2', 510, 480, [[0, 0], [35, 65]], label='같은 멱등 키', dashed=True)
c.box('x3', 650, 570, 120, 50, '반려됨', PINK, PINKF, fs=18)
c.arrow('xa3', 710, 460, [[0, 0], [0, 110]], label='반려')
c.arrow('lp', 675, 400, [[0, 0], [0, -30], [70, -30], [70, 0]], dashed=True)
c.ctext('lpt', 710, 342, '추가 조사 → 승인 대기 복귀', 16)
c.box('x4', 1050, 540, 80, 60, '반영\n차단', PINK, PINKF, fs=16)
c.arrow('xa4', 1005, 445, [[0, 0], [85, 0], [85, 95]], label='실패')
print(c.dump())
