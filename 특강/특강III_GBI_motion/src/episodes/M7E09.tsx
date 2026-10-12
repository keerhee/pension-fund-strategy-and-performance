import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {Scene, SceneT, cueOf} from '../lib/Scene';
import {Card, HBar} from '../lib/ui';
import {pop, prog, rise, typed} from '../lib/anim';
import {makeEpisode} from '../lib/episode';
import N from '../data/M7E09.numbers.json';
import T from '../data/M7E09.timing.json';

const EB = 'BAF.60080 · W06 LDI · ⑧ 실습 · LDI 미니 시뮬레이터';
const MONO = "'JetBrains Mono', 'D2Coding', 'Noto Sans Mono CJK KR', monospace";

const Term: React.FC<{text: string; style?: React.CSSProperties; caret?: boolean}> = ({text, style, caret = true}) => (
  <div
    style={{
      background: '#050D1A',
      border: `1px solid ${C.line}`,
      borderRadius: 14,
      padding: '22px 28px',
      fontFamily: MONO,
      fontSize: 30,
      color: '#CFE3FF',
      whiteSpace: 'pre-wrap',
      ...style,
    }}
  >
    <span style={{color: C.floor}}>&gt; </span>
    {text}
    {caret ? <span style={{background: C.text, marginLeft: 2}}>&nbsp;</span> : null}
  </div>
);

/* S0 세 박스 */
const S0: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const boxes = [
    {k: '[입력] 프롬프트', v: '입력창에 붙여 넣는 지시문 — 원하는 바를 한국어로', s: '코드 지식 불필요', c: C.asset},
    {k: '[입력] 명령어', v: '“실행해줘” 수준의 한 줄 — 터미널을 몰라도 된다', s: '한 줄이면 충분', c: C.accent},
    {k: '[출력] 생성물', v: '코드 · 표 · 차트 · 해석 — 읽고 개선을 지시한다', s: '판단은 사람의 몫', c: C.floor},
  ];
  return (
    <Scene t={t} eyebrow="BAF.60080 · W06 LDI · E09" title="실습에서는 세 가지 박스만 구분하면 됩니다" sub="코딩 경험이 없어도 된다 — 원하는 바를 말로 설명하고 결과를 검토한다">
      <div style={{display: 'flex', gap: 28}}>
        {boxes.map((b, i) => (
          <Card key={b.k} style={{flex: 1, borderTop: `6px solid ${b.c}`, ...rise(f, cue(1) + i * 16)}}>
            <div style={{fontSize: 36, fontWeight: 800, color: b.c}}>{b.k}</div>
            <div style={{fontSize: 28, marginTop: 12}}>{b.v}</div>
            <div style={{fontSize: 28, color: C.muted, marginTop: 16}}>{b.s}</div>
          </Card>
        ))}
      </div>
      <div style={{fontSize: 34, fontWeight: 800, color: C.accent, marginTop: 34, ...rise(f, cue(0) + 10)}}>
        실습 목표 — IC에서 쓸 숫자 근거를 20분 만에 직접 만든다
      </div>
    </Scene>
  );
};

/* S1 네 단계 + 개선 루프 */
const S1: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const steps = [
    ['① 메타프롬프트', '원하는 바를 말로'],
    ['② 코드', 'Claude가 작성'],
    ['③ 실행', '“실행해줘” 한 줄'],
    ['④ 결과', '표 · 차트 · 해석'],
  ];
  return (
    <Scene t={t} eyebrow={EB} title="메타프롬프트에서 결과까지 네 단계를 말로 반복합니다" sub="[입력] 메타프롬프트 → [출력] 코드 → [입력] 실행 → [출력] 결과 — 그리고 말로 개선">
      <div style={{display: 'flex', gap: 14, alignItems: 'center'}}>
        {steps.map((s, i) => (
          <React.Fragment key={s[0]}>
            <Card style={{flex: 1, textAlign: 'center', ...rise(f, cue(0) + 10 + i * 20)}}>
              <div style={{fontSize: 34, fontWeight: 800}}>{s[0]}</div>
              <div style={{fontSize: 26, color: C.muted, marginTop: 6}}>{s[1]}</div>
            </Card>
            {i < 3 ? <div style={{fontSize: 40, color: C.accent, opacity: prog(f, cue(0) + 20 + i * 20)}}>→</div> : null}
          </React.Fragment>
        ))}
      </div>
      <div style={{fontSize: 30, color: C.muted, margin: '34px 0 12px', ...rise(f, cue(1))}}>개선 루프 — ④에서 ①로 돌아가 말로 고친다</div>
      <Term text={typed('버퍼를 250bp로 바꿔 다시 돌려줘', f, cue(1) + 20, 10)} style={{opacity: prog(f, cue(1))}} />
      <div style={{fontSize: 36, fontWeight: 800, color: C.accent, marginTop: 30, ...rise(f, cue(1) + 90)}}>코드는 Claude가, 판단은 사람이 합니다</div>
    </Scene>
  );
};

/* S2 시뮬레이터 명세 */
const S2: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  const items = [
    ['A', '케이스 재현 — w6m7_build.py → w6m7_compute.py, compute_log.txt와 대조', cue(0) + 10],
    ['B', '가상 부채(할인율 3.3%) — PV · 듀레이션 · DV01 · 금리 ±100bp 민감도', cue(0) + 40],
    ['C', '출발 FR 90% · 헤지 0 / 50 / 100%의 ΔFR', cue(0) + 70],
    ['D', '레버리지 LDI(현물 1/3 + 스왑 2/3) · +50bp × 3일 → 버퍼 100 / 150 / 250bp 비교', cue(1)],
  ] as const;
  return (
    <Scene t={t} eyebrow={EB} title="LDI 미니 시뮬레이터는 네 단계로 케이스와 위기를 재현합니다" sub="부채 모델링 + 면역화 + 위기 재현을 코드로 (약 20분) — 명세는 실습데이터 덱">
      {items.map(([k, v, at]) => (
        <div key={k} style={{display: 'flex', gap: 24, alignItems: 'center', marginBottom: 18, ...rise(f, at)}}>
          <div
            style={{
              width: 64,
              height: 64,
              borderRadius: 14,
              background: k === 'D' ? C.liab : C.panel,
              border: `2px solid ${C.accent}`,
              fontSize: 36,
              fontWeight: 900,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            {k}
          </div>
          <div style={{fontSize: 32}}>{v}</div>
        </div>
      ))}
      <Term text={typed('실행해서 A~D 결과를 모두 보여줘. D는 버퍼 100bp vs 250bp를 비교해줘.', f, cue(1) + 50, 14)} style={{marginTop: 18, opacity: prog(f, cue(1) + 40)}} />
    </Scene>
  );
};

/* S3 결과 D */
const S3: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="버퍼 150bp 차이가 강제매도 여부를 가릅니다" sub="[출력] D 위기 시뮬레이션 — 가상 부채 · 금리 +50bp × 3일 · 레버리지 3배">
      <div style={{display: 'flex', gap: 40}}>
        <div style={{flex: 1}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab, ...rise(f, cue(0))}}>버퍼 100bp — 3일차 증거금 고갈</div>
          <HBar f={f} at={cue(0) + 20} label="강제매도" value={N.b100.fire} max={0.12} text="8.7%" color={C.liab} />
          <HBar f={f} at={cue(0) + 40} label="헤지 비율 (축소 후)" value={N.b100.hedge} max={1} text="89%" color={C.asset} />
          <HBar f={f} at={cue(0) + 60} label="적립비율 변화" value={-N.b100.dfr} max={3} text="−2.7%p" color={C.liab} />
        </div>
        <div style={{flex: 1}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor, ...rise(f, cue(1))}}>버퍼 250bp — 증거금 충당</div>
          <HBar f={f} at={cue(1) + 20} label="강제매도" value={N.b250.fire} max={0.12} text="0%" color={C.floor} />
          <HBar f={f} at={cue(1) + 60} label="적립비율 변화" value={-N.b250.dfr} max={3} text="−0.9%p" color={C.floor} />
        </div>
      </div>
      <div style={{fontSize: 30, fontWeight: 700, color: C.accent, marginTop: 10, transform: `scale(${pop(f, cue(2) + 10)})`}}>
        영국 규제 250bp의 근거 · 단일 기금 모형 — 시장 충격(Doom Loop)을 넣으면 손실은 더 커진다
      </div>
    </Scene>
  );
};

/* S4 발언 번역 */
const S4: React.FC<{t: SceneT}> = ({t}) => {
  const f = useCurrentFrame();
  const cue = cueOf(t);
  return (
    <Scene t={t} eyebrow={EB} title="시뮬레이션 숫자는 부채 언어의 IC 발언으로 번역해야 힘이 생깁니다" sub="결과 읽기 — 시뮬레이션은 재료일 뿐, 판단과 문장은 사람의 몫이다">
      <div style={{display: 'flex', gap: 34}}>
        <Card style={{flex: 1, borderTop: `6px solid ${C.liab}`, ...rise(f, cue(0))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.liab}}>나쁜 발언 — 수익률 언어</div>
          {['“LDI는 위험해 보입니다”', '“수익률이 떨어질 것 같다”', '근거 없는 형용사'].map((x) => (
            <div key={x} style={{fontSize: 32, marginTop: 16, textDecoration: f > cue(1) ? 'line-through' : 'none', color: f > cue(1) ? C.muted : C.text}}>
              {x}
            </div>
          ))}
          <div style={{fontSize: 28, color: C.liab, marginTop: 18}}>즉시 반박당한다</div>
        </Card>
        <Card style={{flex: 1, borderTop: `6px solid ${C.floor}`, ...rise(f, cue(1))}}>
          <div style={{fontSize: 34, fontWeight: 800, color: C.floor}}>좋은 발언 — 부채 언어 + 숫자</div>
          {['“100bp면 3일차에 고갈”', '“250bp면 강제매도 0%”', '시뮬레이션 근거'].map((x, i) => (
            <div key={x} style={{fontSize: 32, marginTop: 16, ...rise(f, cue(1) + 20 + i * 14)}}>
              {x}
            </div>
          ))}
          <div style={{fontSize: 28, color: C.floor, marginTop: 18}}>반박하려면 숫자가 필요하다</div>
        </Card>
      </div>
      <div style={{fontSize: 36, fontWeight: 800, color: C.accent, marginTop: 30, ...rise(f, cue(1) + 80)}}>AI가 계산을, 사람이 판단을 — AI-Native 운용역의 분업</div>
    </Scene>
  );
};

export const M7E09 = makeEpisode(T, [S0, S1, S2, S3, S4]);
export const M7E09_TOTAL = T.total;
