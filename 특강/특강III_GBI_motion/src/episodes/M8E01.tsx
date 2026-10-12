import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, Chip} from '../lib/ui';
import {pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E03a.numbers.json';
import T from '../data/M8E01.timing.json';

const EB = 'BAF.60080 · W06 GBI · ① 목표와 위험';
const H = 630;

/* S0 σ 12%는 답이 아니다 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const strike = prog(f, cue(0) + 50, 20);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E01" title="GBI는 목표를 정의하고 우선순위를 정한 뒤 확률로 위험을 봅니다" sub="변동성 12%라는 숫자는 목표 달성 여부를 말해 주지 않는다">
      <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 60, marginTop: 30}}>
        <Card style={{width: 520, textAlign: 'center', position: 'relative', ...rise(f, cue(0))}}>
          <div style={{fontSize: 32, color: C.muted}}>포트폴리오 위험</div>
          <div style={{fontSize: 130, fontWeight: 900, color: C.muted}}>σ 12%</div>
          <div style={{position: 'absolute', left: 40, right: 40, top: '55%', height: 8, background: C.liab, transform: `scaleX(${strike})`, transformOrigin: 'left'}} />
        </Card>
        <div style={{fontSize: 80, color: C.accent, opacity: prog(f, cue(1))}}>→</div>
        <Card style={{width: 620, textAlign: 'center', border: `3px solid ${C.floor}`, transform: `scale(${pop(f, cue(1) + 10)})`}}>
          <div style={{fontSize: 32, color: C.muted}}>목표 위험</div>
          <div style={{fontSize: 64, fontWeight: 900, color: C.floor, marginTop: 10}}>“Safety 실패 확률 3%”</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S1 3원칙 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cols = [
    {k: '① 목표 정의', s: '무엇을 이룰지', items: ['금액 — 얼마나', '시점 — 언제', '우선순위 — 얼마나 중요'], tag: '목표 없이 배분 없다', c: C.asset},
    {k: '② 우선순위 (3계층)', s: '위계가 있다', items: ['Safety ≥ 95%', 'Market ≥ 70%', 'Aspirational ≥ 30%'], tag: 'Safety 먼저, 꿈은 그다음', c: C.floor},
    {k: '③ 확률 기반 배분', s: '위험 = 미달 확률', items: ['Safety 미달 < 5%', 'Market 미달 < 30%', 'Aspirational 미달 < 70%'], tag: 'σ 12%는 답이 아니다', c: C.accent},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="GBI의 3대 원칙은 목표 정의 · 우선순위 · 확률입니다" sub="기본 지식 — 무엇을, 어떤 순서로, 어떤 확률로">
      <div style={{display: 'flex', gap: 28}}>
        {cols.map((c, i) => (
          <Card key={c.k} style={{flex: 1, borderTop: `6px solid ${c.c}`, ...rise(f, cue(i))}}>
            <div style={{fontSize: 36, fontWeight: 800, color: c.c}}>{c.k}</div>
            <div style={{fontSize: 26, color: C.muted}}>{c.s}</div>
            {c.items.map((x) => (
              <div key={x} style={{fontSize: 30, marginTop: 14}}>
                • {x}
              </div>
            ))}
            <div style={{fontSize: 28, fontWeight: 700, color: c.c, marginTop: 20}}>{c.tag}</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

/* S2 세 비유 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const m = [
    {k: '버킷 = 통장 쪼개기', v: '생활비 통장 · 여행 적금 — 모두가 이미 하고 있다'},
    {k: '위험 = 지각할 확률', v: '얼마나 흔들리느냐가 아니라 늦을 확률이 중요하다'},
    {k: '우선순위 = 밥 · 반찬 · 디저트', v: '밥(Safety)이 먼저, 디저트는 여유가 있을 때'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="목표는 세 가지 비유로 읽을 수 있습니다" sub="단원 ②·③의 수식은 이 비유의 정밀한 번역이다">
      <div style={{display: 'flex', gap: 28}}>
        {m.map((x, i) => (
          <Card key={x.k} style={{flex: 1, border: i === 1 && f > cue(1) ? `3px solid ${C.accent}` : undefined, ...rise(f, cue(0) + i * 24)}}>
            <div style={{fontSize: 36, fontWeight: 800, color: C.accent}}>{x.k}</div>
            <div style={{fontSize: 29, color: C.muted, marginTop: 14}}>{x.v}</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

/* S3 미달 확률 그림 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const xs = N.xs as number[];
  const d = (N.dens as number[][])[2];
  const X = (x: number) => 80 + (x / 7.2) * 1000;
  const maxd = Math.max(...d);
  const Y = (v: number) => 540 - (v / maxd) * 420;
  const draw = prog(f, cue(0) + 10, 40);
  const nShow = Math.round(xs.length * draw);
  const line = xs.slice(0, nShow).map((x, i) => `${i ? 'L' : 'M'} ${X(x)} ${Y(d[i])}`).join(' ');
  const G = 3.0;
  const below = xs.map((x, i) => [x, d[i]] as const).filter(([x]) => x <= G);
  const area = `M ${X(below[0][0])} 540 ` + below.map(([x, v]) => `L ${X(x)} ${Y(v)}`).join(' ') + ` L ${X(G)} 540 Z`;
  const pA = prog(f, cue(0) + 60, 24);
  return (
    <Scene t={t} eyebrow={EB} title="GBI는 위험을 목표 미달 확률과 그 깊이로 측정합니다" sub="예시 — Market 계좌: 오늘 2.24억 · 주식 67% · 10년 뒤 목표 G = 3억">
      <svg width={1150} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={80} x2={1100} y1={540} y2={540} stroke={C.muted} strokeWidth={2} />
        {[0, 2, 4, 6].map((v) => (
          <text key={v} x={X(v)} y={580} fill={C.muted} fontSize={24} textAnchor="middle">
            {v}억
          </text>
        ))}
        <text x={1100} y={520} fill={C.muted} fontSize={24} textAnchor="end">
          10년 뒤 자산 W_T
        </text>
        <path d={area} fill={C.liab} opacity={0.35 * pA} />
        <path d={line} fill="none" stroke={C.asset} strokeWidth={5} />
        <line x1={X(G)} x2={X(G)} y1={90} y2={540} stroke={C.floor} strokeWidth={4} strokeDasharray="10 8" opacity={prog(f, cue(0) + 40)} />
        <text x={X(G) + 12} y={110} fill={C.floor} fontSize={30} fontWeight={800} opacity={prog(f, cue(0) + 40)}>
          목표 G = 3억
        </text>
        <text x={X(1.9)} y={470} fill={C.liab} fontSize={40} fontWeight={900} textAnchor="middle" opacity={pA}>
          30%
        </text>
      </svg>
      <div style={{position: 'absolute', left: 1180, top: 0, width: 548}}>
        <Card style={{...rise(f, cue(0))}}>
          <div style={{fontSize: 26, color: C.muted}}>목표 미달 확률</div>
          <Tex tex={String.raw`P(W_T < G)`} size={50} />
        </Card>
        <Card style={{marginTop: 20, ...rise(f, cue(1))}}>
          <div style={{fontSize: 26, color: C.muted}}>깊이 — 기대 부족분</div>
          <Tex tex={String.raw`\mathbb{E}[\,G - W_T \mid W_T < G\,]`} size={40} />
        </Card>
        <div style={{fontSize: 30, fontWeight: 800, color: C.accent, marginTop: 24, ...rise(f, cue(2))}}>
          실무는 몬테카를로 — 경로별 최종 자산을 세어 P(W &lt; G)
        </div>
      </div>
    </Scene>
  );
};

/* S4 95 · 70 · 30 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const tiers = [
    {k: 'Aspirational', p: 0.3, s: '10번 중 3번만 돼도', use: '상속 · 꿈', asset: '주식 · 대체', c: C.accent},
    {k: 'Market', p: 0.7, s: '10번 중 7번 이상', use: '여유 생활', asset: 'GHP + 주식 (약 67%)', c: C.asset},
    {k: 'Safety', p: 0.95, s: '20번 중 19번 이상', use: '필수 생활비', asset: 'GHP (물가연동국채 사다리)', c: C.floor},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="95 · 70 · 30은 배분 비중이 아니라 달성 확률입니다" sub="배분 금액은 이 확률 조건에서 거꾸로 계산해 나온다">
      {tiers.map((x, i) => {
        const at = cue(1) + (2 - i) * 22;
        const pp = prog(f, at + 10, 30);
        return (
          <Card key={x.k} style={{display: 'flex', alignItems: 'center', gap: 30, marginBottom: 18, borderLeft: `8px solid ${x.c}`, ...rise(f, at)}}>
            <div style={{width: 260}}>
              <div style={{fontSize: 36, fontWeight: 800, color: x.c}}>{x.k}</div>
              <div style={{fontSize: 26, color: C.muted}}>{x.use}</div>
            </div>
            <div style={{flex: 1}}>
              <div style={{height: 40, background: C.bg2, borderRadius: 10, position: 'relative'}}>
                <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${x.p * pp * 100}%`, background: x.c, borderRadius: 10}} />
              </div>
              <div style={{fontSize: 24, color: C.muted, marginTop: 6}}>{x.s}</div>
            </div>
            <div style={{width: 140, fontSize: 52, fontWeight: 900, color: x.c}}>≥{Math.round(x.p * 100 * pp)}%</div>
            <div style={{width: 380, fontSize: 26}}>{x.asset}</div>
          </Card>
        );
      })}
      <div style={{display: 'flex', gap: 16, marginTop: 8, ...rise(f, cue(2))}}>
        <Chip color={C.accent}>비중은 입력이 아니라 계산 결과</Chip>
      </div>
    </Scene>
  );
};

export const M8E01 = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M8E01_TOTAL = T.total;
