import json
E=[]; INK='#1e1e1e'
PINK='#ffc9c9'; LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; YEL='#ffec99'; GRAY='#dee2e6'
def cam(x,y,w,h): E.append({"type":"cameraUpdate","x":x,"y":y,"width":w,"height":h})
def text(i,x,y,t,fs=22): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":INK})
def uline(i,x,y,w,c): E.append({"type":"arrow","id":i,"x":x,"y":y,"width":w,"height":0,"points":[[0,0],[w,0]],"strokeColor":c,"strokeWidth":4,"endArrowhead":None})
def frame(i,x,y,w,h,c="#868e96"): E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":c,"strokeWidth":2,"strokeStyle":"dashed","roundness":{"type":3}})
def box(i,x,y,w,h,label,shadow,fill='#ffffff',shape='rectangle'):
    s={"type":shape,"id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1}
    b={"type":shape,"id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"label":{"text":label,"fontSize":20}}
    if shape=='rectangle': s["roundness"]=b["roundness"]={"type":3}
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
frame('ft',20,20,1110,300); text('tt',44,36,'데이터를 세 단계로 나눔'); uline('ut',44,68,240,LAV2)
frame('l0',44,90,320,210,"#adb5bd"); text('l0t',64,102,'L0  원본 보관',20)
box('o1',74,140,260,54,'공공데이터, 엑셀',GRAY); box('o2',74,226,260,54,'이전 작업 결과',GRAY)
arrow('ab1',364,195,[[0,0],[50,0]])
frame('l1',414,90,330,210,"#adb5bd"); text('l1t',434,102,'L1  정리와 확정',20)
box('c1',449,140,260,54,'검사 중 데이터',LAV); box('c2',449,226,260,54,'확정 데이터',LAV2,LAVF)
arrow('ac',579,194,[[0,0],[0,32]],'c1',[0.5,1],'c2',[0.5,0])
arrow('ab2',744,195,[[0,0],[50,0]])
frame('l2',794,90,316,210,"#adb5bd"); text('l2t',814,102,'L2  서비스 전달',20)
box('g1',822,140,260,54,'배포용 묶음',LAV2,LAVF); box('g2',822,226,260,54,'서비스 DB',GRAY)
arrow('ag',952,194,[[0,0],[0,32]],'g1',[0.5,1],'g2',[0.5,0])
# bottom: one item flow
frame('fb',20,350,1110,580); text('tb',44,366,'원료 한 건이 처리되는 순서'); uline('ubl',44,398,270,LAV2)
box('w1',74,430,160,60,'작업 가져오기',GRAY)
box('w2',264,430,140,60,'입력 준비',GRAY)
arrow('aw1',234,460,[[0,0],[30,0]])
frame('fl',436,420,674,216,"#9775fa"); text('flt',456,432,'LLM이 맡는 단계',20)
arrow('aw2',404,460,[[0,0],[32,0]])
box('m1',460,470,190,60,'근거 찾기',LAV)
box('m2',690,470,190,60,'근거 고르기',LAV)
arrow('am1',650,500,[[0,0],[40,0]])
box('m3',920,470,170,60,'설명과 태그 쓰기',LAV)
arrow('am2',880,500,[[0,0],[40,0]])
box('m4',920,560,170,60,'다른 역할이 검토',LAV)
arrow('am3',1005,530,[[0,0],[0,30]])
box('d1',690,660,210,110,'규칙 검사',YEL,shape='diamond')
arrow('ad0',1005,620,[[0,0],[0,20],[-210,20],[-210,40]])
box('r1',120,820,230,60,'확정 데이터에 반영',LAV2,LAVF)
box('r2',450,820,200,60,'사람 확인 대기',YEL)
box('r3',880,820,230,60,'다시 시도 또는 보류',PINK)
arrow('ar1',690,715,[[0,0],[-455,0],[-455,105]],label='통과')
arrow('ar2',795,770,[[0,0],[0,25],[-245,25],[-245,50]],label='판단 필요')
arrow('ar3',900,715,[[0,0],[95,0],[95,105]],label='실패')
arrow('ar4',450,850,[[0,0],[-100,0]],label='승인')
arrow('ar5',995,880,[[0,0],[0,22],[-951,22],[-951,-422],[-921,-422]],dashed=True)
text('rt',470,904,'재시도',16)
cam(-40,-10,1200,900)
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
