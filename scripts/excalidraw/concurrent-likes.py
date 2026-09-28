import json
E=[]; INK='#1e1e1e'
PINK='#ffc9c9'; LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; GRAY='#dee2e6'
def text(i,x,y,t,fs=22): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":INK})
def uline(i,x,y,w,c): E.append({"type":"arrow","id":i,"x":x,"y":y,"width":w,"height":0,"points":[[0,0],[w,0]],"strokeColor":c,"strokeWidth":4,"endArrowhead":None})
def frame(i,x,y,w,h): E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":"#868e96","strokeWidth":2,"strokeStyle":"dashed","roundness":{"type":3}})
def box(i,x,y,w,h,label,shadow,fill='#ffffff',fs=20):
    E.append({"type":"rectangle","id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1,"roundness":{"type":3}})
    E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"roundness":{"type":3},"label":{"text":label,"fontSize":fs}})
def arrow(i,x,y,pts,label=None):
    d={"type":"arrow","id":i,"x":x,"y":y,"width":pts[-1][0],"height":pts[-1][1],"points":pts,"strokeColor":INK,"strokeWidth":2,"endArrowhead":"arrow"}
    if label: d["label"]={"text":label,"fontSize":18}
    E.append(d)
# before
frame('fl',20,20,560,620); text('tl',44,36,'변경 전  잠금 없는 토글 API'); uline('ul',44,68,280,PINK)
for k,x in (('a',70),('b',330)):
    cx=x+100
    box('r'+k,x,110,200,56,'요청 '+k.upper(),GRAY)
    arrow('ar'+k,cx,166,[[0,0],[0,44]])
    box('c'+k,x,210,200,56,'있는지 확인',GRAY)
    arrow('ac'+k,cx,266,[[0,0],[0,64]],label='없음')
    box('i'+k,x,330,200,56,'좋아요 추가',GRAY)
    arrow('ai'+k,cx,386,[[0,0],[0,64]])
box('oa',70,450,200,64,'성공',GRAY)
box('ob',330,450,200,64,'중복 오류',PINK,fill='#fff5f5')
# after
frame('fr',600,20,580,620); text('tr',624,36,'변경 후  행 잠금과 상태 지정 API'); uline('ur',624,68,340,LAV2)
box('sa',650,110,220,56,'요청 A  좋아요',GRAY)
box('sb',910,110,220,56,'요청 B  좋아요',GRAY)
arrow('asa',760,166,[[0,0],[0,44]]); arrow('asb',1020,166,[[0,0],[0,44]])
box('lk',700,210,380,60,'사용자 행 잠금',LAV)
arrow('alk',890,270,[[0,0],[0,70]],label='한 번에 하나씩')
box('pa',700,340,380,56,'A: 좋아요 추가',LAV)
arrow('apa',890,396,[[0,0],[0,34]])
box('pb',700,430,380,56,'B: 이미 좋아요라 그대로',LAV)
arrow('apb',890,486,[[0,0],[0,34]])
box('rs',700,520,380,64,'좋아요 1개, 오류 없음',LAV2,fill=LAVF)
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
