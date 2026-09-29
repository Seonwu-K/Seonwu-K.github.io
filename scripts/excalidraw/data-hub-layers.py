import json
E=[]; INK='#1e1e1e'
PINK='#ffc9c9'; LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; YEL='#ffec99'; GRAY='#dee2e6'
def cam(x,y,w,h): E.append({"type":"cameraUpdate","x":x,"y":y,"width":w,"height":h})
def text(i,x,y,t,fs=22): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":INK})
def uline(i,x,y,w,c): E.append({"type":"arrow","id":i,"x":x,"y":y,"width":w,"height":0,"points":[[0,0],[w,0]],"strokeColor":c,"strokeWidth":4,"endArrowhead":None})
def frame(i,x,y,w,h,c="#868e96",sw=2): E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":c,"strokeWidth":sw,"strokeStyle":"dashed","roundness":{"type":3}})
def box(i,x,y,w,h,label,shadow,fill='#ffffff',shape='rectangle',dashed=False):
    s={"type":shape,"id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1}
    b={"type":shape,"id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"label":{"text":label,"fontSize":20}}
    if shape=='rectangle': s["roundness"]=b["roundness"]={"type":3}
    if dashed: b["strokeStyle"]="dashed"; b["strokeColor"]="#868e96"
    E.extend([s,b])
def arrow(i,x,y,pts,a=None,f1=None,b=None,f2=None,dashed=False,label=None):
    d={"type":"arrow","id":i,"x":x,"y":y,"width":pts[-1][0],"height":pts[-1][1],"points":pts,"strokeColor":INK,"strokeWidth":2,"endArrowhead":"arrow"}
    if a: d["startBinding"]={"elementId":a,"fixedPoint":f1}
    if b: d["endBinding"]={"elementId":b,"fixedPoint":f2}
    if dashed: d["strokeStyle"]="dashed"
    if label: d["label"]={"text":label,"fontSize":16}
    E.append(d)
cam(-40,-10,1200,900)
# top: layers
text('tt',44,36,'데이터 3계층 구조 (L0~L2)'); uline('ut',44,68,260,LAV2)
frame('l0',44,90,320,210,"#b87333",3); text('l0t',64,102,'L0 Bronze  원본 보관',20)
box('o1',74,140,260,54,'공공데이터, 엑셀',GRAY); box('o2',74,226,260,54,'이전 산출물, 검토 이력',GRAY)
arrow('ab1',364,195,[[0,0],[50,0]])
frame('l1',414,90,330,210,"#868e96",3); text('l1t',434,102,'L1 Silver  정리와 검토',20)
box('c1',449,140,260,54,'정리된 데이터',LAV); box('c2',449,226,260,54,'검토 중 후보',LAV)
arrow('ac',579,194,[[0,0],[0,32]],'c1',[0.5,1],'c2',[0.5,0])
arrow('ab2',744,195,[[0,0],[50,0]],label='승인')
frame('l2',794,90,316,210,"#d4a017",3); text('l2t',814,102,'L2 Gold  승인 데이터',20)
box('g1',822,140,260,54,'승인된 필드만',LAV2,LAVF); box('g2',822,226,260,54,'서비스 DB',GRAY)
arrow('ag',952,194,[[0,0],[0,32]],'g1',[0.5,1],'g2',[0.5,0])
# bottom: LangGraph workflow with conditional admin review, plus how execution failures are handled
import exlib
c = exlib.Canvas()
c.frame('fl', 20, 370, 1120, 560, 'LangGraph 기반 Human-in-the-Loop 검증 흐름', LAV2)
c.E.append({"type": "ellipse", "id": "st", "x": 30, "y": 459, "width": 22, "height": 22,
            "backgroundColor": INK, "fillStyle": "solid", "strokeColor": INK})
c.arrow('a0', 52, 470, [[0, 0], [18, 0]])
c.box('n1', 70, 440, 130, 60, '근거 찾기', LAV, fs=18)
c.box('n2', 240, 440, 130, 60, '근거 고르기', LAV, fs=18)
c.box('n3', 410, 440, 165, 60, '설명과 태그 쓰기', LAV, fs=17)
c.box('n4', 615, 440, 150, 60, '다른 역할 검토', LAV, fs=17)
c.box('n5', 800, 420, 170, 100, '규칙 검사', YEL, shape='diamond', fs=18)
c.box('n9', 1020, 440, 110, 60, '추가 조사', PINK, exlib.PINKF, fs=17)
for i, x1, x2 in (('e1', 200, 240), ('e2', 370, 410), ('e3', 575, 615), ('e4', 765, 800)):
    c.arrow(i, x1, 470, [[0, 0], [x2 - x1, 0]])
c.msg('e5', 970, 1020, 470, '실패')
c.box('h1', 795, 570, 180, 100, '관리자 검수\n필요?', YEL, shape='diamond', fs=16)
c.arrow('e6', 885, 520, [[0, 0], [0, 50]], label='통과')
c.box('h2', 590, 590, 150, 60, '체크포인트 저장', GRAY, fs=17)
c.box('h3', 340, 580, 200, 80, 'interrupt\n관리자 검수', YEL, shape='ellipse', fs=18)
c.msg('e7', 795, 740, 620, '예')
c.arrow('e8', 590, 620, [[0, 0], [-50, 0]])
c.box('h4', 60, 740, 190, 64, 'L1 검토 후보\n(승인되면 L2)', LAV2, LAVF, fs=17)
c.arrow('e9', 340, 620, [[0, 0], [-185, 0], [-185, 120]], label='승인 후 재개')
c.arrow('e10', 885, 670, [[0, 0], [0, 102], [-635, 102]], label='아니오')
c.E.append({"type": "rectangle", "id": "fp", "x": 300, "y": 810, "width": 830, "height": 100, "strokeColor": exlib.MUTED,
            "strokeWidth": 1, "strokeStyle": "dashed", "roundness": {"type": 3}})
c.text('fpt', 316, 818, '실행 실패 처리 (LLM 호출 오류)', 16, exlib.MUTED)
c.box('f1', 320, 852, 95, 38, '일시 실패', GRAY, fs=16)
c.box('f2', 440, 852, 150, 38, 'RETRY_WAIT', PINK, exlib.PINKF, fs=16)
c.box('f3', 615, 852, 75, 38, '재시도', GRAY, fs=16)
c.box('f4', 770, 852, 95, 38, '반복 실패', GRAY, fs=16)
c.box('f5', 890, 852, 105, 38, 'PARKED', PINK, exlib.PINKF, fs=16)
c.box('f6', 1020, 852, 100, 38, '다음 원료', GRAY, fs=16)
for i, x1, x2 in (('fa1', 415, 440), ('fa2', 590, 615), ('fa3', 865, 890), ('fa4', 995, 1020)):
    c.arrow(i, x1, 871, [[0, 0], [x2 - x1, 0]])
E.extend(c.E)
cam(-40,-10,1200,900)
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
