import json
E=[]; INK='#1e1e1e'
PINK='#ffc9c9'; PINKF='#fff5f5'; LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; GRAY='#dee2e6'; YEL='#ffec99'
def text(i,x,y,t,fs=22,c=INK): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":c})
def uline(i,x,y,w,c): E.append({"type":"arrow","id":i,"x":x,"y":y,"width":w,"height":0,"points":[[0,0],[w,0]],"strokeColor":c,"strokeWidth":4,"endArrowhead":None})
def frame(i,x,y,w,h): E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":"#868e96","strokeWidth":2,"strokeStyle":"dashed","roundness":{"type":3}})
def box(i,x,y,w,h,label,shadow=GRAY,fill='#ffffff',fs=20):
    E.append({"type":"rectangle","id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1,"roundness":{"type":3}})
    E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"roundness":{"type":3},"label":{"text":label,"fontSize":fs}})
def arrow(i,x,y,pts,label=None,dashed=False):
    d={"type":"arrow","id":i,"x":x,"y":y,"width":pts[-1][0],"height":pts[-1][1],"points":pts,"strokeColor":INK,"strokeWidth":2,"endArrowhead":"arrow"}
    if label: d["label"]={"text":label,"fontSize":16}
    if dashed: d["strokeStyle"]="dashed"
    E.append(d)
# before: rollback hides the failed deploy
frame('fb',20,20,1120,330); text('tb',44,36,'변경 전  롤백에 가려진 배포 실패'); uline('ub',44,68,330,PINK)
box('b1',50,110,180,60,'새 버전 배포')
box('b2',300,110,200,60,'백엔드 기동 실패',PINK)
box('b3',570,110,160,60,'자동 롤백')
box('b4',800,110,300,60,'이전 버전으로 정상 화면')
arrow('ab1',230,140,[[0,0],[70,0]])
arrow('ab2',500,140,[[0,0],[70,0]])
arrow('ab3',730,140,[[0,0],[70,0]])
box('c1',300,250,200,60,'CloudWatch, SNS')
box('c2',570,250,530,60,'알림 없음, 48시간 뒤 발견',PINK,PINKF)
arrow('ac0',400,170,[[0,0],[0,80]],label='EC2 생존만 확인',dashed=True)
arrow('ac1',500,280,[[0,0],[70,0]])
# after: process-level monitoring and team alert
frame('fa',20,390,1120,370); text('ta',44,406,'변경 후  프로세스까지 보는 모니터링과 알림'); uline('ua',44,438,430,LAV2)
box('a1',40,480,180,80,'서버별 Alloy')
box('a2',340,490,190,60,'Cloudflare Tunnel',LAV,fs=18)
box('a3',600,490,200,60,'Prometheus, Loki',LAV,fs=18)
box('a4',870,490,230,60,'Grafana 알림 규칙',LAV2,LAVF)
box('a5',870,650,230,64,'팀 Discord',YEL)
box('a6',600,650,200,64,'Blackbox',LAV,fs=18)
arrow('aa1',220,520,[[0,0],[120,0]],label='지표, 로그')
arrow('aa2',530,520,[[0,0],[70,0]])
arrow('aa3',800,520,[[0,0],[70,0]])
arrow('aa4',985,550,[[0,0],[0,100]],label='조건 지속 시')
arrow('aa5',700,650,[[0,0],[0,-100]],label='공개 주소 확인')
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
