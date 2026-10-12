import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, Chip} from '../lib/ui';
import {fmt, lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E04.numbers.json';
import T from '../data/M8E04.timing.json';

const EB = 'BAF.60080 · W06 GBI · ④ Floor 만들기';
const H = 630;

/* S0 RB 현금흐름 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const X = (age: number) => 120 + (age - 45) * 38;
  const base = 420;
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E04" title="Retirement Bond는 은퇴 후 실질 고정 소득만 주는 개인의 Floor 자산입니다" sub="RB는 은퇴일부터 소득만 주고 쿠폰도 원금 상환도 없다 — 45세에 사면 65세부터 20년간 실질 연 2,400만 원">
      <svg width={1728} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X(45)} x2={X(86)} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        {[45, 55, 65, 75, 85].map((a) => (
          <text key={a} x={X(a)} y={base + 40} fill={C.muted} fontSize={24} textAnchor="middle">
            {a}세
          </text>
        ))}
        <g opacity={prog(f, cue(0))}>
          <rect x={X(45) - 14} y={base + 50} width={28} height={110 * prog(f, cue(0) + 10)} fill={C.liab} rx={4} />
          <text x={X(45) + 22} y={base + 140} fill={C.liab} fontSize={26} fontWeight={700}>
            매수 −2.64억
          </text>
        </g>
        {Array.from({length: 20}).map((_, i) => {
          const p = prog(f, cue(0) + 30 + i * 3, 10);
          return <rect key={i} x={X(65 + i) - 10} y={base - 120 * p} width={20} height={120 * p} fill={C.floor} rx={3} />;
        })}
        <text x={X(75)} y={base - 140} fill={C.floor} fontSize={30} fontWeight={800} textAnchor="middle" opacity={prog(f, cue(0) + 60)}>
          65세부터 20년 · 실질 연 2,400만
        </text>
        <g opacity={prog(f, cue(1))}>
          <rect x={X(46)} y={base - 60} width={X(64) - X(46)} height={44} rx={22} fill="none" stroke={C.line} strokeWidth={2} strokeDasharray="8 6" />
          <text x={(X(46) + X(64)) / 2} y={base - 30} fill={C.muted} fontSize={26} textAnchor="middle">
            쿠폰 없음 · 원금 상환 없음
          </text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 0, top: 0, display: 'flex', gap: 14, ...rise(f, cue(2))}}>
        <Chip color={C.muted} style={{color: C.text}}>
          Merton SeLFIES (2017)
        </Chip>
        <span style={{fontSize: 34, color: C.accent}}>→</span>
        <Chip color={C.floor}>브라질 RendA+ (2023) 첫 발행</Chip>
      </div>
    </Scene>
  );
};

/* S1 젊을수록 싸다 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const p1 = prog(f, cue(0) + 10, 30);
  const p2 = prog(f, cue(1) + 10, 30);
  const k = 80;
  return (
    <Scene t={t} eyebrow={EB} title="젊을수록 노후 소득의 가격이 쌉니다" sub="원리 — M7 연금현가 공식으로 65세 값을 구하고 다시 45세로 할인 · 연 2,400만 원 × 20년, r = 2%(실질)">
      <div style={{display: 'flex', gap: 60, alignItems: 'flex-end', height: 480, paddingLeft: 80}}>
        {[
          {k: '65세 즉시 시작', v: N.rb65, p: p1, c: C.asset},
          {k: '45세 가입 (20년 후 시작)', v: N.rb45, p: p2, c: C.floor},
        ].map((b) => (
          <div key={b.k} style={{width: 320, textAlign: 'center'}}>
            <div style={{fontSize: 56, fontWeight: 900, color: b.c, opacity: b.p}}>약 {fmt(b.v * b.p, 2)}억</div>
            <div style={{height: b.v * k * b.p, background: b.c, borderRadius: 12, marginTop: 10}} />
            <div style={{fontSize: 28, color: C.muted, marginTop: 12}}>{b.k}</div>
          </div>
        ))}
        <div style={{flex: 1}}>
          <Card style={{...rise(f, cue(0))}}>
            <Tex tex={String.raw`PV_{65} = 0.24 \times \frac{1 - 1.02^{-20}}{0.02} \approx ${fmt(N.rb65, 2)}`} size={36} />
          </Card>
          <Card style={{marginTop: 18, ...rise(f, cue(1))}}>
            <Tex tex={String.raw`PV_{45} = \frac{PV_{65}}{1.02^{20}} = \frac{${fmt(N.rb65, 2)}}{${fmt(N.disc, 3)}} \approx ${fmt(N.rb45, 2)}`} size={36} />
          </Card>
          <div style={{fontSize: 32, fontWeight: 800, color: C.accent, marginTop: 24, transform: `scale(${pop(f, cue(2) + 6)})`, transformOrigin: 'left'}}>
            RB 가격이 곧 Floor — “당신의 Safety 목표는 지금 얼마인가”
          </div>
        </div>
      </div>
    </Scene>
  );
};

/* S2 GHP 복제 · 한국 현실 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="이상적 자산이 없으면 GHP로 복제해 Floor를 만듭니다" sub="EDHEC Retirement Bond Index와 Goal-Hedging Portfolio — 완전한 매칭은 불가능, 충분히 가까운 복제">
      <div style={{display: 'flex', gap: 22, alignItems: 'center', ...rise(f, cue(0))}}>
        {['명목 국채', 'TIPS (물가연동)', '금리 스왑'].map((x, i) => (
          <React.Fragment key={x}>
            <Card style={{flex: 1, textAlign: 'center'}}>
              <div style={{fontSize: 34, fontWeight: 800}}>{x}</div>
            </Card>
            <div style={{fontSize: 40, color: C.accent}}>{i < 2 ? '+' : '='}</div>
          </React.Fragment>
        ))}
        <Card style={{flex: 1.2, textAlign: 'center', border: `3px solid ${C.floor}`}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor}}>GHP ≈ RB</div>
          <div style={{fontSize: 22, color: C.muted}}>D · C · 실질 노출 일치</div>
        </Card>
      </div>
      <div style={{display: 'flex', gap: 30, marginTop: 30}}>
        <Card style={{flex: 1, borderTop: `6px solid ${C.liab}`, ...rise(f, cue(1))}}>
          <div style={{fontSize: 32, fontWeight: 800, color: C.liab}}>한국의 현실 — 재료가 빈약하다</div>
          {['KTBi — 유동성 빈약', '연금식 지급 국채 부재', '초장기물 공급 제약'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 12}}>
              • {x}
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, borderTop: `6px solid ${C.floor}`, ...rise(f, cue(2))}}>
          <div style={{fontSize: 32, fontWeight: 800, color: C.floor}}>발행론 — 부채의 인식</div>
          {['고령화 국가의 공공재', 'NPS가 앵커 수요자', '민간 — 보험 연금 · GHP 복제'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 12}}>
              • {x}
            </div>
          ))}
        </Card>
      </div>
    </Scene>
  );
};

/* S3 Floor는 시장 가격 — 금리 슬라이더 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const curve = N.floor_curve as {r: number; F: number}[];
  const X = (r: number) => 100 + ((r - 0.01) / 0.03) * 900;
  const Y = (v: number) => 560 - ((v - 3.5) / 2.2) * 480;
  const path = curve.map((p, i) => `${i ? 'L' : 'M'} ${X(p.r)} ${Y(p.F)}`).join(' ');
  const s1 = prog(f, cue(1), 40);
  const s2 = prog(f, cue(2), 40);
  const r = s2 > 0 ? lerp(0.025, 0.035, s2) : lerp(0.015, 0.025, s1);
  const Fv = 0.24 * (1 - Math.pow(1 + r, -25)) / r;
  return (
    <Scene t={t} eyebrow={EB} title="Floor는 임의 비율이 아니라 필수 목표를 시장에서 사는 비용입니다" sub="매년 실질 2,400만 원 × 25년 — 실제로 살 수 있는 가격(물가연동국채 금리)으로 잰다">
      <svg width={1100} height={H} style={{position: 'absolute', left: 0, top: 0, opacity: prog(f, cue(0))}}>
        <line x1={100} x2={1000} y1={560} y2={560} stroke={C.muted} strokeWidth={2} />
        {[0.01, 0.02, 0.03, 0.04].map((x) => (
          <text key={x} x={X(x)} y={598} fill={C.muted} fontSize={24} textAnchor="middle">
            {Math.round(x * 100)}%
          </text>
        ))}
        {[4, 5].map((v) => (
          <text key={v} x={88} y={Y(v) + 8} fill={C.muted} fontSize={24} textAnchor="end">
            {v}억
          </text>
        ))}
        <path d={path} fill="none" stroke={C.floor} strokeWidth={5} />
        <circle cx={X(r)} cy={Y(Fv)} r={14} fill={s2 > 0.5 ? C.liab : C.accent} />
        <line x1={X(r)} x2={X(r)} y1={Y(Fv) + 14} y2={560} stroke={C.muted} strokeDasharray="6 6" />
        <text x={1000} y={540} fill={C.muted} fontSize={24} textAnchor="end">
          실질 할인율
        </text>
      </svg>
      <div style={{position: 'absolute', left: 1140, top: 20, width: 588}}>
        <Card style={{textAlign: 'center'}}>
          <div style={{fontSize: 28, color: C.muted}}>할인율 {fmt(r * 100, 1)}%</div>
          <div style={{fontSize: 96, fontWeight: 900, color: s2 > 0.5 ? C.liab : C.floor}}>{fmt(Fv, 2)}억</div>
          <div style={{fontSize: 26, color: C.muted}}>Floor = 필수 목표의 연금현가</div>
        </Card>
        <Card style={{marginTop: 20, borderLeft: `6px solid ${C.liab}`, ...rise(f, cue(2) + 30)}}>
          <div style={{fontSize: 28, fontWeight: 800, color: C.liab}}>낙관 할인율의 함정</div>
          <div style={{fontSize: 26, marginTop: 6}}>쿠션이 커 보여 위험을 더 산다 — M7과 같은 문제</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S4 이순자 씨 네 걸음 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const steps = [
    {k: '① 이상', v: '평생 소득 채권(RB)을 산다'},
    {k: '② 복제', v: '없으니 국채로 복제한다 (GHP)'},
    {k: '③ 가격', v: '복제 비용 3.50억이 Floor'},
    {k: '④ 운용', v: '남는 1.50억만 위험을 진다'},
  ];
  const pF = prog(f, cue(1) + 10, 30);
  const pC = prog(f, cue(2) + 10, 30);
  return (
    <Scene t={t} eyebrow={EB} title="필수 소득을 지키는 길은 ‘이상 → 복제 → 가격 → 운용’ 네 걸음입니다" sub="이순자 씨는 국민연금 외에 매달 150만 원이 평생 더 필요하다 — 금융자산 5억">
      <div style={{display: 'flex', gap: 12, alignItems: 'center'}}>
        {steps.map((s, i) => (
          <React.Fragment key={s.k}>
            <Card style={{flex: 1, ...rise(f, cue(0) + 10 + i * 14)}}>
              <div style={{fontSize: 32, fontWeight: 800, color: C.accent}}>{s.k}</div>
              <div style={{fontSize: 26, marginTop: 6}}>{s.v}</div>
            </Card>
            {i < 3 ? <div style={{fontSize: 34, color: C.accent}}>→</div> : null}
          </React.Fragment>
        ))}
      </div>
      <div style={{display: 'flex', height: 140, marginTop: 40, borderRadius: 14, overflow: 'hidden', border: `2px solid ${C.line}`}}>
        <div style={{width: `${70 * pF}%`, background: C.floor, display: 'flex', alignItems: 'center', paddingLeft: 30, fontSize: 40, fontWeight: 900, color: C.bg}}>
          {pF > 0.5 ? 'Floor 3.50억 (GHP)' : ''}
        </div>
        <div style={{width: `${30 * pC}%`, background: C.accent, display: 'flex', alignItems: 'center', paddingLeft: 24, fontSize: 36, fontWeight: 900, color: C.bg}}>
          {pC > 0.5 ? '쿠션 1.50억' : ''}
        </div>
      </div>
      <div style={{fontSize: 26, color: C.muted, marginTop: 12, ...rise(f, cue(1) + 30)}}>
        (월 300만 − NPS 150만) × 12 × 23년 현가(실질 1.5%) ≈ 3.50억
      </div>
    </Scene>
  );
};

/* S5 Martellini–Milhau 10년 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const ev = [
    ['2012', 'Retirement Bond 개념 — 개인 Floor의 도입'],
    ['2013', 'Retirement Bond Index 방법론 (복제 공식 공개)'],
    ['2015', '“A Framework for Goal-Based Investing” — 전체 연쇄 완성'],
    ['2018', 'EDHEC “Flexicure” GBI 은퇴 솔루션 제안'],
    ['2020', '“Advances in Retirement Investing” · COVID 급락에 규칙 기반 방어'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="Martellini와 Milhau는 10년에 걸쳐 TDF와 DB LDI 사이에 새 길을 냈습니다" sub="에피소드 — TDF는 단순하고 DB의 LDI는 개인에 맞지 않는다">
      {ev.map((e, i) => (
        <div key={e[0]} style={{display: 'flex', alignItems: 'center', gap: 28, marginBottom: 22, ...rise(f, (i < 4 ? cue(0) : cue(1)) + (i % 4) * 16)}}>
          <div style={{width: 120, fontSize: 42, fontWeight: 900, color: i === 4 ? C.floor : C.accent}}>{e[0]}</div>
          <div style={{width: 18, height: 18, borderRadius: 9, background: i === 4 ? C.floor : C.accent}} />
          <div style={{fontSize: 32}}>{e[1]}</div>
        </div>
      ))}
      <div style={{fontSize: 34, fontWeight: 800, color: C.floor, marginTop: 10, ...rise(f, cue(1) + 40)}}>큰 이론은 10년이 걸리고, 위기가 이론을 검증한다 — 예측 없이도 보호</div>
    </Scene>
  );
};

export const M8E04 = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M8E04_TOTAL = T.total;
