import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, CounterRow, RevealTable} from '../lib/ui';
import {fmt, lerp, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E01.numbers.json';
import T from '../data/M7E01.timing.json';

const EB = 'BAF.60080 · W06 LDI · ① 부채와 적립비율';
const W = 1728;
const H = 630;

/* S0 자산 +7.5%인데 나쁜 해 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const pA = prog(f, cue(0) + 20, 40);
  const pL = prog(f, cue(1) + 20, 40);
  const k = 3.4;
  const base = 560;
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E01" title="자산이 7.5% 올랐는데도 나쁜 해가 될 수 있습니다" sub="할인율이 3%에서 2%로 내려 부채가 15% 늘어난 해의 회의실">
      <svg width={1000} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={120} y={base - N.A * k} width={240} height={N.A * k} rx={8} fill={C.asset} opacity={0.35} />
        <rect x={120} y={base - lerp(N.A, N.hook.A1, pA) * k} width={240} height={lerp(N.A, N.hook.A1, pA) * k} rx={8} fill={C.asset} opacity={0.85} />
        <text x={240} y={base - lerp(N.A, N.hook.A1, pA) * k - 18} fill={C.asset} fontSize={40} fontWeight={800} textAnchor="middle">
          자산 {fmt(lerp(N.A, N.hook.A1, pA), 1)}
        </text>
        <rect x={520} y={base - lerp(N.L, N.hook.L1, pL) * k} width={240} height={lerp(N.L, N.hook.L1, pL) * k} rx={8} fill={C.liab} opacity={0.85} />
        <text x={640} y={base - lerp(N.L, N.hook.L1, pL) * k - 18} fill={C.liab} fontSize={40} fontWeight={800} textAnchor="middle">
          부채 {fmt(lerp(N.L, N.hook.L1, pL), 1)}
        </text>
        <line x1={80} x2={820} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        <text x={240} y={base + 44} fill={C.muted} fontSize={28} textAnchor="middle" opacity={pA}>
          +7.5%
        </text>
        <text x={640} y={base + 44} fill={C.muted} fontSize={28} textAnchor="middle" opacity={pL}>
          +15% (할인율 3% → 2%)
        </text>
      </svg>
      <div style={{position: 'absolute', left: 1000, top: 30, width: 728}}>
        <Card style={{...rise(f, cue(0))}}>
          <div style={{fontSize: 28, color: C.muted}}>운용역의 보고</div>
          <div style={{fontSize: 56, fontWeight: 900, color: C.asset}}>“자산 +7.5%”</div>
        </Card>
        <Card style={{marginTop: 20, ...rise(f, cue(1))}}>
          <div style={{fontSize: 28, color: C.muted}}>이사회의 질문</div>
          <div style={{fontSize: 56, fontWeight: 900, color: C.liab}}>“부채는 +15%”</div>
        </Card>
        <Card style={{marginTop: 20, padding: '4px 0', ...rise(f, cue(2))}}>
          <CounterRow f={f} show={cue(2)} at={cue(2) + 10} label="적립비율" from={N.FR0 * 100} to={N.hook.FR1 * 100} d={0} unit="%" color={C.accent} />
        </Card>
      </div>
    </Scene>
  );
};

/* S1 화폐의 시간가치 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cards = [
    {k: '① 1년 맡기면', tex: String.raw`P\,(1+r)`, n: '100 × 1.04 = 104', at: cue(0) + 20},
    {k: '② t년 맡기면 (복리)', tex: String.raw`P\,(1+r)^t`, n: '100 × 1.04² = 108.16', at: cue(0) + 50},
    {k: '③ 거꾸로 풀면 = 할인', tex: String.raw`\frac{CF}{(1+r)^t}`, n: '108.16 ÷ 1.04² = 100', at: cue(1) + 10},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="미래의 자금은 붙을 이자만큼 깎아 오늘 값으로 바꿉니다" sub="기본 지식 — 화폐의 시간가치: 오늘의 100만 원이 1년 뒤 100만 원보다 값지다">
      <div style={{display: 'flex', gap: 30, marginTop: 20}}>
        {cards.map((c, i) => (
          <Card key={c.k} style={{flex: 1, textAlign: 'center', border: i === 2 ? `3px solid ${C.accent}` : undefined, ...rise(f, c.at)}}>
            <div style={{fontSize: 30, color: i === 2 ? C.accent : C.muted}}>{c.k}</div>
            <Tex tex={c.tex} size={64} />
            <div style={{fontSize: 30, fontWeight: 700, marginTop: 6}}>{c.n}</div>
          </Card>
        ))}
      </div>
      <div style={{fontSize: 32, color: C.muted, textAlign: 'center', marginTop: 40, ...rise(f, cue(1) + 40)}}>
        불리기 → ← 할인 (금리 4% 예)
      </div>
    </Scene>
  );
};

/* S2 연금 부채 = 해마다 할인해 더한 값 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const k = 5;
  const base = 500;
  const X = (i: number) => 520 + i * 220;
  const stackP = prog(f, cue(2), 40);
  return (
    <Scene t={t} eyebrow={EB} title="연금 부채는 해마다 줄 금액을 각각 할인해 더한 값입니다" sub="숫자 예 — 3년간 매년 30을 지급, 할인율 4%">
      <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={60} x2={1280} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
        {[0, 1, 2, 3].map((i) => (
          <text key={i} x={i === 0 ? 220 : X(i - 1)} y={base + 44} fill={C.muted} fontSize={26} textAnchor="middle">
            {i === 0 ? '오늘' : `${i}년 뒤`}
          </text>
        ))}
        {N.pv.map((pv, i) => {
          const pIn = prog(f, cue(0) + 10 + i * 10, 20);
          const pD = prog(f, cue(1) + 6 + i * 20, 30);
          const h = lerp(30, pv, pD) * k;
          // 오늘 쪽으로 쌓이기
          const xx = lerp(X(i), 220, stackP);
          const prev = N.pv.slice(0, i).reduce((a, b) => a + b, 0) * k;
          const yy = lerp(base - h, base - prev - h, stackP);
          return (
            <g key={i} opacity={pIn}>
              <rect x={X(i) - 50} y={base - 30 * k} width={100} height={30 * k} rx={6} fill="none" stroke={C.muted} strokeDasharray="8 6" strokeWidth={2} opacity={1 - stackP} />
              <rect x={xx - 50} y={yy} width={100} height={h} rx={6} fill={C.liab} opacity={0.6 + i * 0.13} stroke={C.bg} strokeWidth={2} />
              <text x={xx} y={yy + h / 2 + 12} fill={C.bg} fontSize={30} fontWeight={800} textAnchor="middle">
                {fmt(lerp(30, pv, pD), 2)}
              </text>
            </g>
          );
        })}
        <g opacity={prog(f, cue(2) + 30)}>
          <text x={220} y={base - N.Lsum * k - 24} fill={C.liab} fontSize={42} fontWeight={900} textAnchor="middle">
            L = {fmt(N.Lsum, 2)}
          </text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 1320, top: 10, width: 408}}>
        <Card style={{...rise(f, cue(1) + 60)}}>
          <div style={{fontSize: 26, color: C.muted}}>같은 금액이면 연금현가 공식</div>
          <Tex tex={String.raw`L = C\,\frac{1-(1+r)^{-n}}{r}`} size={32} />
          <div style={{fontSize: 26, color: C.muted}}>30 × 2.775 = 83.25</div>
        </Card>
        <Card style={{marginTop: 20, ...rise(f, cue(2) + 40)}}>
          <div style={{fontSize: 30}}>줄 금액 90</div>
          <div style={{fontSize: 30}}>오늘 필요 {fmt(N.Lsum, 2)}</div>
          <div style={{fontSize: 30, color: C.accent, fontWeight: 700}}>이자가 채우는 몫 {fmt(90 - N.Lsum, 2)}</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S3 부채는 추정 · FR과 S */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const wob = Math.sin(f / 9) * 18 * (1 - prog(f, cue(1), 20));
  const k = 4.2;
  const base = 560;
  return (
    <Scene t={t} eyebrow={EB} title="자산은 매일 관찰되지만 부채는 할인율로 추정될 뿐입니다" sub="적립비율은 줄 금액의 몇 배를 가졌는지, 잉여금은 버틸 여유입니다">
      <svg width={760} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={90} y={base - N.A * k} width={250} height={N.A * k} rx={8} fill={C.asset} opacity={prog(f, cue(0))} />
        <text x={215} y={base - 200} fill={C.bg} fontSize={36} fontWeight={800} textAnchor="middle" opacity={prog(f, cue(0))}>
          자산 100
        </text>
        <text x={215} y={base + 44} fill={C.asset} fontSize={26} textAnchor="middle" opacity={prog(f, cue(0))}>
          시장 가격 · 매일 관찰
        </text>
        <rect
          x={400}
          y={base - N.L * k - wob}
          width={250}
          height={N.L * k + wob}
          rx={8}
          fill={C.liab}
          fillOpacity={0.25}
          stroke={C.liab}
          strokeWidth={4}
          strokeDasharray="12 8"
          opacity={prog(f, cue(0) + 20)}
        />
        <text x={525} y={base - 150} fill={C.liab} fontSize={36} fontWeight={800} textAnchor="middle" opacity={prog(f, cue(0) + 20)}>
          부채 80
        </text>
        <text x={525} y={base + 44} fill={C.liab} fontSize={26} textAnchor="middle" opacity={prog(f, cue(0) + 20)}>
          할인율로 추정
        </text>
        <line x1={60} x2={700} y1={base} y2={base} stroke={C.muted} strokeWidth={2} />
      </svg>
      <div style={{position: 'absolute', left: 820, top: 0, width: 908}}>
        <div style={{display: 'flex', gap: 24}}>
          <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(1))}}>
            <div style={{fontSize: 28, color: C.muted}}>적립비율 FR</div>
            <Tex tex={String.raw`\frac{A}{L} = \frac{100}{80}`} size={44} />
            <div style={{fontSize: 64, fontWeight: 900, color: C.accent, transform: `scale(${pop(f, cue(1) + 30)})`}}>125%</div>
          </Card>
          <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(1) + 14)}}>
            <div style={{fontSize: 28, color: C.muted}}>잉여금 S</div>
            <Tex tex={String.raw`A - L = 100 - 80`} size={44} />
            <div style={{fontSize: 64, fontWeight: 900, color: C.accent, transform: `scale(${pop(f, cue(1) + 44)})`}}>20</div>
          </Card>
        </div>
        <div style={{fontSize: 28, color: C.muted, marginTop: 20, ...rise(f, cue(1) + 50)}}>판정: FR ≥ 100%면 적립, 미만이면 미적립</div>
        <Card style={{marginTop: 26, borderLeft: `6px solid ${C.liab}`, ...rise(f, cue(2))}}>
          <div style={{fontSize: 30, fontWeight: 700}}>적립배율 ≠ 적립비율</div>
          <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>국민연금 공시 지표 = 적립금 ÷ 그해 지출 (부채 현재가치가 아니다)</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S4 1년 뒤 적립비율 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="1년 뒤 적립비율은 자산 수익률에서 부채 수익률을 뺀 만큼 움직입니다" sub="r_L은 시간 이자와 금리 변화에 따른 재평가를 합친 부채의 변화율이다">
      <div style={{width: 1000}}>
        <RevealTable
          f={f}
          cols={['단계 (자산 +7%, 부채 +10%)', '계산', '결과']}
          widths={[1.3, 1, 0.7]}
          rows={[
            {cells: ['새 자산', '100 × 1.07', fmt(N.yr.A1, 0)], at: cue(0) + 20},
            {cells: ['새 부채', '80 × 1.10', fmt(N.yr.L1, 0)], at: cue(0) + 40},
            {cells: ['새 적립비율 (정확)', '107 ÷ 88', `${fmt(N.yr.FR1 * 100, 1)}%`], at: cue(1), hi: f >= cue(1) && f < cue(2)},
            {cells: ['근사식', '125% × (7% − 10%)', `${fmt((N.FR0 + N.yr.approx) * 100, 2)}%`], at: cue(2), hi: f >= cue(2)},
          ]}
        />
      </div>
      <div style={{position: 'absolute', left: 1060, top: 0, width: 668}}>
        <Card style={{...rise(f, cue(2) + 10)}}>
          <div style={{fontSize: 26, color: C.muted}}>근사 (1 + a) ÷ (1 + b) ≈ 1 + a − b</div>
          <Tex tex={String.raw`\Delta FR \approx FR \times (r_A - r_L)`} size={44} />
        </Card>
        <div style={{fontSize: 38, fontWeight: 800, color: C.liab, marginTop: 40, ...rise(f, cue(1) + 30)}}>
          7%를 벌고도 −{fmt((N.FR0 - N.yr.FR1) * 100, 1)}%p
        </div>
        <div style={{fontSize: 30, color: C.muted, marginTop: 10, ...rise(f, cue(1) + 40)}}>좋은 해 = “부채보다 많이 번 해”</div>
      </div>
    </Scene>
  );
};

/* S5 잉여금 수익률 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const p = prog(f, cue(1) + 20, 40);
  return (
    <Scene t={t} eyebrow={EB} title="성적표를 한 숫자로 쓰면 잉여금 수익률이 됩니다" sub="잉여금 변화 = 자산이 번 금액 − 부채가 늘어난 금액, 이를 자산으로 나눈다">
      <div style={{...rise(f, cue(0))}}>
        <Tex tex={String.raw`R_S = r_A - \frac{L}{A}\, r_L`} size={72} />
      </div>
      <div style={{display: 'flex', gap: 24, justifyContent: 'center', marginTop: 20, ...rise(f, cue(1))}}>
        {[
          ['r_A', '+7%', C.asset],
          ['r_L', '+10%', C.liab],
          ['L/A', '0.8', C.muted],
          ['R_S', `${fmt(N.yr.RS * 100, 0)}%`, C.accent],
        ].map(([k, v, c]) => (
          <Card key={k} style={{width: 280, textAlign: 'center'}}>
            <Tex tex={k} size={34} color={C.muted} style={{margin: '-10px 0'}} />
            <div style={{fontSize: 56, fontWeight: 900, color: c}}>{v}</div>
          </Card>
        ))}
      </div>
      <div style={{textAlign: 'center', fontSize: 36, marginTop: 30, ...rise(f, cue(1) + 20)}}>
        잉여금 <b style={{color: C.accent}}>{fmt(lerp(N.S0, N.yr.A1 - N.yr.L1, p), 1)}</b>
        <span style={{color: C.muted}}> (= 107 − 88)</span>
      </div>
    </Scene>
  );
};

export const M7E01 = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M7E01_TOTAL = T.total;
