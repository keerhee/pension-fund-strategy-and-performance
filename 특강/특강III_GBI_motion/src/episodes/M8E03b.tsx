import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, RevealTable} from '../lib/ui';
import {fmt, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E03b.numbers.json';
import T from '../data/M8E03b.timing.json';

const EB = 'BAF.60080 · W06 GBI · ③ 필요 자본 · 방법 2 Das–Markowitz';
const H = 630;
const AC = [C.floor, C.asset, C.accent];
const GL = ['3.795', '2.706', '0.877']; // 강의본 표기

/* 평균-분산 평면 */
const Plane: React.FC<{f: number; at: number; acc: number; agg?: number; lines?: number}> = ({f, at, acc, agg = -1, lines = -1}) => {
  const X = (s: number) => 90 + (s / 0.55) * 900;
  const Y = (m: number) => 560 - (m / 0.3) * 500;
  const fr = N.frontier.filter((p) => p.s < 0.55 && p.m < 0.3);
  const draw = prog(f, at, 40);
  const n = Math.max(2, Math.round(fr.length * draw));
  const path = fr.slice(0, n).map((p, i) => `${i ? 'L' : 'M'} ${X(p.s)} ${Y(p.m)}`).join(' ');
  return (
    <svg width={1050} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <line x1={90} x2={1000} y1={560} y2={560} stroke={C.muted} strokeWidth={2} />
      <line x1={90} x2={90} y1={40} y2={560} stroke={C.muted} strokeWidth={2} />
      {[0.1, 0.2, 0.3, 0.4, 0.5].map((s) => (
        <text key={s} x={X(s)} y={598} fill={C.muted} fontSize={22} textAnchor="middle">
          {Math.round(s * 100)}%
        </text>
      ))}
      {[0.1, 0.2].map((m) => (
        <text key={m} x={78} y={Y(m) + 8} fill={C.muted} fontSize={22} textAnchor="end">
          {Math.round(m * 100)}%
        </text>
      ))}
      <text x={1000} y={545} fill={C.muted} fontSize={22} textAnchor="end">
        표준편차 σ
      </text>
      <text x={100} y={50} fill={C.muted} fontSize={22}>
        기대수익 μ
      </text>
      <path d={path} fill="none" stroke={C.text} strokeWidth={4} />
      {N.assets.map((a, i) => (
        <g key={a.k} opacity={prog(f, at - 20 + i * 8)}>
          <circle cx={X(a.s)} cy={Y(a.m)} r={10} fill={C.muted} />
          <text x={X(a.s) + 14} y={Y(a.m) + 30} fill={C.muted} fontSize={22}>
            {a.k}
          </text>
        </g>
      ))}
      {N.accounts.map((a, i) => {
        if (i > acc) return null;
        const p = prog(f, at + 40 + i * 30, 20);
        const H_ = a.H;
        // 제약선 μ = H + zσ
        return (
          <g key={a.name} opacity={p}>
            {lines >= i ? (
              <line x1={X(0)} y1={Y(H_)} x2={X(0.55)} y2={Y(H_ + a.z * 0.55)} stroke={AC[i]} strokeWidth={2} strokeDasharray="8 6" />
            ) : null}
            <circle cx={X(a.s)} cy={Y(a.m)} r={14 * pop(f, at + 40 + i * 30)} fill={AC[i]} />
            <text x={X(a.s) + (i === 0 ? 18 : -16)} y={Y(a.m) + (i === 0 ? 40 : -18)} fill={AC[i]} fontSize={26} fontWeight={800} textAnchor={i === 0 ? 'start' : 'end'}>
              {a.name} γ {GL[i]}
            </text>
          </g>
        );
      })}
      {agg >= 0 ? (
        <g opacity={prog(f, agg)}>
          <rect x={X(N.agg.s) - 13} y={Y(N.agg.m) - 13} width={26} height={26} transform={`rotate(45 ${X(N.agg.s)} ${Y(N.agg.m)})`} fill={C.text} />
          <text x={X(N.agg.s) + 22} y={Y(N.agg.m) + 36} fill={C.text} fontSize={26} fontWeight={800}>
            합산 γ {fmt(N.agg.gamma, 3)}
          </text>
        </g>
      ) : null}
    </svg>
  );
};

/* S0 문제 설정 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E03b" title="방법 2 — Das–Markowitz는 (H, α)를 평균-분산 조건으로 바꿔 풉니다" sub="H 최소 수익률 · α 미달 확률 한도 · 원 논문(2010)의 가상 자산 셋">
      <Card style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`\max_w\; \mu_p \quad \text{s.t.}\quad P(R_p < H) \le \alpha \;\;\overset{\text{정규}}{\Longleftrightarrow}\;\; \mu_p - z_\alpha\,\sigma_p \ge H`} size={48} />
      </Card>
      <div style={{width: 1728, marginTop: 26}}>
        <RevealTable
          f={f}
          size={30}
          cols={['자산 (원 논문의 가상 자산)', '기대수익률 · 표준편차', '상관']}
          widths={[1.2, 1, 1.4]}
          rows={[
            {cells: ['채권형', '5% · 5%', '두 주식형과 0'], at: cue(2)},
            {cells: ['저위험 주식형', '10% · 20%', '고위험 주식형과 0.20 (공분산 0.02)'], at: cue(2) + 14},
            {cells: ['고위험 주식형', '25% · 50%', '저위험 주식형과 0.20'], at: cue(2) + 28},
          ]}
        />
      </div>
    </Scene>
  );
};

/* S1 손계산 ① 검사 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const m = N.check.m;
  const s = N.check.s;
  return (
    <Scene t={t} eyebrow={EB} title="포트폴리오 하나가 조건을 지키는지 먼저 검사합니다" sub="은퇴 계정(H = −10%, α = 5%)에 채권 60 · 저위험 30 · 고위험 10%를 넣어 본다">
      <div style={{display: 'flex', gap: 26}}>
        {[
          ['기대수익 μ', `${fmt(m * 100, 2)}%`, C.text],
          ['표준편차 σ', `${fmt(s * 100, 2)}%`, C.text],
          ['하위 5% 수익률 μ − 1.645σ', `${fmt((m - 1.645 * s) * 100, 2)}%`, C.floor],
        ].map(([k, v, c], i) => (
          <Card key={k} style={{flex: 1, textAlign: 'center', ...rise(f, cue(1) + i * 16)}}>
            <div style={{fontSize: 28, color: C.muted}}>{k}</div>
            <div style={{fontSize: 70, fontWeight: 900, color: c}}>{v}</div>
          </Card>
        ))}
      </div>
      <div style={{position: 'relative', height: 120, marginTop: 40, ...rise(f, cue(1) + 50)}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: 50, height: 6, background: C.line}} />
        {[
          {v: -0.1, k: 'H = −10%', c: C.liab},
          {v: m - 1.645 * s, k: '하위 5% −6.40%', c: C.floor},
          {v: m, k: '평균 8.50%', c: C.text},
        ].map((p) => (
          <div key={p.k} style={{position: 'absolute', left: `${((p.v + 0.15) / 0.3) * 100}%`, top: 30}}>
            <div style={{width: 6, height: 46, background: p.c}} />
            <div style={{fontSize: 26, color: p.c, fontWeight: 700, whiteSpace: 'nowrap', transform: 'translateX(-40%)'}}>{p.k}</div>
          </div>
        ))}
      </div>
      <div style={{fontSize: 34, fontWeight: 800, color: C.accent, marginTop: 30, ...rise(f, cue(2))}}>
        통과 — 여유 3.6%p → 제약이 등호로 걸릴 때까지 위험을 올린다
      </div>
    </Scene>
  );
};

/* S2 세 계정 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="세 계정에 같은 순서를 적용하면 — γ 3.795 · 2.706 · 0.877" sub="계정마다 (H, α)만 다르다 · 미달 기준이 느슨할수록 γ가 작아 주식이 는다 (원 논문 표 재계산)">
      <Plane f={f} at={cue(0)} acc={2} lines={2} />
      <div style={{position: 'absolute', left: 1080, top: 0, width: 648}}>
        {N.accounts.map((a, i) => (
          <Card key={a.name} style={{marginBottom: 16, borderLeft: `6px solid ${AC[i]}`, padding: '16px 22px', ...rise(f, cue(1) + i * 24)}}>
            <div style={{fontSize: 30, fontWeight: 800, color: AC[i]}}>
              {a.name} (H {Math.round(a.H * 100)}%, α {Math.round(a.alpha * 100)}%)
            </div>
            <div style={{fontSize: 26, marginTop: 4}}>
              채권 · 저위험 · 고위험 = {a.w.map((x) => fmt(x * 100, 1)).join(' · ')}%
            </div>
            <div style={{fontSize: 24, color: C.muted}}>
              μ {fmt(a.m * 100, 2)}% · σ {fmt(a.s * 100, 2)}%
            </div>
          </Card>
        ))}
        <div style={{fontSize: 26, color: C.accent, fontWeight: 700, ...rise(f, cue(2) + 20)}}>상속 롱온리 → 0 · 8.9 · 91.1% (μ 26.35 → 23.67%)</div>
      </div>
    </Scene>
  );
};

/* S3 합쳐도 효율선 위 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="공매도를 허용하면 계좌별 해를 합쳐도 효율선 위에 있습니다" sub="계좌의 해 = 최소분산 포트폴리오 g + (1/γ) × 위험을 더 지는 방향 v">
      <Plane f={f} at={-100} acc={2} agg={cue(1) + 10} />
      <div style={{position: 'absolute', left: 1080, top: 0, width: 648}}>
        <Card style={{...rise(f, cue(0))}}>
          <Tex tex={String.raw`w_k = g + \frac{1}{\gamma_k}\,v`} size={50} />
          <Tex tex={String.raw`\frac{1}{\gamma} = \sum_k a_k \frac{1}{\gamma_k}`} size={44} />
        </Card>
        <Card style={{marginTop: 18, ...rise(f, cue(1))}}>
          <div style={{fontSize: 26, color: C.muted}}>은퇴 60 · 교육 20 · 상속 20%</div>
          <div style={{fontSize: 40, fontWeight: 900, marginTop: 4}}>전체 γ {fmt(N.agg.gamma, 3)}</div>
          <div style={{fontSize: 26, color: C.muted}}>평균 2.99가 아니다 — 역수의 평균</div>
          <div style={{fontSize: 26, marginTop: 6}}>채권 {Math.round(N.agg.w[0] * 100)} · 저위험 {Math.round(N.agg.w[1] * 100)} · 고위험 {Math.round(N.agg.w[2] * 100)}%</div>
          <div style={{fontSize: 24, color: C.accent, fontWeight: 700, marginTop: 8, opacity: prog(f, cue(2))}}>계정별 롱온리면 연 12bp 손실</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S4 왜 편한가 · 한계 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pts = [
    {k: '묻기 쉬운 두 숫자 (H, α)', v: '“이 계좌는 5% 확률로도 −10% 아래면 안 된다” → 운용사가 γ = 3.795로 번역'},
    {k: '쓰던 평균-분산 도구 그대로', v: 'γ를 10~30% 잘못 말하면 연 2.5~44bp 손실(원문 표 3) — (H, α)로 묻는 편이 낫다'},
    {k: '안 되는 목표를 먼저 거른다', v: '이 세 자산으로 “원금 손실 확률 5% 이하”는 불가능 — 하위 5% 경계의 최댓값 −2.31%'},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="실무에서 방법 2(Das–Markowitz)가 편한 이유는 세 가지입니다" sub="BPT는 왜 그렇게 행동하는지를, Das–Markowitz는 그 행동을 어떻게 운용할지를 답한다">
      {pts.map((p, i) => (
        <Card key={p.k} style={{marginBottom: 16, display: 'flex', gap: 24, alignItems: 'center', ...rise(f, cue(0) + 10 + i * 20)}}>
          <div style={{fontSize: 46, fontWeight: 900, color: C.accent, width: 50}}>{i + 1}</div>
          <div>
            <div style={{fontSize: 32, fontWeight: 800}}>{p.k}</div>
            <div style={{fontSize: 26, color: C.muted, marginTop: 4}}>{p.v}</div>
          </div>
        </Card>
      ))}
      <Card style={{borderLeft: `6px solid ${C.liab}`, ...rise(f, cue(1))}}>
        <div style={{fontSize: 32, fontWeight: 800, color: C.liab}}>한계 — 미달의 크기는 막지 못한다 → 필수 목표의 바닥은 Floor(CPPI)로</div>
      </Card>
    </Scene>
  );
};

export const M8E03b = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M8E03b_TOTAL = T.total;
