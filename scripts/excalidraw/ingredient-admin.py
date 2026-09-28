import json
E=[]; INK='#1e1e1e'
def cam(x,y,w,h): E.append({"type":"cameraUpdate","x":x,"y":y,"width":w,"height":h})
def text(i,x,y,t,fs): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":INK})
def uline(i,x,y,w,c): E.append({"type":"arrow","id":i,"x":x,"y":y,"width":w,"height":0,"points":[[0,0],[w,0]],"strokeColor":c,"strokeWidth":4,"endArrowhead":None})
def frame(i,x,y,w,h): E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":"#868e96","strokeWidth":2,"strokeStyle":"dashed","roundness":{"type":3}})
def box(i,x,y,w,h,label,shadow,fill='#ffffff',dashed=False):
    E.append({"type":"rectangle","id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1,"roundness":{"type":3}})
    b={"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"roundness":{"type":3},"label":{"text":label,"fontSize":20}}
    if dashed: b["strokeStyle"]="dashed"
    E.append(b)
def arrow(i,a,b,x,y,pts,f1,f2,dashed=False):
    d={"type":"arrow","id":i,"x":x,"y":y,"width":pts[-1][0],"height":pts[-1][1],"points":pts,"strokeColor":INK,"strokeWidth":2,"endArrowhead":"arrow","startBinding":{"elementId":a,"fixedPoint":f1},"endBinding":{"elementId":b,"fixedPoint":f2}}
    if dashed: d["strokeStyle"]="dashed"
    E.append(d)
PINK='#ffc9c9'; LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; YEL='#ffec99'; GRAY='#dee2e6'
H=64
cam(-40,-10,1200,900)
# before
frame('fb',20,20,1110,250); text('tb',44,36,'변경 전  파일로 관리',22); uline('ub',44,68,196,PINK)
box('p1',44,100,150,H,'팀원',GRAY); box('p2',44,190,150,H,'AI 검수',GRAY)
box('x1',264,100,220,H,'엑셀 작업 파일',PINK); box('x2',264,190,220,H,'작업별 JSON 파일',PINK)
arrow('a1','p1','x1',194,132,[[0,0],[70,0]],[1,0.5],[0,0.5]); arrow('a2','p2','x2',194,222,[[0,0],[70,0]],[1,0.5],[0,0.5])
box('x3',600,145,280,H,'서버 시작 시 전체 읽기',PINK)
arrow('a3','x1','x3',484,132,[[0,0],[116,35]],[1,0.5],[0,0.35]); arrow('a4','x2','x3',484,222,[[0,0],[116,-35]],[1,0.5],[0,0.65])
# after
frame('fa',20,310,1110,430); text('ta',44,326,'변경 후  DB와 관리자 화면으로 관리',22); uline('ua',44,358,330,LAV2)
box('q1',44,390,150,H,'팀원',GRAY)
box('s1',254,390,210,H,'관리자 화면',LAV)
arrow('b1','q1','s1',194,422,[[0,0],[60,0]],[1,0.5],[0,0.5])
box('s2',534,390,220,H,'변경 요청 API',LAV)
arrow('b2','s1','s2',464,422,[[0,0],[70,0]],[1,0.5],[0,0.5])
box('s3',854,390,200,H,'요청 거절',YEL,dashed=True)
arrow('b3','s2','s3',754,422,[[0,0],[100,0]],[1,0.5],[0,0.5],dashed=True)
box('s4',254,520,210,H,'작업 상태 DB',GRAY)
arrow('b4','s2','s4',644,454,[[0,0],[0,33],[-285,33],[-285,66]],[0.5,1],[0.5,0])
box('s5',534,520,220,H,'확정 데이터 DB',LAV2,fill=LAVF)
arrow('b5','s2','s5',644,454,[[0,0],[0,66]],[0.5,1],[0.5,0])
box('s6',534,640,220,H,'배포용 데이터 묶음',LAV2,fill=LAVF)
arrow('b6','s5','s6',644,584,[[0,0],[0,56]],[0.5,1],[0.5,0])
box('s7',854,640,200,H,'서비스 DB',GRAY)
arrow('b7','s6','s7',754,672,[[0,0],[100,0]],[1,0.5],[0,0.5])
cam(-40,-10,1200,900)
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
