"""사례 03: 변경 전 롤백에 가려진 배포 실패(시퀀스), 변경 후 관측 구조와 알림 시간(구조도)."""
from exlib import *

c = Canvas()
# before: sequence of the failed deploy hidden by rollback
c.frame('fb', 20, 20, 1120, 650, '변경 전  롤백에 가려진 배포 실패', PINK)
X = {'tm': 130, 'cp': 420, 'be': 710, 'cw': 1000}
c.lifeline('ltm', X['tm'], 100, 640, '팀', w=150)
c.lifeline('lcp', X['cp'], 100, 640, 'CodePipeline,\nCodeDeploy', w=190, fs=16)
c.lifeline('lbe', X['be'], 100, 640, '백엔드 EC2', w=160)
c.lifeline('lcw', X['cw'], 100, 640, 'CloudWatch', w=160, fs=18)
c.msg('m1', X['tm'], X['cp'], 200, '새 버전 배포')
c.msg('m2', X['cp'], X['be'], 255, '새 버전 설치, 시작')
c.msg('m3', X['be'], X['cp'], 310, '기동 실패 (파일 누락)', ret=True)
c.msg('m4', X['cp'], X['be'], 365, '이전 버전으로 롤백')
c.msg('m5', X['be'], X['cp'], 420, '정상 동작', ret=True)
c.msg('m6', X['cw'], X['be'], 475, 'EC2 상태, 자원 확인')
c.msg('m7', X['be'], X['cw'], 530, 'EC2 정상', ret=True)
c.box('miss', X['tm'] - 100, 565, 200, 60, '배포 실패 알림 없음\n48시간 뒤 수동 확인', PINK, PINKF, fs=16)

# after: observability structure and how fast the alert arrives
dy = 700
c.frame('fa', 20, dy, 1120, 420, '변경 후  프로세스까지 보는 모니터링과 알림', LAV2)
c.box('a1', 40, dy + 130, 160, 70, '서버별 Alloy')
c.box('a2', 290, dy + 135, 170, 60, 'Cloudflare Tunnel', LAV, fs=17)
c.box('a3', 530, dy + 80, 200, 56, 'Loki (로그)', LAV, fs=18)
c.box('a4', 530, dy + 190, 200, 56, 'Prometheus (지표)', LAV, fs=18)
c.box('a5', 810, dy + 130, 220, 64, 'Grafana 알림 규칙', LAV2, LAVF)
c.box('a6', 530, dy + 310, 200, 64, 'Blackbox\n(공개 주소 확인)', LAV, fs=16)
c.box('a7', 810, dy + 300, 220, 64, '팀 Discord', YEL)
c.msg('aa1', 200, 290, dy + 165, '지표, 로그')
c.arrow('aa2', 460, dy + 158, [[0, 0], [70, -50]])
c.arrow('aa3', 460, dy + 172, [[0, 0], [70, 46]])
c.arrow('aa4', 730, dy + 108, [[0, 0], [80, 42]])
c.arrow('aa5', 730, dy + 218, [[0, 0], [80, -42]])
c.arrow('aa6', 630, dy + 310, [[0, 0], [0, -64]], label='확인 결과')
c.arrow('aa7', 920, dy + 194, [[0, 0], [0, 106]], label='조건 2분 지속')
c.text('at', 818, dy + 384, '2~3분 내 수신 (스테이징 측정)', 15, MUTED)
print(c.dump())
