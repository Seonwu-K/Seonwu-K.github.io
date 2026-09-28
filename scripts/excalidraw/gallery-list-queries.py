import json
E=[]; INK='#1e1e1e'
PINK='#ffc9c9'; LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; YEL='#ffec99'; GRAY='#dee2e6'
def text(i,x,y,t,fs=22,c=INK): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":c})
def uline(i,x,y,w,c): E.append({"type":"arrow","id":i,"x":x,"y":y,"width":w,"height":0,"points":[[0,0],[w,0]],"strokeColor":c,"strokeWidth":4,"endArrowhead":None})
def frame(i,x,y,w,h,c="#868e96"): E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":c,"strokeWidth":2,"strokeStyle":"dashed","roundness":{"type":3}})
def box(i,x,y,w,h,label,shadow,fill='#ffffff',dashed=False,fs=20,stroke=INK):
    E.append({"type":"rectangle","id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1,"roundness":{"type":3}})
    b={"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":stroke,"strokeWidth":2,"roundness":{"type":3},"label":{"text":label,"fontSize":fs}}
    if dashed: b["strokeStyle"]="dashed"
    E.append(b)
def plain(i,x,y,w,h,fill,stroke=INK):
    E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":stroke,"strokeWidth":2,"roundness":{"type":3}})
def arrow(i,x,y,pts,label=None,dashed=False):
    d={"type":"arrow","id":i,"x":x,"y":y,"width":pts[-1][0],"height":pts[-1][1],"points":pts,"strokeColor":INK,"strokeWidth":2,"endArrowhead":"arrow"}
    if label: d["label"]={"text":label,"fontSize":18}
    if dashed: d["strokeStyle"]="dashed"
    E.append(d)
# before
frame('fl',20,20,560,640); text('tl',44,36,'변경 전  이미지까지 담는 목록'); uline('ul',44,68,300,PINK)
box('a1',70,100,260,60,'목록 요청',GRAY)
arrow('aa1',200,160,[[0,0],[0,40]])
box('a2',70,200,260,60,'게시글 50건 조회',GRAY)
arrow('aa2',200,260,[[0,0],[0,50]])
# stacked cards for repeated image queries
plain('st3',94,334,260,60,'#ffc9c9'); plain('st2',82,322,260,60,'#ffe3e3')
E.append({"type":"rectangle","id":"a3","x":70,"y":310,"width":260,"height":60,"backgroundColor":"#ffffff","fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"roundness":{"type":3},"label":{"text":"이미지 조회","fontSize":20}})
arrow('loop',330,340,[[0,0],[90,0],[90,-100],[10,-100]],label='N+1 (N=50)',dashed=True)
arrow('aa3',200,394,[[0,0],[0,46]])
box('a4',70,440,260,60,'좋아요 수, 태그\nIN 조회 각 1회',GRAY,fs=18)
arrow('aa4',200,500,[[0,0],[0,50]])
box('a5',70,550,260,70,'쿼리 53회',PINK,fill='#fff5f5',fs=24)
# after
frame('fr',600,20,560,640); text('tr',624,36,'변경 후  목록 전용 DTO'); uline('ur',624,68,235,LAV2)
box('b1',650,100,260,60,'목록 요청',GRAY)
arrow('bb1',780,160,[[0,0],[0,40]])
box('b2',650,200,260,60,'게시글 목록 조회',LAV)
box('b2c',940,200,190,60,'전체 개수 조회',LAV)
arrow('bb2c',910,230,[[0,0],[30,0]])
arrow('bb2',780,260,[[0,0],[0,50]])
box('b3',650,310,260,60,'이미지 조회 제외\n(목록 전용 DTO)',GRAY,dashed=True,stroke='#868e96',fs=18)
arrow('bb3',780,370,[[0,0],[0,70]])
box('b4',650,440,260,60,'좋아요 수, 태그\nIN 조회 각 1회',LAV,fs=18)
arrow('bb4',780,500,[[0,0],[0,50]])
box('b5',650,550,260,70,'쿼리 4회',LAV2,fill=LAVF,fs=24)
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
