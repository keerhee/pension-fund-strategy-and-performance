import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, Chip, HBar, RevealTable} from '../lib/ui';
import {fmt, pct, pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M8E07.numbers.json';
import T from '../data/M8E07.timing.json';

const EB = 'BAF.60080 · W06 GBI · ⑦ GBI와 현실 세계';
const SRC = '출처: 금융감독원 2025년 퇴직연금 운용현황(2026.5) · 고용노동부 · 한국금융신문 2026.9.10 · 자본시장연구원 26-08';

/* S0 MVO → GBI 지도 · 4대 도전 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const cols = [
    {k: 'MVO', a: '일반 투자자', r: 'σ (변동성)', p: 'γ 하나'},
    {k: 'TDF', a: 'DC 가입자', r: '경로 위험', p: '나이 하나'},
    {k: 'LDI', a: 'DB 기관', r: '듀레이션 갭', p: '기관 단위'},
    {k: 'GBI', a: '개인', r: 'P(W < G)', p: '완전 개인화'},
  ];
  const ch = ['① 목표 수집 — 설문 · 현재 편향', '② 계산 복잡성 — 개인별 MC × 10만 명', '③ 비용 — TDF 0.3~0.5% vs GBI 0.8~1.5%(예상)', '④ 규제 — 적합성 · 맞춤 자문 · 설명 의무'];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E07" title="GBI는 가장 개인화된 틀이지만 가장 복잡하고 비쌉니다" sub="전반부 W1~W7의 지도 — 오른쪽으로 갈수록 “누구를 위한 최적인가”가 좁혀진다">
      <div style={{display: 'flex', gap: 14}}>
        {cols.map((c, i) => (
          <Card key={c.k} style={{flex: 1, border: i === 3 ? `3px solid ${C.floor}` : undefined, padding: '18px 22px', ...rise(f, cue(0) + i * 12)}}>
            <div style={{fontSize: 38, fontWeight: 900, color: i === 3 ? C.floor : C.text}}>{c.k}</div>
            <div style={{fontSize: 24, color: C.muted, marginTop: 6}}>대상 · {c.a}</div>
            <div style={{fontSize: 24, color: C.muted}}>위험 · {c.r}</div>
            <div style={{fontSize: 24, color: C.muted}}>개인화 · {c.p}</div>
          </Card>
        ))}
      </div>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginTop: 24}}>
        {ch.map((x, i) => (
          <Card key={x} style={{padding: '14px 22px', ...rise(f, cue(2) + i * 12)}}>
            <div style={{fontSize: 27}}>{x}</div>
          </Card>
        ))}
      </div>
    </Scene>
  );
};

/* S1 퇴직연금 501조 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const P = N.pension as {k: string; v: number; sh: number; ret: number}[];
  const cs = [C.liab, C.asset, C.floor];
  return (
    <Scene t={t} eyebrow={EB} title="한국 퇴직연금 501조 — DB는 회사, DC · IRP는 개인이 위험을 집니다" sub={SRC}>
      <div style={{display: 'flex', height: 120, borderRadius: 14, overflow: 'hidden', ...rise(f, cue(0))}}>
        {P.map((p, i) => (
          <div key={p.k} style={{width: `${p.sh * 100 * prog(f, cue(1) + i * 14, 24)}%`, background: cs[i], display: 'flex', flexDirection: 'column', justifyContent: 'center', paddingLeft: 20, color: C.bg, fontWeight: 800}}>
            <div style={{fontSize: 28}}>{p.k}</div>
            <div style={{fontSize: 34}}>
              {fmt(p.v, 1)}조 · {p.ret}%
            </div>
          </div>
        ))}
      </div>
      <div style={{display: 'flex', gap: 14, marginTop: 14, ...rise(f, cue(1) + 50)}}>
        <Chip color={C.liab}>DB — 기관의 LDI(M7) 무대</Chip>
        <Chip color={C.floor}>DC · IRP — 개인이 목표를 지는 GBI 무대</Chip>
      </div>
      <div style={{display: 'flex', gap: 30, marginTop: 30, alignItems: 'center'}}>
        <Card style={{width: 520, textAlign: 'center', ...rise(f, cue(2))}}>
          <div style={{fontSize: 28, color: C.muted}}>원리금보장 비중 (2025 말)</div>
          <div style={{fontSize: 100, fontWeight: 900, color: C.liab}}>{pct(N.guar_share * prog(f, cue(2) + 10, 40), 1)}</div>
        </Card>
        <div style={{flex: 1}}>
          <HBar f={f} at={cue(2) + 30} label="원리금보장 수익률 (2025)" value={N.guar_ret} max={18} text={`${N.guar_ret}%`} color={C.muted} textWidth={200} />
          <HBar f={f} at={cue(2) + 50} label="실적배당 수익률 (2025)" value={N.perf_ret} max={18} text={`${fmt(N.perf_ret, 2)}%`} color={C.floor} textWidth={200} />
        </div>
      </div>
    </Scene>
  );
};

/* S2 디폴트옵션 · TDF */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const people = Array.from({length: 10});
  const stable = Math.round(10 * N.default_stable);
  return (
    <Scene t={t} eyebrow={EB} title="디폴트옵션은 목표를 묻지 않고 대신 정해 주는 장치입니다" sub="사전지정운용제도 — 2022.7.12 시행, 2023.7 본격 적용 · DC · IRP 미지시 적립금을 자동 운용">
      <Card style={{...rise(f, cue(1))}}>
        <div style={{fontSize: 30, color: C.muted}}>실제 선택 (2025 말) — 적립금 {N.default_aum}조 중 안정형(원리금보장) {pct(N.default_stable, 1)}</div>
        <div style={{display: 'flex', gap: 18, marginTop: 18}}>
          {people.map((_, i) => (
            <div key={i} style={{flex: 1, height: 90, borderRadius: 14, background: i < stable ? C.muted : C.floor, opacity: prog(f, cue(1) + 10 + i * 5, 10), display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 26, fontWeight: 800, color: C.bg}}>
              {i < stable ? '보장' : '투자'}
            </div>
          ))}
        </div>
        <div style={{fontSize: 30, fontWeight: 800, color: C.liab, marginTop: 14}}>열에 여덟이 원리금보장 — 목표에 못 미친다</div>
      </Card>
      <div style={{display: 'flex', gap: 24, marginTop: 24}}>
        <Card style={{flex: 1, ...rise(f, cue(2))}}>
          <div style={{fontSize: 30, fontWeight: 800}}>한국 TDF — 나이 하나로 줄이는 글라이드패스</div>
          <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>목표 금액 · 확률을 묻지 않고, Floor도 없다 · 평균 총보수 {N.tdf_fee}%</div>
        </Card>
        <Card style={{width: 520, textAlign: 'center', ...rise(f, cue(2) + 20)}}>
          <div style={{fontSize: 26, color: C.muted}}>2022년 국내 TDF2025 · TDF2045</div>
          <div style={{fontSize: 56, fontWeight: 900, color: C.liab, transform: `scale(${pop(f, cue(2) + 40)})`}}>
            −14.0% · −16.8%
          </div>
        </Card>
      </div>
    </Scene>
  );
};

/* S3 로보 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const ev = [
    ['2015~18', '독립 로보 등장 — 초기 전략은 사실상 디지털 TDF'],
    ['2019~20', '목표 기반 전환 시도 — COVID 급락이 첫 스트레스 테스트'],
    ['2021~24', '적립금 성장, 그러나 자문형 한계 — 일임 불가의 벽'],
    ['2024.12~', '혁신금융서비스로 IRP 일임 지정 — 2025.3 첫 출시'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="한국 GBI의 병목은 기술이 아니라 제도였고 그 제도가 막 열렸습니다" sub="에피소드 — 한국 로보의 GBI 도전: TDF 모방에서 일임 시대로">
      <div style={{display: 'flex', gap: 30}}>
        <div style={{flex: 1}}>
          {ev.map((e, i) => (
            <div key={e[0]} style={{display: 'flex', gap: 22, alignItems: 'center', marginBottom: 22, ...rise(f, cue(0) + 10 + i * 18)}}>
              <div style={{width: 170, fontSize: 32, fontWeight: 900, color: i === 3 ? C.floor : C.accent}}>{e[0]}</div>
              <div style={{fontSize: 28}}>{e[1]}</div>
            </div>
          ))}
        </div>
        <Card style={{width: 480, textAlign: 'center', alignSelf: 'flex-start', ...rise(f, cue(1))}}>
          <div style={{fontSize: 28, color: C.muted}}>국내 로보 운용금액 (2026.3)</div>
          <div style={{fontSize: 64, fontWeight: 900, color: C.floor, whiteSpace: 'nowrap'}}>1조 2,760억</div>
          <div style={{fontSize: 26, color: C.muted}}>전년 대비 +29%</div>
        </Card>
      </div>
      <div style={{fontSize: 30, fontWeight: 800, color: C.accent, marginTop: 8, ...rise(f, cue(2))}}>IRP 일임 — 로보가 규칙(쿠션 비례 · Floor 재설정)을 승인 없이 실행</div>
    </Scene>
  );
};

/* S4 발전 방향 세 줄 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="발전 방향은 세 줄 — 목표를 묻고, 목표로 운용하고, 소득으로 돌려준다" sub="제안 · 교육용 — 줄마다 이번 강의의 개념 하나와 연결한다">
      <div style={{width: 1728}}>
        <RevealTable
          f={f}
          size={28}
          cols={['지금', '→ 바꾼다면', '강의 개념']}
          widths={[0.9, 1.2, 1]}
          rows={[
            {cells: ['수익률 공시', '목표 달성 확률 · Floor 확보율 공시', '① P(W < G) · ③ 필요 자본'], at: cue(0) + 10},
            {cells: ['위험 등급 디폴트', '목표 기반 디폴트 — GHP + 쿠션 × m', '④⑤ Floor · 승수 · ③ 방법 2'], at: cue(1) + 10},
            {cells: ['적립 단계만 (일시금 87%)', '인출 단계까지 — 소득 Floor 매년 재측정', '⑤⑥ Flexicure 재설정'], at: cue(2) + 10},
          ]}
        />
      </div>
      <div style={{fontSize: 26, color: C.muted, marginTop: 18, ...rise(f, cue(2) + 40)}}>도입에는 공시 기준 · 디폴트옵션 상품 승인 · 일임 규정의 변경이 필요 (제안)</div>
    </Scene>
  );
};

export const M8E07 = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M8E07_TOTAL = T.total;
