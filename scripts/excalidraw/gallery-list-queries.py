"""사례 05: 응답 구조 변경(위)과 실제로 나간 SQL 쿼리 목록(아래)."""
from exlib import *

c = Canvas()


def rows(prefix, x, y, items):
    for n, (no, label, kind) in enumerate(items):
        if kind == 'gap':
            c.ctext(f'{prefix}g{n}', x + 286, y + 4, '⋮   게시글마다 이미지 조회 반복 (× 50)', 16, MUTED)
            y += 40
            continue
        sh, fill, dashed = {'img': (PINK, PINKF, False), 'key': (LAV2, LAVF, False),
                            'skip': (GRAY, '#ffffff', True)}.get(kind, (GRAY, '#ffffff', False))
        if no:
            c.box(f'{prefix}n{n}', x, y, 60, 42, no, GRAY, fs=16)
        c.box(f'{prefix}q{n}', x + 76, y, 420, 42, label, sh, fill, fs=17, dashed=dashed)
        y += 54


# before
c.frame('fb', 20, 20, 560, 580, '변경 전  쿼리 53회', PINK)
c.box('bs1', 44, 92, 180, 50, '게시글 엔티티', GRAY, fs=17)
c.box('bs2', 284, 92, 256, 50, '이미지 목록 포함 DTO', PINK, PINKF, fs=17)
c.arrow('bsa', 224, 117, [[0, 0], [60, 0]])
c.text('bl', 44, 170, '실행된 SQL', 16, MUTED)
rows('b', 44, 200, [('1', '게시글 50건', ''), ('2', '이미지 (게시글 1)', 'img'), ('3', '이미지 (게시글 2)', 'img'),
                    ('', '', 'gap'), ('51', '이미지 (게시글 50)', 'img'),
                    ('52', '좋아요 수 IN (...)', ''), ('53', '태그 IN (...)', '')])

# after
c.frame('fa', 600, 20, 560, 580, '변경 후  쿼리 4회', LAV2)
c.box('as1', 624, 92, 180, 50, '게시글', GRAY, fs=17)
c.box('as2', 864, 88, 256, 58, '목록 전용 DTO\n(이미지 목록 제외)', LAV2, LAVF, fs=16)
c.arrow('asa', 804, 117, [[0, 0], [60, 0]])
c.text('al', 624, 170, '실행된 SQL', 16, MUTED)
rows('a', 624, 200, [('1', '게시글 + 작성자 + 카테고리 (fetch join)', 'key'), ('2', '전체 개수', ''),
                     ('3', '좋아요 수 IN (...)', ''), ('4', '태그 IN (...)', ''),
                     ('', '이미지 조회 없음', 'skip')])
print(c.dump())
