import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Tex} from '../lib/Tex';
import {Card, RevealTable} from '../lib/ui';
import {fmt, pct, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E03c.numbers.json';
import T from '../data/M8E03c.timing.json';

const EB = 'BAF.60080 · W06 GBI · ③ 필요 자본 · 방법 3 몬테카를로';
const H = 630;

/* S0 아이디어 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E03c" title="방법 3 — 몬테카를로는 경로를 수만 개 만들어 달성 확률을 직접 셉니다" sub="방법 1은 로그정규 · 고정 비중, 방법 2는 한 기간 · 정규 — 두꺼운 꼬리 · 현금흐름 · 동적 규칙에는 닫힌 해가 없다">
      <Card style={{...rise(f, cue(1))}}>
        <Tex tex={String.raw`\hat p = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}\{W_T^{(i)} \ge G\}, \qquad \text{오차} \approx \sqrt{\frac{p(1-p)}{N}}`} size={50} />
      </Card>
      <div style={{display: 'flex', gap: 30, marginTop: 26}}>
        <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(2))}}>
          <div style={{fontSize: 28, color: C.muted}}>N = 10,000 · p = 70%</div>
          <div style={{fontSize: 70, fontWeight: 900, color: C.asset}}>±{fmt(N.se * 100, 2)}%p</div>
        </Card>
        <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(2) + 20)}}>
          <div style={{fontSize: 28, color: C.muted}}>강의 실행 N = 100,000</div>
          <div style={{fontSize: 70, fontWeight: 900, color: C.floor}}>±0.14%p</div>
          <div style={{fontSize: 24, color: C.muted}}>1초 안에 끝난다</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S1 경로 부채꼴 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const P = N.paths as number[][];
  const X = (y: number) => 110 + y * 95;
  const Y = (v: number) => 560 - (Math.log(v) - Math.log(1)) * 260;
  const yrs = prog(f, cue(0) + 10, 140) * 10;
  const done = prog(f, cue(1), 20);
  const G = 3;
  const shown = Math.round(P.length * prog(f, cue(0), 30));
  const pathD = (p: number[]) => {
    const n = Math.floor(yrs);
    const pts = p.slice(0, n + 1).map((v, i) => `${i ? 'L' : 'M'} ${X(i)} ${Y(v)}`);
    if (n < 10) {
      const fr = yrs - n;
      const v = p[n] * Math.pow(p[n + 1] / p[n], fr);
      pts.push(`L ${X(n + fr)} ${Y(v)}`);
    }
    return pts.join(' ');
  };
  const hits = P.filter((p) => p[10] >= G).length;
  return (
    <Scene t={t} eyebrow={EB} title="경로 하나를 한 해씩 굴리는 일을 10만 번 반복합니다" sub={`Market 계좌 · K = ${fmt(N.K_mc, 2)}억 · 주식 67% · 매년 비중 되돌림 · seed 2026 (표본 ${P.length}개 표시)`}>
      <svg width={1250} height={H} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X(0)} x2={X(10)} y1={570} y2={570} stroke={C.muted} strokeWidth={2} />
        {[0, 2, 4, 6, 8, 10].map((y) => (
          <text key={y} x={X(y)} y={605} fill={C.muted} fontSize={22} textAnchor="middle">
            {y}년
          </text>
        ))}
        {[2, 3, 5, 8].map((v) => (
          <text key={v} x={X(0) - 14} y={Y(v) + 8} fill={C.muted} fontSize={22} textAnchor="end">
            {v}억
          </text>
        ))}
        {P.slice(0, shown).map((p, i) => (
          <path key={i} d={pathD(p)} fill="none" stroke={done > 0 ? (p[10] >= G ? C.floor : C.liab) : C.asset} strokeWidth={1.6} opacity={0.35} />
        ))}
        <line x1={X(0)} x2={X(10) + 20} y1={Y(G)} y2={Y(G)} stroke={C.text} strokeWidth={3} strokeDasharray="10 8" />
        <text x={X(10) + 26} y={Y(G) + 8} fill={C.text} fontSize={28} fontWeight={800}>
          G = 3억
        </text>
      </svg>
      <div style={{position: 'absolute', left: 1300, top: 40, width: 428}}>
        <Card style={{textAlign: 'center', opacity: done}}>
          <div style={{fontSize: 28, color: C.muted}}>3억에 닿은 비율</div>
          <div style={{fontSize: 30, color: C.muted}}>표본 {hits}/{P.length}</div>
          <div style={{fontSize: 96, fontWeight: 900, color: C.floor}}>{pct(N.hit, 1)}</div>
          <div style={{fontSize: 24, color: C.muted}}>10만 경로 기준</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S2 K 찾기 — 장난감 10경로 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const Ks = [2.0, 2.2, 2.4];
  return (
    <Scene t={t} eyebrow={EB} title="K 찾기 — 후보 K마다 같은 경로 전체에서 성공 비율을 셉니다" sub="장난감 예 — Market(G 3억 · p 70%) · 경로 10개 · 10년 뒤 자산 = K × 성장 배수">
      <div style={{display: 'flex', gap: 30}}>
        <div style={{flex: 1}}>
          <Card style={{padding: '8px 0'}}>
            <div style={{display: 'flex', padding: '10px 24px', fontSize: 24, color: C.muted, borderBottom: `1px solid ${C.line}`}}>
              <span style={{flex: 1.2}}>경로 (성장 배수)</span>
              {Ks.map((k) => (
                <span key={k} style={{flex: 1, textAlign: 'center'}}>
                  K {fmt(k, 1)}억
                </span>
              ))}
            </div>
            {N.toy.map((g, i) => (
              <div key={i} style={{display: 'flex', padding: '5px 24px', fontSize: 25, ...rise(f, cue(1) + i * 5, 10, 10)}}>
                <span style={{flex: 1.2, color: C.muted}}>
                  {i + 1} ({fmt(g, 3)})
                </span>
                {Ks.map((k, j) => {
                  const w = k * g;
                  const ok = w >= 3;
                  return (
                    <span key={k} style={{flex: 1, textAlign: 'center', color: ok ? C.floor : C.liab, opacity: prog(f, cue(1) + 50 + j * 16)}}>
                      {fmt(w, 2)} {ok ? '✓' : ''}
                    </span>
                  );
                })}
              </div>
            ))}
          </Card>
        </div>
        <div style={{width: 560}}>
          {Ks.map((k, j) => {
            const hits = N.toy.filter((g) => k * g >= 3).length;
            return (
              <Card key={k} style={{marginBottom: 14, display: 'flex', justifyContent: 'space-between', alignItems: 'center', ...rise(f, cue(1) + 60 + j * 16)}}>
                <span style={{fontSize: 30}}>K {fmt(k, 1)}억</span>
                <span style={{fontSize: 40, fontWeight: 900, color: hits >= 7 ? C.floor : C.liab}}>
                  {hits}/10 {hits >= 7 ? '✓' : '미달'}
                </span>
              </Card>
            );
          })}
          <Card style={{border: `3px solid ${C.accent}`, transform: `scale(${pop(f, cue(2) + 10)})`}}>
            <div style={{fontSize: 26, color: C.muted}}>10만 경로 · 이분법</div>
            <div style={{fontSize: 46, fontWeight: 900, color: C.accent}}>K = {fmt(N.K_mc, 2)}억</div>
            <div style={{fontSize: 24, color: C.muted}}>닫힌 해 2.24억 · 공통 난수로 비교</div>
          </Card>
        </div>
      </div>
    </Scene>
  );
};

/* S3 다수결은 틀린다 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const steps = ['후보(K · 비중)를 미리 정한다', '각 후보를 같은 경로 전체에 적용', '후보마다 성공 비율 · 부족액을 센다', '조건을 모두 만족하는 가장 싼 후보'];
  return (
    <Scene t={t} eyebrow={EB} title="다수결은 틀립니다 — 후보를 먼저 정하고 같은 경로로 셉니다" sub="미래를 보고 고르지 말고, 미리 정한 후보를 같은 경로로 세어 고른다">
      <div style={{display: 'flex', gap: 30}}>
        <Card style={{flex: 1, borderTop: `6px solid ${C.liab}`, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab}}>✗ 경로마다 다수결</div>
          {['경로마다 가장 좋은 K · 비중을 고른다', '사후 최적 — 미래 경로를 안 뒤 고른다', '실행 불가 · 극단 해 (주식 100% vs GHP 100%)'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 14}}>
              • {x}
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, borderTop: `6px solid ${C.floor}`, ...rise(f, cue(1))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor}}>✓ 올바른 네 단계</div>
          {steps.map((x, i) => (
            <div key={x} style={{fontSize: 28, marginTop: 14, ...rise(f, cue(1) + 20 + i * 14)}}>
              {i + 1}. {x}
            </div>
          ))}
        </Card>
      </div>
      <div style={{fontSize: 28, color: C.muted, marginTop: 24, ...rise(f, cue(1) + 90)}}>
        한 계좌 격자로 세면: 최소 통과 K = {N.grid.K}억 · 주식 {Math.round(N.grid.w * 100)}% (Safety {pct(N.grid.pS, 1)} · Market {pct(N.grid.pM, 1)} · Aspirational {pct(N.grid.pA, 1)})
      </div>
    </Scene>
  );
};

/* S4 결과 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="MC는 닫힌 해를 재현하고, 꼬리의 비용은 갭 위험에서 드러납니다" sub="seed 2026 · 100,000 경로 · 10년 연 단위 · t분포는 자유도 5를 분산 1로 맞춤 — gbi_mc.py 실행 결과">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['목표 · 기준 확률', '닫힌 해 K', 'MC K', '닫힌 K로 센 확률', 'MC K · 두꺼운 꼬리 t5']}
          widths={[1.3, 0.8, 0.8, 1, 1.1]}
          rows={N.table.map((r, i) => ({cells: [r.goal, `${fmt(r.Kc, 2)}억`, `${fmt(r.Km, 2)}억`, r.pk, `${fmt(r.Kt, 2)}억`], at: cue(0) + 10 + i * 16, hi: f >= cue(1) && f < cue(2)}))}
        />
      </div>
      <div style={{display: 'flex', gap: 26, marginTop: 24}}>
        <Card style={{flex: 1, ...rise(f, cue(2))}}>
          <div style={{fontSize: 28, color: C.muted}}>CPPI · 자산 10억 · m 3 · floor 위반</div>
          <div style={{display: 'flex', alignItems: 'baseline', gap: 24, marginTop: 6}}>
            <span style={{fontSize: 60, fontWeight: 900, color: C.asset}}>{pct(N.cppi.breach_n, 1)}</span>
            <span style={{fontSize: 40, color: C.accent}}>→</span>
            <span style={{fontSize: 60, fontWeight: 900, color: C.liab, transform: `scale(${pop(f, cue(2) + 40)})`, display: 'inline-block'}}>{pct(N.cppi.breach_t, 1)}</span>
            <span style={{fontSize: 26, color: C.muted}}>정규 → t5</span>
          </div>
        </Card>
        <Card style={{flex: 1, ...rise(f, cue(2) + 20)}}>
          <div style={{fontSize: 28, color: C.muted}}>같은 CPPI의 목표 달성</div>
          <div style={{fontSize: 28, marginTop: 8}}>6억 {pct(N.cppi.p6, 1)} · 9억 {pct(N.cppi.p9, 1)} · 14억 {pct(N.cppi.p14, 1)}</div>
          <div style={{fontSize: 26, color: C.muted}}>중위 {fmt(N.cppi.med, 1)}억</div>
        </Card>
      </div>
    </Scene>
  );
};

/* S5 세 방법 비교 */
const S5: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="같은 문제, 세 풀이 — K를, 비중을, 확률을 셉니다" sub="방법 1 · 2는 확률을 평균 · 변동성 조건으로 번역하고, 방법 3은 그 번역을 경로로 확인한다">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={26}
          cols={['구분', '방법 1 — 가장 싼 K', '방법 2 — Das–Markowitz', '방법 3 — 몬테카를로']}
          widths={[0.7, 1.1, 1.1, 1.1]}
          rows={[
            {cells: ['묻는 것', '목표 G · 시점 T · 확률 p', '최소 수익률 H · 한도 α', '목표 · 확률 + 현금흐름 · 규칙'], at: cue(0) + 6},
            {cells: ['가정', '로그정규 · 고정 비중', '한 기간 · 정규', '아무 분포 · 동적 규칙'], at: cue(0) + 20},
            {cells: ['답', 'K 4.91 · 2.24 · 1.97억', 'γ 3.795 · 2.706 · 0.877', 'K 2.26억 · 확률 · 부족액'], at: cue(0) + 34},
            {cells: ['언제', '상담 첫 장 · 손계산 점검', '계좌별 배분 설계', '상품 운용 · 공시 · IC 검증'], at: cue(1)},
            {cells: ['이론 계보', 'Kataoka(1963)형', 'Telser(1956)형', 'Roy(1952) 확률을 직접'], at: cue(1) + 14},
          ]}
        />
      </div>
      <div style={{fontSize: 32, fontWeight: 800, color: C.accent, marginTop: 24, ...rise(f, cue(2))}}>
        바닥은 CPPI가, 위험 블록의 구성은 Das–Markowitz가 — 다음 편: ④ Floor 만들기
      </div>
    </Scene>
  );
};

export const M8E03c = makeEpisode(T, [S0, S1, S2, S3, S4, S5]);
export const M8E03c_TOTAL = T.total;
