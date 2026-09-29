"""사례 04: 동시 요청 시퀀스(비관적 락 전후)와 같은 요청 재시도 시 결과 비교."""
from exlib import *

c = Canvas()
# before: both requests read "none" and insert
c.frame('fb', 20, 20, 560, 640, '변경 전  잠금 없는 토글 API', PINK)
A, B, D = 110, 300, 490
for i, x, t in (('ba', A, '요청 A'), ('bb', B, '요청 B'), ('bd', D, 'DB')):
    c.lifeline(i, x, 100, 630, t, w=140)
AB = (A + B) / 2
c.msg('b1', A, D, 200, '좋아요 있나?', lx=AB)
c.msg('b2', B, D, 250, '좋아요 있나?')
c.msg('b3', D, A, 300, '없음', ret=True, lx=AB)
c.msg('b4', D, B, 350, '없음', ret=True)
c.msg('b5', A, D, 410, 'INSERT', lx=AB)
c.msg('b6', B, D, 460, 'INSERT')
c.msg('b7', D, A, 510, '성공', ret=True, lx=AB)
c.msg('b8', D, B, 560, '중복 키 오류', ret=True)
c.box('be', B - 70, 580, 140, 40, '실패', PINK, PINKF, fs=18)

# after: user row lock serializes the two requests
c.frame('fa', 600, 20, 560, 640, '변경 후  비관적 락과 상태 지정 API', LAV2)
A2, B2, D2 = 670, 880, 1090
c.lifeline('aa', A2, 100, 630, '요청 A', w=120)
c.lifeline('ab', B2, 100, 630, '요청 B', w=120)
c.lifeline('ad', D2, 100, 630, 'DB', w=120)
AB2 = (A2 + B2) / 2
c.msg('a1', A2, D2, 200, 'SELECT user FOR UPDATE', lx=AB2, fs=15)
c.msg('a2', B2, D2, 250, 'SELECT user FOR UPDATE', fs=15)
c.box('aw', B2 - 60, 272, 120, 40, '잠금 대기', YEL, fs=18)
c.msg('a3', A2, D2, 350, '저장 후 커밋', lx=AB2)
c.msg('a4', D2, B2, 395, 'A 커밋 후 잠금 획득', ret=True, fs=15)
c.msg('a5', B2, D2, 460, 'liked=true')
c.msg('a6', D2, B2, 510, '이미 좋아요, 변경 없음', ret=True)
c.box('ar', A2 - 50, 570, 500, 50, '좋아요 1개, 오류 없음', LAV2, LAVF, fs=18)

# retry: toggle vs desired state
c.frame('fr', 20, 690, 1140, 250, '같은 요청 재시도 시 결과 비교', LAV2)
c.ctext('h1', 480, 756, '첫 요청', 18)
c.ctext('h2', 860, 756, '재시도', 18)
c.box('r1', 50, 790, 250, 56, '토글 API', GRAY, fs=18)
c.box('r2', 360, 790, 240, 56, '꺼짐 → 켜짐', GRAY, fs=18)
c.box('r3', 740, 790, 240, 56, '켜짐 → 꺼짐', PINK, PINKF, fs=18)
c.box('r4', 50, 866, 250, 56, '상태 지정 API\n(liked: true)', GRAY, fs=16)
c.box('r5', 360, 866, 240, 56, '꺼짐 → 켜짐', GRAY, fs=18)
c.box('r6', 740, 866, 240, 56, '켜짐 → 켜짐', LAV2, LAVF, fs=18)
c.arrow('ra1', 600, 818, [[0, 0], [140, 0]])
c.arrow('ra2', 600, 894, [[0, 0], [140, 0]])
print(c.dump())
