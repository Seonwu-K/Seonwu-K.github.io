"""사례 05: DB 백업 방식 변경 전후, (full) 복구 리허설 소요 시간.
인자 full: 아래에 새 EC2 전체 복구 리허설 단계별 시간을 추가한다.
"""
import sys
from exlib import *

FULL = 'full' in sys.argv
c = Canvas()

# before
c.frame('fb', 20, 20, 1120, 200, '변경 전  하루 1회 pg_dump', PINK)
c.box('b1', 50, 100, 240, 70, 'EC2 Docker\nPostgres', None, fs=18)
c.msg('ba1', 290, 470, 135, '매일 1회 덤프')
c.box('b2', 470, 100, 160, 70, 'S3', None, fs=18)
c.box('b3', 720, 100, 390, 70, '최대 24시간치 데이터 손실\n복원 가능 여부는 확인 안 됨', PINK, PINKF, fs=17)

# after
c.frame('fa', 20, 250, 1120, 330, '변경 후  pgBackRest WAL 아카이빙과 복구 리허설', LAV2)
c.box('a1', 50, 340, 240, 70, 'EC2 Docker\nPostgres', None, fs=18)
c.box('a2', 360, 330, 250, 90, 'pgBackRest\n전체 주 1회, 증분 매일\nWAL 5분 안에 전송', LAV, fs=16)
c.box('a3', 680, 340, 190, 70, 'S3\n(삭제 불가)', None, fs=17)
c.arrow('aa1', 290, 375, [[0, 0], [70, 0]])
c.arrow('aa2', 610, 375, [[0, 0], [70, 0]])
c.box('a4', 930, 330, 190, 90, '데이터 손실 한도\n5분\n(실측 132초)', LAV2, LAVF, fs=16)
c.arrow('aa3', 870, 375, [[0, 0], [60, 0]])
# rehearsal
c.box('r1', 360, 480, 250, 64, '특정 시점 복원 (PITR)\nDB 복원 약 10초', LAV, fs=16)
c.box('r2', 680, 480, 440, 64, '새 EC2에서 문서만 보고 전체 복구\n약 2분 20초 (첫 리허설 7분 13초)', LAV, fs=16)
c.arrow('ra2', 775, 410, [[0, 0], [0, 70]])
c.arrow('ra3', 775, 410, [[0, 0], [0, 38], [-290, 38], [-290, 70]])
c.text('rat', 790, 424, '복구 리허설', 16)

if FULL:
    dy = 610
    c.frame('fr', 20, dy, 1120, 250, '새 EC2 전체 복구 리허설  단계별 소요 (순수 실행)', LAV2)
    steps = [('기동', 17), ('부트스트랩', 60), ('설정, 이미지', 18), ('DB 복원', 18), ('백엔드 배포', 29)]
    x, scale = 50, 6.2
    for n, (name, sec) in enumerate(steps):
        w = sec * scale
        sh = LAV2 if name == 'DB 복원' else LAV
        c.box(f's{n}', x, dy + 95, w, 56, '', sh, LAVF if name == 'DB 복원' else '#ffffff', fs=14)
        c.ctext(f's{n}t', x + w / 2, dy + 160, f'{name}', 15)
        c.ctext(f's{n}n', x + w / 2, dy + 113, f'{sec}초', 15)
        x += w + 6
    c.text('stot', x + 14, dy + 108, '= 약 2분 20초', 20)
    c.text('snote', 50, dy + 200, '막힌 지점 두 곳(비공개 저장소 clone 실패, 복원본의 WAL이 운영 백업을 오염)을 런북에 반영', 15, MUTED)
print(c.dump())
