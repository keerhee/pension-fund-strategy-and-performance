#!/usr/bin/env python3
"""factor_lab.py — BAF.60080 W02·W10·W12 실습 공용 계산 도구
데이터: KAIST BAF634(2025) Problem_Set_2.xls 를 CSV로 옮긴 것 (Kenneth French Data Library 원자료, 월간 %, 1926-07 ~ 2015).
사용 예:
  python3 factor_lab.py summary --set ind30                  # 평균·표준편차·샤프
  python3 factor_lab.py grs --set ind30 --model capm         # 시계열 회귀 + GRS
  python3 factor_lab.py grs --set sb25 --model ff3 --start 196307
  python3 factor_lab.py factors                              # SMB·HML·UMD 만들기와 프리미엄 t값
  python3 factor_lab.py rolling --factor HML --window 120    # 10년 롤링 프리미엄
  python3 factor_lab.py combo --w HML=0.5,UMD=0.5            # 팩터 결합 성과
  python3 factor_lab.py manager --port S1B5 --start 196307    # 가상 운용사의 CAPM·FF3 알파
  python3 factor_lab.py jkp --country kor                     # data/factors/ 의 JKP 팩터(미국·한국) 요약
  python3 factor_lab.py jkp --country usa --start 201508      # 미국 표본 밖(2015.08~)
"""
import argparse, os, numpy as np, pandas as pd
from scipy import stats
H=os.path.dirname(os.path.abspath(__file__))
def rd(n): return pd.read_csv(os.path.join(H,f'baf_{n}.csv'),index_col=0,dtype={'yyyymm':str})
SETS={'ind30':'ind30_vw','mom10':'mom10','sb25':'size_bm25'}

def load(start=None,end=None):
    mk=rd('mkt_rf'); sb=rd('size_bm25'); mo=rd('mom10')
    S=[c for c in sb if c.startswith('S1')]; B=[c for c in sb if c.startswith('S5')]
    L=[c for c in sb if c.endswith('B1')]; Hh=[c for c in sb if c.endswith('B5')]
    f=pd.DataFrame(index=mk.index)
    f['MKT_RF']=mk.MKT_RF; f['RF']=mk.RF
    f['SMB']=sb[S].mean(axis=1)-sb[B].mean(axis=1)          # 5×5에서 소형 행 평균 − 대형 행 평균
    f['HML']=sb[Hh].mean(axis=1)-sb[L].mean(axis=1)          # 고 BE/ME 열 평균 − 저 BE/ME 열 평균
    f['UMD']=mo['D10_Winner']-mo['D01_Loser']      # 승자 십분위 − 패자 십분위
    if start: f=f[f.index>=str(start)]
    if end: f=f[f.index<=str(end)]
    return f

def excess(setname,f):
    r=rd(SETS[setname]).reindex(f.index)
    return r.sub(f.RF,axis=0)                       # 원자료는 총수익률 → 초과수익률

MODELS={'capm':['MKT_RF'],'ff3':['MKT_RF','SMB','HML'],'ff3mom':['MKT_RF','SMB','HML','UMD'],'mom':['MKT_RF','UMD']}

def grs(R,F):
    d=pd.concat([R,F],axis=1).dropna(); R=d[R.columns].values; F=d[F.columns].values
    T,N=R.shape; K=F.shape[1]
    X=np.column_stack([np.ones(T),F]); B=np.linalg.lstsq(X,R,rcond=None)[0]
    E=R-X@B; a=B[0]; Sig=E.T@E/(T-K-1)
    mu=F.mean(0); Om=np.atleast_2d(np.cov(F.T,ddof=1))
    q=a@np.linalg.solve(Sig,a); sh2=mu@np.linalg.solve(Om,mu)
    G=(T-N-K)/N*q/(1+sh2); p=1-stats.f.cdf(G,N,T-N-K)
    se=np.sqrt(np.diag(Sig)*np.linalg.inv(X.T@X)[0,0])
    r2=1-E.var(0)/R.var(0)
    return dict(T=T,N=N,K=K,alpha=a,t=a/se,beta=B[1:].T,first=d.index[0],last=d.index[-1],r2=r2,GRS=G,p=p,
                mean_abs_alpha=np.abs(a).mean(),sh_f=np.sqrt(sh2)*np.sqrt(12),
                sh_tan=np.sqrt(sh2+q)*np.sqrt(12))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',choices=['summary','grs','factors','rolling','combo','manager','jkp'])
    ap.add_argument('--set',default='ind30',choices=list(SETS)); ap.add_argument('--model',default='capm',choices=list(MODELS))
    ap.add_argument('--start'); ap.add_argument('--end'); ap.add_argument('--factor',default='HML'); ap.add_argument('--window',type=int,default=120)
    ap.add_argument('--w',default='HML=0.5,UMD=0.5'); ap.add_argument('--port',default='S1B5'); ap.add_argument('--file'); ap.add_argument('--country',choices=['usa','kor']); ap.add_argument('--weighting',default='vw_cap',choices=['ew','vw','vw_cap']); ap.add_argument('--factors',default='be_me,ret_12_1,market_equity')
    a=ap.parse_args(); f=load(a.start,a.end); pd.set_option('display.width',200)
    if a.cmd=='summary':
        R=excess(a.set,f).dropna(how='all'); s=pd.DataFrame({'mean%':R.mean(),'sd%':R.std(),'sharpe_ann':R.mean()/R.std()*np.sqrt(12)})
        print(f'[{a.set}] {R.index[0]}~{R.index[-1]}  T={len(R)}  (월간 초과수익률 %)'); print(s.round(3).to_string())
        print(f'\n평균–표준편차 상관 {np.corrcoef(s["mean%"],s["sd%"])[0,1]:.3f} · 샤프 범위 {s.sharpe_ann.min():.2f}~{s.sharpe_ann.max():.2f}')
    elif a.cmd=='grs':
        cols=MODELS[a.model]; R=excess(a.set,f); g=grs(R,f[cols])
        print(f'[{a.set} · {a.model}] T={g["T"]} N={g["N"]} K={g["K"]}  기간 {g["first"]}~{g["last"]}')
        t=pd.DataFrame({'alpha%':g['alpha'],'t(alpha)':g['t'],'R2':g['r2']},index=R.columns)
        for i,c in enumerate(cols): t['b_'+c]=g['beta'][:,i]
        print(t.round(3).to_string())
        print(f'\nGRS F = {g["GRS"]:.3f}  p = {g["p"]:.4f}   평균 |alpha| = {g["mean_abs_alpha"]:.3f}%/월')
        print(f'팩터 조합의 최대 샤프(연) = {g["sh_f"]:.3f} · 시험자산까지 쓴 접점 샤프(연) = {g["sh_tan"]:.3f}')
        print(f'|t|>=2 인 포트폴리오 {int((np.abs(g["t"])>=2).sum())}개 / {g["N"]}')
    elif a.cmd=='factors':
        F=f[['MKT_RF','SMB','HML','UMD']].dropna(); m=F.mean(); s=F.std(); T=len(F)
        out=pd.DataFrame({'mean%/월':m,'sd%/월':s,'t':m/s*np.sqrt(T),'sharpe_ann':m/s*np.sqrt(12),'min%':F.min()})
        print(f'팩터 프리미엄 {F.index[0]}~{F.index[-1]} T={T}'); print(out.round(3).to_string())
        print('\n상관행렬'); print(F.corr().round(2).to_string())
    elif a.cmd=='rolling':
        x=f[a.factor].dropna(); r=x.rolling(a.window).mean()*12; tt=x.rolling(a.window).mean()/x.rolling(a.window).std()*np.sqrt(a.window)
        o=pd.DataFrame({'ann_mean%':r,'t':tt}).dropna(); print(o.iloc[::12].round(2).to_string())
        neg=(o["ann_mean%"]<0).mean()
        print(f'\n{a.window}개월 롤링 연 프리미엄이 음(−)인 달의 비율 {neg:.1%} · 최저 {o["ann_mean%"].min():.2f}% ({o["ann_mean%"].idxmin()} 끝 구간) · 최근 {o["ann_mean%"].iloc[-1]:.2f}%')
    elif a.cmd=='combo':
        w={k:float(v) for k,v in (p.split('=') for p in a.w.split(','))}
        F=f[list(w)].dropna(); p=sum(F[k]*v for k,v in w.items())
        def st(x):
            c=(1+x/100).cumprod(); dd=(c/c.cummax()-1).min()
            w12=((1+x/100).rolling(12).apply(np.prod,raw=True)-1)*100   # 12개월 복리 수익률
            return pd.Series({'mean%/월':x.mean(),'sd%/월':x.std(),'sharpe_ann':x.mean()/x.std()*np.sqrt(12),'MDD%':dd*100,'worst_12m%':w12.min()})
        o=pd.DataFrame({**{k:st(F[k]) for k in w},'COMBO':st(p)}).T
        print(f'결합 {w}  {F.index[0]}~{F.index[-1]}'); print(o.round(2).to_string()); print(f'\n상관 {F.corr().round(2).values[0,1:] if len(w)>1 else "-"}')
    elif a.cmd=='manager':
        R=excess('sb25',f)[[a.port]]
        print(f'가상 위탁운용사 = 25개 포트폴리오 중 {a.port} (초과수익률)')
        for m in ['capm','ff3','ff3mom']:
            g=grs(R,f[MODELS[m]]); b=' '.join(f'{c}={v:.2f}' for c,v in zip(MODELS[m],g['beta'][0]))
            print(f'  {m:7s} T={g["T"]}  alpha={g["alpha"][0]:.3f}%/월 (연 {g["alpha"][0]*12:.2f}%)  t={g["t"][0]:.2f}  R2={g["r2"][0]:.3f}  {b}')
    elif a.cmd=='jkp':
        if not a.file:
            if not a.country: print('--file 또는 --country(usa|kor) 를 준다'); return
            a.file=os.path.join(H,'data','factors',f'[{a.country}]_[all_factors]_[monthly]_[{a.weighting}].csv')
        if not os.path.exists(a.file):
            print(f'파일이 없다: {a.file}\nBAF634 강의 데이터를 내려받아 이 폴더 아래 data/ 에 넣는다 (DATA.md 참고):\nhttps://drive.google.com/drive/folders/1vRVfhTRU7YsaT1ndiqTEkxfSEfVIioVZ?usp=sharing'); return
        d=pd.read_csv(a.file); d.columns=[c.lower() for c in d.columns]
        if 'location' in d and d['location'].nunique()>1: print('location 열에 여러 국가가 있음:',d['location'].unique()[:10])
        d['date']=pd.to_datetime(d['date']); dall=d.copy(); d=d[d['date']>=pd.Timestamp(a.start[:4]+'-'+a.start[4:]+'-01')] if a.start else d
        if 'weighting' in d and d['weighting'].nunique()>1: print('weighting 열에 여러 가중 방식:',d['weighting'].unique(),'→ 한 가지만 남긴 파일을 쓴다'); return
        if 'direction' in d: print('direction(부호):',d.groupby('name')['direction'].first().reindex(a.factors.split(',')).to_dict())
        W=d.pivot_table(index='date',columns='name',values='ret')*100   # JKP는 소수 → %
        names=[x for x in a.factors.split(',') if x in W]
        miss=[x for x in a.factors.split(',') if x not in W]
        if miss: print('파일에 없는 팩터:',miss)
        X=W[names].dropna(how='all'); out=[]
        for c in names:
            x=X[c].dropna(); c12=((1+x/100).rolling(12).apply(np.prod,raw=True)-1)*100; cum=(1+x/100).cumprod()
            out.append(dict(factor=c,first=x.index[0].strftime('%Y-%m'),last=x.index[-1].strftime('%Y-%m'),T=len(x),**{'mean%/월':x.mean(),'t':x.mean()/x.std()*np.sqrt(len(x)),'sharpe_ann':x.mean()/x.std()*np.sqrt(12),'MDD%':(cum/cum.cummax()-1).min()*100,'worst_12m%':c12.min()}))
        print(pd.DataFrame(out).set_index('factor').round(2).to_string())
        if len(names)>1: print('\n상관'); print(X[names].corr().round(2).to_string())
        # 이 과제의 미국 1926~2015 팩터와 겹치는 기간의 상관 (부호 확인용 — 미국 파일일 때 의미가 있다)
        MAP={'be_me':'HML','ret_12_1':'UMD','market_equity':'SMB'}
        ours=load(); ours.index=pd.PeriodIndex(ours.index,freq='M')
        Y=dall.pivot_table(index='date',columns='name',values='ret')*100; Y.index=Y.index.to_period('M'); rows=[]
        for c in [x for x in a.factors.split(',') if x in Y]:
            if c in MAP:
                j=pd.concat([Y[c],ours[MAP[c]]],axis=1).dropna()
                if len(j)>=24: rows.append(f'{c} vs {MAP[c]}: 겹치는 {len(j)}개월 상관 {j.corr().iloc[0,1]:.2f}')
        if rows: print('\n부호 확인 (이 과제의 1926~2015 팩터와 겹치는 전 기간, --start 와 무관)'); print('\n'.join(rows))
if __name__=='__main__': main()
