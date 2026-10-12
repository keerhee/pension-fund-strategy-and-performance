import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, Chip} from '../lib/ui';
import {pop, prog, rise} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import T from '../data/M8E00.timing.json';

const EB = 'BAF.60080 · W06 GBI · 도입';

/* S0 LDI → GBI 다리 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const rows = [
    ['지켜야 할 것', '부채 L (연금 약속)', '목표 G (노후 생활비)'],
    ['지키는 자산', '부채 벤치마크 (장기채)', 'GHP (물가연동국채 등)'],
    ['버틸 여유', '잉여금 S = A − L', '쿠션 A − F'],
    ['수익 추구', 'Return-Seeking', 'PSP (Performance-Seeking)'],
    ['위험의 뜻', '적립비율이 떨어질 위험', '목표를 못 이룰 확률'],
  ];
  const sw = prog(f, cue(2), 30);
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 GBI · E00" title="GBI — 목표기반투자" sub="Goal-Based Investing · 개인의 노후 생활비 약속은 연기금의 부채와 같다">
      <Card style={{padding: '6px 0', ...rise(f, cue(1))}}>
        <div style={{display: 'flex', padding: '14px 30px', fontSize: 30, fontWeight: 800, borderBottom: `1px solid ${C.line}`}}>
          <span style={{flex: 0.8, color: C.muted}}>구분</span>
          <span style={{flex: 1, color: C.liab, opacity: 1 - 0.5 * sw}}>LDI (기관 · M7)</span>
          <span style={{flex: 1, color: C.floor, opacity: 0.4 + 0.6 * sw}}>GBI (개인 · M8)</span>
        </div>
        {rows.map((r, i) => (
          <div key={r[0]} style={{display: 'flex', padding: '15px 30px', fontSize: 31}}>
            <span style={{flex: 0.8, color: C.muted}}>{r[0]}</span>
            <span style={{flex: 1, opacity: 1 - 0.5 * sw}}>{r[1]}</span>
            <span style={{flex: 1, fontWeight: 700, ...rise(f, cue(2) + i * 10)}}>{r[2]}</span>
          </div>
        ))}
      </Card>
    </Scene>
  );
};

/* S1 같은 65세 · 같은 5억 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const split = prog(f, cue(2), 30);
  const person = (name: string, tag: string, items: string[], c: string, dir: number) => (
    <Card style={{flex: 1, borderTop: `6px solid ${c}`, opacity: rise(f, cue(0)).opacity, transform: `translateX(${dir * split * 20}px)`}}>
      <div style={{fontSize: 40, fontWeight: 800}}>{name}</div>
      <div style={{fontSize: 28, color: C.muted}}>65세 · 금융자산 5억</div>
      <div style={{fontSize: 34, fontWeight: 800, color: c, marginTop: 14, opacity: prog(f, cue(1))}}>{tag}</div>
      {items.map((x, i) => (
        <div key={x} style={{fontSize: 29, marginTop: 10, ...rise(f, cue(1) + 10 + i * 10)}}>
          • {x}
        </div>
      ))}
    </Card>
  );
  return (
    <Scene t={t} eyebrow={EB} title="같은 65세, 같은 5억이라도 목표가 다르면 같은 답일 수 없습니다" sub="DC 가입자에게 “부채”가 없는 것이 아니라 각자의 부채가 다르다">
      <div style={{display: 'flex', gap: 40}}>
        {person('이순자 씨', '안정 최우선', ['NPS 월 150만', '월 300만 — 부족 불가', '손주 교육은 여유가 되면'], C.floor, -1)}
        {person('김영수 씨', '성장 지향', ['임대 월 200만', '기본 생활은 임대로 충분', '자녀 증여 · 세계여행'], C.accent, 1)}
      </div>
      <div style={{display: 'flex', justifyContent: 'center', marginTop: 34, gap: 30, alignItems: 'center', ...rise(f, cue(2))}}>
        <Chip color={C.muted} style={{color: C.text, textDecoration: f > cue(2) + 40 ? 'line-through' : 'none'}}>
          TDF — 같은 나이면 같은 비중
        </Chip>
        <span style={{fontSize: 40, color: C.accent}}>→</span>
        <Chip color={C.floor} style={{transform: `scale(${pop(f, cue(2) + 40)})`}}>
          GBI — 목표가 다르면 다른 비중
        </Chip>
      </div>
    </Scene>
  );
};

/* S2 세 메시지 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const msgs = [
    {k: '목표가 다르면 포트폴리오도 달라야 한다', v: '목표 정의 · 우선순위 · 확률의 3원칙', c: C.asset},
    {k: '3계층 버킷 — 계좌마다 달성 확률을 건다', v: 'Safety ≥ 95% → Market ≥ 70% → Aspirational ≥ 30%', c: C.floor},
    {k: 'Flexicure — 안정과 유연을 동시에', v: 'RB → GHP → Floor → 쿠션(A − F)에 비례해 PSP를 동적 배분', c: C.accent},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="이번 주가 던지는 메시지는 세 가지입니다" sub="은퇴 투자의 “최적해”는 누구의 최적해인가">
      {msgs.map((m, i) => (
        <Card key={m.k} style={{display: 'flex', gap: 30, alignItems: 'center', marginBottom: 22, ...rise(f, cue(i))}}>
          <div style={{width: 76, height: 76, borderRadius: 38, background: m.c, color: C.bg, fontSize: 42, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
            {i + 1}
          </div>
          <div>
            <div style={{fontSize: 38, fontWeight: 800, color: m.c}}>{m.k}</div>
            <div style={{fontSize: 28, color: C.muted, marginTop: 6}}>{m.v}</div>
          </div>
        </Card>
      ))}
    </Scene>
  );
};

/* S3 열 개 단원 */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const groups = [
    {k: '1교시', u: ['① 목표와 위험', '② 심리계정', '③ 필요 자본']},
    {k: '2교시', u: ['④ Floor 만들기', '⑤ 쿠션과 승수', '⑥ Floor 운용 규칙']},
    {k: '3교시', u: ['⑦ GBI와 현실 세계', '⑧ 기관의 GBI · H대']},
    {k: '4교시', u: ['⑨ 실습 · GBI 설계기', '⑩ 모의 IC']},
  ];
  return (
    <Scene t={t} eyebrow={EB} title="열 개 단원은 오후 IC 두 안건의 숫자로 모입니다" sub="단원마다 푸는 질문이 하나씩 있다">
      {groups.map((g, i) => (
        <div key={g.k} style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 22, ...rise(f, cue(0) + i * 16)}}>
          <div style={{width: 120, fontSize: 30, color: C.accent, fontWeight: 700}}>{g.k}</div>
          <div style={{display: 'flex', gap: 12, flexWrap: 'wrap'}}>
            {g.u.map((u) => (
              <Chip key={u} color={C.muted} style={{color: C.text}}>
                {u}
              </Chip>
            ))}
          </div>
        </div>
      ))}
      <div style={{display: 'flex', gap: 20, marginTop: 30, ...rise(f, cue(1))}}>
        {['Floor', '쿠션', '달성 확률'].map((k) => (
          <Chip key={k} color={C.floor} style={{fontSize: 36, padding: '12px 36px'}}>
            {k}
          </Chip>
        ))}
        <span style={{fontSize: 34, fontWeight: 800, color: C.accent, alignSelf: 'center'}}>— 이번 주의 공용어</span>
      </div>
    </Scene>
  );
};

/* S4 두 안건 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const card = (no: string, k: string, nums: string[], items: string[], at: number) => (
    <Card style={{flex: 1, ...rise(f, at)}}>
      <div style={{fontSize: 28, color: C.accent, fontWeight: 800}}>{no}</div>
      <div style={{fontSize: 38, fontWeight: 800, marginTop: 4}}>{k}</div>
      <div style={{display: 'flex', gap: 12, marginTop: 18}}>
        {nums.map((n, i) => (
          <Chip key={n} color={C.floor} style={{transform: `scale(${pop(f, at + 20 + i * 10)})`}}>
            {n}
          </Chip>
        ))}
      </div>
      {items.map((x) => (
        <div key={x} style={{fontSize: 27, color: C.muted, marginTop: 14}}>
          • {x}
        </div>
      ))}
    </Card>
  );
  return (
    <Scene t={t} eyebrow={EB} title="세 시간 뒤 여러분은 두 안건에 표결합니다" sub="평가 기준은 공통 — 목표 언어(Floor · 쿠션 · 달성 확률)로 논증했는가">
      <div style={{display: 'flex', gap: 34}}>
        {card('제1호', '디폴트옵션 Flexicure형 도입', ['Floor', 'm 상한', '총보수'], ['Cash Trap — 쿠션 0으로 회복에 못 탐', 'LTCM · 2022 TDF 반면교사'], cue(0))}
        {card('제2호', 'H대학기금 — 세 숫자', ['x 비유동', 'y 유동', 'z 지출률'], ['모방 3장벽 — 접근권 · 시간 지평 · 인력', 'GBI로 읽기 — Floor · GHP · 위험 예산'], cue(1))}
      </div>
    </Scene>
  );
};

export const M8E00 = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M8E00_TOTAL = T.total;
