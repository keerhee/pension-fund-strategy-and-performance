import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, HBar, RevealTable} from '../lib/ui';
import {fmt, pct, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E06.numbers.json';
import T from '../data/M8E06.timing.json';

const EB = 'BAF.60080 · W06 GBI · ⑥ Floor 운용 규칙';

/* S0 매년 재설정 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const R = N.reset as {k: string; A: number; F: number; psp_reset: number; psp_no: number}[];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E06" title="Floor를 매년 다시 정하면 Cash Trap을 피하는 대신 보호 수준이 움직입니다" sub="Flexicure(EDHEC 2018) — 매년 초 F = 0.8A · 1년 뒤 (A 10 · F 8 · m 3 출발, PSP 60%)">
      <div style={{display: 'flex', gap: 30}}>
        {R.map((r, i) => {
          const at = cue(1 + i);
          return (
            <Card key={r.k} style={{flex: 1, borderTop: `6px solid ${i ? C.liab : C.floor}`, ...rise(f, at)}}>
              <div style={{fontSize: 36, fontWeight: 800, color: i ? C.liab : C.floor}}>
                {r.k} — A = {fmt(r.A, 1)}
              </div>
              <div style={{fontSize: 28, color: C.muted, marginTop: 6}}>
                재설정 Floor {fmt(r.F, 1)} {i ? '' : '(이익 잠금)'}
              </div>
              <HBar f={f} at={at + 20} label="재설정 후 PSP" value={r.psp_reset} max={1} text={pct(r.psp_reset, 0)} color={C.floor} textWidth={140} />
              <HBar f={f} at={at + 40} label="재설정 안 하면" value={r.psp_no} max={1} text={pct(r.psp_no, 0)} color={i ? C.liab : C.accent} textWidth={140} />
            </Card>
          );
        })}
      </div>
      <div style={{fontSize: 34, fontWeight: 800, color: C.accent, marginTop: 10, ...rise(f, cue(3))}}>보호하는 것은 절대 금액이 아니라 ‘한 해 손실 ≤ 20%’</div>
    </Scene>
  );
};

/* S1 장치들 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="벌면 잠그고, 가까워지면 줄이고, 닿으면 확정하는 장치가 더 있습니다" sub="GBI 일반 틀의 장치 — F는 Floor, A는 자산, C는 열망 목표의 현재가치">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['상황', '장치']}
          widths={[0.8, 2]}
          rows={[
            {cells: ['벌면 이익을 잠근다', 'Ratchet (TIPP, Estep–Kritzman 1988)'], at: cue(0) + 10},
            {cells: ['벌면 이익을 잠근다', '최대낙폭 Floor (Grossman–Zhou 1993)'], at: cue(0) + 26},
            {cells: ['목표에 가까우면 줄인다', 'Cap'], at: cue(1)},
            {cells: ['목표에 닿으면 확정', 'Stop-gain (EDHEC GBI) — 자산이 C에 처음 닿는 날 전액 GHP로'], at: cue(1) + 16},
            {cells: ['시장이 불안하면 조인다', '변동성 연동 m'], at: cue(1) + 32},
          ]}
        />
      </div>
      <Card style={{marginTop: 22, borderLeft: `6px solid ${C.accent}`, ...rise(f, cue(2))}}>
        <div style={{fontSize: 30, fontWeight: 800}}>IC 결정 — 잃었을 때 Floor 유지(ratchet)는 보호 우선, 재설정(Flexicure)은 참여 우선</div>
      </Card>
    </Scene>
  );
};

/* S2 장점과 한계 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="규칙 기반 자동 보호는 강력하지만 Cash Trap과 승수 선택의 함정이 있습니다" sub="이론은 연속시간, 실무는 이산시간 — ‘떨어지면 판다’는 구조는 남는다">
      <div style={{display: 'flex', gap: 30}}>
        <Card style={{flex: 1, borderTop: `6px solid ${C.floor}`, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor}}>장점 — 자동 · 투명</div>
          {['하락 시 PSP 자동 감소', '“최악에도 Safety 목표” 심리적 안정', '감정 편향 차단'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 12}}>
              • {x}
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, borderTop: `6px solid ${C.liab}`, ...rise(f, cue(1))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab}}>한계 — 규칙의 그림자</div>
          {['급락 시 락인 (Cash Trap)', 'm — 크면 락인, 작으면 정체', '이산 리밸런싱 오버슈트', '쏠림 — 모두 같은 규칙이면 같이 판다'].map((x) => (
            <div key={x} style={{fontSize: 28, marginTop: 12}}>
              • {x}
            </div>
          ))}
        </Card>
      </div>
      <div style={{fontSize: 32, fontWeight: 800, color: C.accent, marginTop: 24, ...rise(f, cue(2))}}>도입 조건 — 규모 한도 · 매도 속도 상한 (IC 반대신문 쟁점)</div>
    </Scene>
  );
};

/* S3 VaR 운용 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const V = N.var as {k: string; vol: number; two: number; E: number}[];
  return (
    <Scene t={t} eyebrow={EB} title="VaR로 Floor를 운용하면 Cash Trap은 없지만 변동성 급등 때 함께 팝니다" sub="‘2σ 손실 ≤ 자산의 5%’가 되게 위험자산을 정한다 — 자산 10억 · 손실 예산 0.5억">
      <div style={{width: 1300}}>
        {V.map((v, i) => (
          <HBar
            key={v.k}
            f={f}
            at={cue(1) + i * 40}
            label={`${v.k} — 연 변동성 ${Math.round(v.vol * 100)}% · 월 2σ ${fmt(v.two * 100, 1)}%`}
            value={v.E}
            max={10}
            text={`${fmt(v.E, 1)}억 (${Math.round(v.E * 10)}%)`}
            color={i ? C.liab : C.asset}
            textWidth={320}
          />
        ))}
      </div>
      <div style={{fontSize: 34, fontWeight: 800, color: C.liab, marginTop: 10, ...rise(f, cue(1) + 80)}}>불안기 — 2.4억을 한 번에 판다</div>
      <Card style={{marginTop: 24, borderLeft: `6px solid ${C.floor}`, ...rise(f, cue(2))}}>
        <div style={{fontSize: 30, fontWeight: 800, color: C.floor}}>권고 — 필수 목표는 고정 Floor(GHP)로 지키고, VaR 예산은 위험 계좌 안에서만</div>
      </Card>
    </Scene>
  );
};

export const M8E06 = makeEpisode(T, [S0, S1, S2, S3]);
export const M8E06_TOTAL = T.total;
