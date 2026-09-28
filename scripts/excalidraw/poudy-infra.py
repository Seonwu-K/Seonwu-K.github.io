import json
E=[]; INK='#1e1e1e'
LAV='#d0bfff'; LAV2='#b197fc'; LAVF='#f3f0ff'; GRAY='#dee2e6'; YEL='#ffec99'
def text(i,x,y,t,fs=20,c=INK): E.append({"type":"text","id":i,"x":x,"y":y,"text":t,"fontSize":fs,"strokeColor":c})
def frame(i,x,y,w,h,label,c="#868e96"):
    E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"strokeColor":c,"strokeWidth":2,"strokeStyle":"dashed","roundness":{"type":3}})
    text(i+"t",x+16,y+12,label,18,"#495057")
def box(i,x,y,w,h,label,shadow=GRAY,fill='#ffffff',fs=20):
    E.append({"type":"rectangle","id":i+"s","x":x+8,"y":y+8,"width":w,"height":h,"backgroundColor":shadow,"fillStyle":"solid","strokeColor":shadow,"strokeWidth":1,"roundness":{"type":3}})
    E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":w,"height":h,"backgroundColor":fill,"fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"roundness":{"type":3},"label":{"text":label,"fontSize":fs}})
def tile(i,x,y,label,color):
    E.append({"type":"rectangle","id":i,"x":x,"y":y,"width":56,"height":44,"backgroundColor":color,"fillStyle":"solid","strokeColor":INK,"strokeWidth":1,"label":{"text":label,"fontSize":16,"strokeColor":"#ffffff"}})
def arrow(i,x,y,pts,label=None,dashed=False):
    d={"type":"arrow","id":i,"x":x,"y":y,"width":pts[-1][0],"height":pts[-1][1],"points":pts,"strokeColor":INK,"strokeWidth":2,"endArrowhead":"arrow"}
    if label: d["label"]={"text":label,"fontSize":16}
    if dashed: d["strokeStyle"]="dashed"
    E.append(d)
AWS='#e8590c'; S3C='#2f9e44'
# client
E.append({"type":"ellipse","id":"cl","x":30,"y":230,"width":180,"height":180,"backgroundColor":"#ffffff","fillStyle":"solid","strokeColor":INK,"strokeWidth":2,"label":{"text":"웹, 앱\n사용자","fontSize":20}})
# frontend EC2
frame('fe',260,110,310,390,'Frontend EC2'); tile('fetile',506,94,'EC2',AWS)
box('ng',290,160,250,80,'Nginx',LAV)
box('nx',290,300,250,80,'Next.js',GRAY)
box('fa',290,420,120,44,'Alloy',YEL,fs=16)
arrow('a1',210,300,[[0,0],[80,-100]],label='poudy.site')
arrow('a2',415,240,[[0,0],[0,60]],label='페이지')
# backend EC2
frame('be',630,110,290,230,'Backend EC2'); tile('betile',856,94,'EC2',AWS)
box('sp',660,160,230,90,'Spring Boot',LAV2,LAVF)
box('ba',660,280,110,44,'Alloy',YEL,fs=16)
arrow('a3',540,200,[[0,0],[120,0]],label='/api/*')
arrow('a4',540,340,[[0,0],[120,-100]])
# DB EC2
frame('db',630,380,290,150,'DB EC2'); tile('dbtile',856,364,'EC2',AWS)
box('pg',660,430,230,70,'PostgreSQL',LAV2,LAVF)
arrow('a5',830,250,[[0,0],[0,180]],label='사설망')
# S3
box('s3a',990,160,190,80,'피드백 이미지',GRAY); tile('s3at',1140,144,'S3',S3C)
box('s3b',990,430,190,70,'DB 백업',GRAY); tile('s3bt',1140,414,'S3',S3C)
arrow('a6',890,200,[[0,0],[100,0]])
arrow('a7',890,465,[[0,0],[100,0]],label='매일')
# monitoring EC2
frame('mo',260,580,920,190,'Monitoring EC2'); tile('motile',1116,564,'EC2',AWS); next(e for e in E if e['id']=='mot').update(x=276,y=738)
box('cf',290,640,200,80,'Cloudflare Tunnel',GRAY,fs=18)
box('pm',560,625,170,50,'Prometheus',GRAY,fs=18)
box('lk',560,690,170,50,'Loki',GRAY,fs=18)
box('gf',800,640,160,80,'Grafana',LAV)
box('bb',1000,640,160,80,'Blackbox',GRAY,fs=18)
arrow('m1',350,464,[[0,0],[0,176]],label='지표, 로그',dashed=True)
arrow('m2',660,302,[[0,0],[-60,0],[-60,258],[-190,258],[-190,338]],dashed=True)
arrow('m3',490,670,[[0,0],[70,-20]])
arrow('m4',490,690,[[0,0],[70,25]])
arrow('m5',730,650,[[0,0],[70,20]])
arrow('m6',730,715,[[0,0],[70,-20]])
arrow('m7',1080,640,[[0,0],[0,-30],[-435,-30],[-435,-15]],label='확인 결과')
# deploy pipeline
frame('cd',260,820,920,170,'배포 파이프라인 (CodePipeline)')
box('gh',290,870,150,56,'GitHub',GRAY,fs=18)
box('cb',510,870,170,56,'CodeBuild',GRAY,fs=18)
box('cdp',750,870,170,56,'CodeDeploy',LAV,fs=18)
box('tg',990,870,160,56,'FE, BE EC2',GRAY,fs=18)
arrow('d1',440,898,[[0,0],[70,0]])
arrow('d2',680,898,[[0,0],[70,0]])
arrow('d3',920,898,[[0,0],[70,0]],label='배포')
arrow('d4',835,926,[[0,0],[0,40],[235,40],[235,0]],label='실패 시 이전 버전 재배포',dashed=True)
# data pipeline (collect, refine, approve, load)
frame('dp',1250,90,410,440,'데이터 파이프라인')
box('p1',1280,140,200,54,'공공데이터, 엑셀',GRAY,fs=18)
box('p2',1280,250,200,60,'정제 파이프라인\n(L0~L2)',LAV2,LAVF,fs=18)
box('p3',1280,440,200,54,'배포용 묶음',LAV,fs=18)
box('pl',1520,150,110,50,'LLM',GRAY,fs=18)
box('pa',1520,350,110,54,'관리자 화면',YEL,fs=16)
arrow('pd1',1380,194,[[0,0],[0,56]])
arrow('pd2',1380,310,[[0,0],[0,130]])
arrow('pd3',1575,200,[[0,0],[0,65],[-95,65]])
arrow('pd4',1575,350,[[0,0],[0,-55],[-95,-55]],label='승인')
arrow('pd5',1280,467,[[0,0],[-50,0],[-50,88],[-505,88],[-505,33]],label='승인 데이터 반영')
print(json.dumps(E,ensure_ascii=False,separators=(',',':')))
