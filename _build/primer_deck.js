// 프라이머 덱 공용 빌더 — 주차별 스크립트는 내용(spec)만 넘긴다.
// 룰북: .claude/skills/zeroone-pitch-deck/SKILL.md
//  · 제목은 주장문("~합니다"), 모든 본문 슬라이드는 결론 한 줄(punch/banner)로 끝난다
//  · 그림 비율은 PNG에서 직접 읽는다 — 손으로 적으면 찌그러진다
const fs = require("fs");
const path = require("path");
const T = require(
  "/Users/keerhee/Project/.claude/skills/zeroone-pitch-deck/scripts/template.js");
const C = T.C;

const ROOT = path.join(__dirname, "..");

/** PNG 헤더(IHDR)에서 가로/세로를 읽어 비율을 돌려준다. */
function ratioOf(p) {
  const b = fs.readFileSync(p);
  if (b.toString("ascii", 1, 4) !== "PNG") throw new Error("PNG이 아닙니다: " + p);
  return b.readUInt32BE(16) / b.readUInt32BE(20);
}

function build(spec) {
  const ART = (n) => {
    const p = path.join(__dirname, "_art", spec.art, n);
    if (!fs.existsSync(p)) throw new Error("그림이 없습니다: " + p);
    return p;
  };
  let page = 1;

  // ── 표지 ──
  T.setBrand({ eyebrow: spec.eyebrow, wordmark: "BAF.60080" });
  T.cover(T.slide(true), {
    title: spec.coverTitle,
    sub: spec.coverSub,
    org: "연기금 운용전략과 성과평가 · 2026 가을학기",
    chain: spec.chain,
  });

  // ── 목차 ──
  page = 2;
  {
    const s = T.slide();
    T.head(s, { title: spec.agendaTitle, page });
    T.agenda(s, spec.agenda, { y: 2.14 });
    T.banner(s, spec.agendaBanner, { y: 6.10 });
  }

  // ── 본문 ──
  for (const it of spec.slides) {
    page += 1;
    if (it.type === "divider") {
      T.divider(T.slide(true), { num: it.num, title: it.title, sub: it.sub, page });
      continue;
    }
    if (it.type === "closing") {
      T.closing(T.slide(true), {
        statements: it.statements, message: it.message,
        contacts: it.contacts, note: it.note,
      });
      continue;
    }
    const s = T.slide();
    const cy = T.head(s, { title: it.title, page });

    if (it.type === "fig") {
      T.figImg(s, ART(it.file), ratioOf(ART(it.file)), { y: cy + 0.06, bottom: 5.86 });

    } else if (it.type === "eq") {
      // 한 줄짜리 납작한 식은 넓은 카드에서 높이에 눌려 작아진다.
      // 룰북 §7.5.1대로 높이를 키우지 말고 카드 폭을 좁힌다.
      const h = it.h || 2.10, pad = 0.34, ratio = ratioOf(ART(it.file));
      const availH = h - pad * 1.7 - (it.cap ? 0.38 : 0);
      const full = T.CW - pad * 2;
      const eqW = Math.min(full, availH * ratio);
      let w = it.w || T.CW;
      if (!it.w && eqW < full * 0.72) {
        // 좁히되 카드 머리말(cap)이 한 줄로 들어갈 폭은 남긴다
        const capNeed = it.cap
          ? T.wUnits(it.cap) * (T.S.label + 1) / 72 + pad * 2 + 0.24 : 0;
        w = Math.min(T.CW, Math.max(eqW + pad * 2 + 0.5, capNeed));
      }
      const y2 = T.eqInCard(s, {
        y: cy + 0.06, h, kind: "ghost", cap: it.cap, w,
        x: T.M + (T.CW - w) / 2, path: ART(it.file), ratio,
      });
      if (it.cards) T.cards(s, it.cards, { y: y2 + 0.26, h: it.cardH || 1.16 });

    } else if (it.type === "cards") {
      T.cards(s, it.cards, { y: cy + 0.14, h: it.h || 3.30 });

    } else if (it.type === "table") {
      T.dataTable(s, it.head, it.rows,
        { y: cy + (it.dy != null ? it.dy : 0.06), rowH: it.rowH || 0.66,
          widths: it.widths, emph: it.emph });

    } else {
      throw new Error("모르는 슬라이드 유형: " + it.type);
    }

    if (it.punch) T.punch(s, it.punch, { y: it.punchY || 6.00 });
    if (it.banner) T.banner(s, it.banner, { y: it.bannerY || 6.06 });
    if (it.note) T.note(s, it.note, { y: it.noteY || 6.44 });
  }

  const out = path.join(ROOT, spec.out);
  return T.save(out).then(() => { console.log("저장:", path.basename(out)); return out; });
}

module.exports = { build, C, T, ratioOf };
