import cairosvg
F='font-family="Noto Sans CJK KR, Noto Sans CJK JP"'
W,H=1400,1540
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs><marker id="a" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#2E5BAA"/></marker></defs><rect width="{W}" height="{H}" fill="#fff"/>']
def box(x,y,w,h,title,lines,fill="#EAF1FB",tc="#1B2C5E",bc="#3B4252",stroke="#D6D6DB",tag=None):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    if tag: s.append(f'<text x="{x+18}" y="{y+34}" font-size="22" font-weight="700" fill="#2E5BAA" {F}>{tag}</text>')
    s.append(f'<text x="{x+w/2}" y="{y+(46 if not tag else 50)}" text-anchor="middle" font-size="30" font-weight="700" fill="{tc}" {F}>{title}</text>')
    for k,l in enumerate(lines):
        s.append(f'<text x="{x+w/2}" y="{y+(92 if not tag else 96)+k*38}" text-anchor="middle" font-size="25" fill="{bc}" {F}>{l}</text>')
def arr(x1,y1,x2,y2,label=None,lx=None,ly=None):
    s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2E5BAA" stroke-width="4" marker-end="url(#a)"/>')
    if label: s.append(f'<text x="{lx}" y="{ly}" font-size="25" font-weight="700" fill="#2E5BAA" {F}>{label}</text>')
# 1 입력
box(60,30,860,170,"입력",["계좌 잔액 · 자산(가격 상승률, 분배율, 변동성)","투자 기간 · 연금 인출세율 · ISA 유형"],tag="①")
box(980,30,360,170,"세법 모듈",["tax_rules_2026.py","세율 · 공제 · 한도"],fill="#F4F5F9",tag="⓪")
arr(980,115,925,115)
arr(490,200,490,250)
# 2 계수
box(60,250,1280,300,"1원당 세후 계수 계산",[],tag="②")
for k,(t,ls) in enumerate([("일반계좌",["분배금 매년 15.4%","매도 시 차익 과세","(국내주식형 ETF 비과세)"]),("ISA",["운용 중 비과세","끝에 (순이익 − 한도)","× 9.9%"]),("연금저축 · IRP",["운용 중 비과세","끝에 잔액 × (1 − 인출세율)","세후 지분 = 1 − 인출세율"])]):
    x=100+k*405
    s.append(f'<rect x="{x}" y="320" width="380" height="200" rx="12" fill="#fff" stroke="#D6D6DB" stroke-width="2"/>')
    s.append(f'<text x="{x+190}" y="362" text-anchor="middle" font-size="27" font-weight="700" fill="#2E5BAA" {F}>{t}</text>')
    for j,l in enumerate(ls): s.append(f'<text x="{x+190}" y="{405+j*36}" text-anchor="middle" font-size="24" fill="#3B4252" {F}>{l}</text>')
arr(700,550,700,600)
# 3 결정
cx,cy=700,690
s.append(f'<polygon points="{cx},{cy-90} {cx+330},{cy} {cx},{cy+90} {cx-330},{cy}" fill="#FCF2E0" stroke="#C77700" stroke-width="3"/>')
s.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="29" font-weight="700" fill="#1B2C5E" {F}>목표 배분이</text>')
s.append(f'<text x="{cx}" y="{cy+32}" text-anchor="middle" font-size="29" font-weight="700" fill="#1B2C5E" {F}>정해져 있나?</text>')
s.append(f'<polyline points="{cx-330},{cy} 250,{cy} 250,826" fill="none" stroke="#2E5BAA" stroke-width="4" marker-end="url(#a)"/>')
s.append(f'<polyline points="{cx+330},{cy} 1150,{cy} 1150,826" fill="none" stroke="#2E5BAA" stroke-width="4" marker-end="url(#a)"/>')
s.append(f'<text x="270" y="{cy+60}" font-size="27" font-weight="700" fill="#C77700" {F}>예</text>')
s.append(f'<text x="1170" y="{cy+60}" font-size="27" font-weight="700" fill="#C77700" {F}>아니오</text>')
# 4a LP
box(60,830,620,250,"배치 선형계획(LP)",["세후 가치 − 세금을 최대화","제약: 계좌 잔액 · 목표 배분","IRP 70% · 해외 양도세 · ISA 세금","결과: 최적 배치 x*, 쌍대가격 λ"],tag="③")
arr(370,1080,370,1126)
box(60,1130,620,150,"계좌별 한계가치",["Z = λ계좌 ÷ λ일반","(세후 비중 목표일 때)"],fill="#E6F5F0",tag="④")
# 4b QP
box(720,830,620,250,"배분·배치 공동 2차계획(QP)",["세후 가치 − 세금 − 위험 벌점","위험 = 세후 노출의 분산","위험회피 계수 γ 선택","결과: 배분 + 배치"],tag="③′")
arr(1030,1080,1030,1126)
box(720,1130,620,150,"γ를 바꿔 프런티어",["배분이 바뀔 때","배치가 어떻게 따라 바뀌나"],fill="#E6F5F0",tag="④′")
# 5 평가
arr(370,1280,600,1336); arr(1030,1280,800,1336)
box(260,1340,880,170,"평가 · 비교 · 리포트",["기준 전략(같은 비중 · 채권 우선 · 해외주식 우선)과 비교","민감도(인출세율 · 투자 기간) → results.md · 차트"],fill="#1B2C5E",tc="#FFFFFF",bc="#CADCFC",stroke="#1B2C5E",tag=None)
s.append('</svg>')
cairosvg.svg2png(bytestring="".join(s).encode(),write_to="flowchart.png")
