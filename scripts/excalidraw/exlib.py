"""Excalidraw 그림 공통 도구: 흰 박스, 검은 테두리, 색은 그림자로만 표시."""
import json

INK = '#1e1e1e'
PINK = '#ffc9c9'; PINKF = '#fff5f5'
LAV = '#d0bfff'; LAV2 = '#b197fc'; LAVF = '#f3f0ff'
GRAY = '#dee2e6'; YEL = '#ffec99'; MUTED = '#868e96'


def twidth(t, fs):
    return sum(fs * (1.0 if ord(ch) > 0x3000 else 0.55) for ch in t)


class Canvas:
    def __init__(self):
        self.E = []

    def text(self, i, x, y, t, fs=20, c=INK):
        self.E.append({"type": "text", "id": i, "x": x, "y": y, "text": t, "fontSize": fs, "strokeColor": c})

    def ctext(self, i, cx, y, t, fs=16, c=INK):
        self.text(i, cx - twidth(t, fs) / 2, y, t, fs, c)

    def uline(self, i, x, y, w, c):
        self.E.append({"type": "arrow", "id": i, "x": x, "y": y, "width": w, "height": 0, "points": [[0, 0], [w, 0]],
                       "strokeColor": c, "strokeWidth": 4, "endArrowhead": None})

    def frame(self, i, x, y, w, h, title=None, ucolor=None, fs=22):
        self.E.append({"type": "rectangle", "id": i, "x": x, "y": y, "width": w, "height": h, "strokeColor": MUTED,
                       "strokeWidth": 2, "strokeStyle": "dashed", "roundness": {"type": 3}})
        if title:
            self.text(i + "t", x + 24, y + 16, title, fs)
            if ucolor:
                self.uline(i + "u", x + 24, y + 48, twidth(title, fs) + 8, ucolor)

    def box(self, i, x, y, w, h, label, shadow=GRAY, fill='#ffffff', fs=20, dashed=False, shape='rectangle'):
        s = {"type": shape, "id": i + "s", "x": x + 8, "y": y + 8, "width": w, "height": h, "backgroundColor": shadow,
             "fillStyle": "solid", "strokeColor": shadow, "strokeWidth": 1}
        b = {"type": shape, "id": i, "x": x, "y": y, "width": w, "height": h, "backgroundColor": fill,
             "fillStyle": "solid", "strokeColor": INK, "strokeWidth": 2, "label": {"text": label, "fontSize": fs}}
        if shape == 'rectangle':
            s["roundness"] = b["roundness"] = {"type": 3}
        if dashed:
            b["strokeStyle"] = "dashed"; b["strokeColor"] = MUTED
        self.E.extend([s, b])

    def arrow(self, i, x, y, pts, label=None, dashed=False, color=INK, head="arrow", fs=16):
        d = {"type": "arrow", "id": i, "x": x, "y": y, "width": pts[-1][0], "height": pts[-1][1], "points": pts,
             "strokeColor": color, "strokeWidth": 2, "endArrowhead": head}
        if label:
            d["label"] = {"text": label, "fontSize": fs}
        if dashed:
            d["strokeStyle"] = "dashed"
        self.E.append(d)

    # sequence diagram helpers
    def lifeline(self, i, cx, y1, y2, label, shadow=GRAY, w=150, fs=20):
        self.box(i, cx - w / 2, y1, w, 50, label, shadow, fs=fs)
        self.E.append({"type": "arrow", "id": i + "l", "x": cx, "y": y1 + 58, "width": 0, "height": y2 - y1 - 58,
                       "points": [[0, 0], [0, y2 - y1 - 58]], "strokeColor": '#adb5bd', "strokeWidth": 1,
                       "strokeStyle": "dashed", "endArrowhead": None})

    def msg(self, i, x1, x2, y, label, ret=False, fs=16, lx=None):
        """메시지 화살표. 라벨은 선 위에 둔다(lx로 라벨 중심 지정 가능)."""
        self.arrow(i, x1, y, [[0, 0], [x2 - x1, 0]], dashed=ret)
        self.ctext(i + "t", lx if lx is not None else (x1 + x2) / 2, y - 26, label, fs)

    def dump(self):
        return json.dumps(self.E, ensure_ascii=False, separators=(',', ':'))
