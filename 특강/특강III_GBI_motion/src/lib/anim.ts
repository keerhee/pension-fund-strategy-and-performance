import {interpolate, spring, Easing} from 'remotion';

const ease = Easing.bezier(0.22, 1, 0.36, 1);

/** from 프레임부터 dur 동안 0→1 (easeOut) */
export const prog = (f: number, from: number, dur = 18) =>
  interpolate(f, [from, from + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: ease,
  });

/** 튀어나오는 스프링 0→1 */
export const pop = (f: number, from: number, fps = 30) =>
  spring({frame: f - from, fps, config: {damping: 14, stiffness: 140}});

/** a→b 사이 값 보간 (p: 0..1) */
export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;

/** 등장: 투명도 + 아래에서 올라오기 */
export const rise = (f: number, from: number, dist = 24, dur = 16) => {
  const p = prog(f, from, dur);
  return {opacity: p, transform: `translateY(${(1 - p) * dist}px)`};
};

export const fmt = (v: number, d = 1) =>
  v.toLocaleString('ko-KR', {minimumFractionDigits: d, maximumFractionDigits: d});
export const pct = (v: number, d = 0) => `${fmt(v * 100, d)}%`;
export const signed = (v: number, d = 1) => `${v > 0 ? '+' : v < 0 ? '−' : ''}${fmt(Math.abs(v), d)}`;

/** 감쇠 진동 (도장·충격) */
export const shake = (f: number, from: number, amp = 8, dur = 12) => {
  const t = f - from;
  if (t < 0 || t > dur) return 0;
  return amp * Math.sin(t * 2.2) * (1 - t / dur);
};

/** 한 글자씩 타이핑 */
export const typed = (text: string, f: number, from: number, cps = 18, fps = 30) => {
  const n = Math.max(0, Math.floor(((f - from) / fps) * cps));
  return text.slice(0, n);
};
