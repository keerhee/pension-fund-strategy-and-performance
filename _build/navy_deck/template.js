/* ============================================================================
 * report-navy-deck — 검증된 헬퍼 템플릿 (v1.7)
 *
 * v1.7 변경점 (AI-Native 에이전트 구현 덱 지원):
 *   1) 세 산출물 박스 헬퍼 정식 편입 — promptBoxIn(앰버=입력 프롬프트) /
 *      cmdBox(블루 헤더=명령어) / outputBox(네이비 헤더=출력·생성물). 박스 종류를
 *      색·헤더로 못박고, 헤더에 [입력]/[출력] 접두 라벨을 강제한다.
 *   2) 메타프롬프트 사슬([입력]메타프롬프트→[출력]설정파일→[입력]실행→[출력]결과)을
 *      문과·입문생 표준 패턴으로 §3.6에 편입. 초보자는 .md/.json을 직접 안 쓰고
 *      메타프롬프트로 Claude가 생성하게 한다.
 *   3) 색 의미 확장 — 앰버=입력 프롬프트, 블루 헤더=명령어, 네이비 헤더=출력.
 *      본문 오렌지 금지 원칙은 유지.
 *   (이전) v1.6.1: figureSlide / figurePanelSlide 실제 구현.
 *
 * v1.6.1 변경점:
 *   - figureSlide / figurePanelSlide 헬퍼를 실제 구현(정식 편입). 그동안 SKILL.md
 *     §2.1·§4가 둘을 헬퍼로 안내했으나 코드에는 없어(문서-코드 불일치) 그림 슬라이드를
 *     매번 head+figImg로 손수 짜야 했다. (A) figureSlide = head+figImg 래퍼,
 *     (B) figurePanelSlide = 좌측 tint 해설 패널 + 우측 원본 이미지(hairline 테두리).
 *
 * v1.6 변경점:
 *   1) qRows가 field 20pt 룰을 어기던 버그 수정 — 질문 본문이 S.qT-2(=16pt)로
 *      나오던 것을 별도 토큰(qNum/qText/qTag)으로 분리. field에서 질문 본문 20pt,
 *      Q라벨 22pt, 태그 16pt(모두 14pt 하한 충족). field가 진짜 기본값이 되도록
 *      qRows의 기본 rowH도 모드에 맞춰 자동 조정(field 1.18 / theory 0.84).
 *   2) eqInCard 헬퍼 정식 편입 — 회색 수식 카드(panelGray) + 수식 PNG를 카드 안
 *      가로·세로 중앙에 배치. 수식 슬라이드의 사실상 표준 패턴이라 손으로 매번
 *      그리던 것을 헬퍼로 묶음.
 *   (이전) v1.5: figImg(그림 꽉 채움) 추가 · divider 번호 150->88pt.
 * v1.4 변경점:
 *   1) 커스텀 슬라이드 헬퍼를 정식 편입: cover / divider / statCards /
 *      stepCards / qRows. 모두 S(모드) 값을 따른다 → field로 두면 20pt대로 커짐.
 *   2) SIZES에 커스텀 헬퍼용 크기(step·statCap·qT) 추가.
 *   3) wtable에 폰트 오버라이드 인자 추가 — 행 많은 인덱스성 표(7행+)는
 *      14pt 하한을 지키며 16~17pt로 낮춰 세로 넘침을 방지(field에서 특히).
 *   (이전) v1.3: field/theory 본문 스케일 모드, panel 상하 균형, 부제↔본문 충돌 방지.
 * ========================================================================== */

const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
p.layout = "W";

// ---- 컬러 (절대 골격) -------------------------------------------------------
const C = {
  navy:"1B2C5E", white:"FFFFFF", orange:"E65100", blue:"2E5BAA", green:"3FA36F",
  body:"3B4252", muted:"6B7280", hair:"D6D6DB",
  panelBlue:"EAF1FB", panelGreen:"E6F5F0", panelGray:"F4F5F9",
  coverSub:"CADCFC", coverSub2:"8FA8D8",
};
const P = { acc:"C77700", fill:"FCF2E0", ink:"2A2622" };
const F = "Noto Sans CJK KR";
const MONO = "Noto Sans Mono CJK KR";

// ---- 본문 스케일 모드 -------------------------------------------------------
// "field" = 본문 20pt (재직자·현장·취준생·MBA 강의 기본 — 압도적 선호). 빔 가독성 최우선.
// "theory" = 16pt (수식·표·정보밀도가 매우 높은 이론 덱에만 한정). ★v1.9.7 최소 폰트 16pt 상향.
// ★ field가 하드 기본값이다. 기준 덱이 작아 보인다는 이유로 임의로 theory로 바꾸지 말 것.
//   모든 본문 헬퍼(qRows 포함)는 S(=SIZES[MODE])를 따르므로 field면 자동으로 20pt대가 된다.
const MODE = "field";

const SIZES = {
  field:  { msgT:21, msgD:20, msgN:22, panelT:20, panelB:20, tblH:20, tblB:20,
            bigCard:24, banner:20, caption:18, qLabel:18,
            stepT:18, stepSub:16, stepB:16, stepEg:16, statCap:16, qT:18,
            qNum:22, qText:20, qTag:16 },          // ★v1.9.7 stepSub/stepEg/statCap 16pt 하한 충족
  theory: { msgT:18, msgD:16, msgN:18, panelT:16, panelB:16, tblH:16, tblB:16,
            bigCard:21, banner:16, caption:16, qLabel:16,
            stepT:17, stepSub:16, stepB:16, stepEg:16, statCap:16, qT:16,
            qNum:18, qText:16, qTag:16 },          // ★v1.9.7 theory 최소 16pt (구 14pt대 전면 상향)
};
const S = SIZES[MODE];

// ---- 레이아웃 상수 ----------------------------------------------------------
const LX = 0.62, CW = 12.09;
const CY_SUB = 2.02, CY_NOSUB = 1.74;
let SUBJECT = "과목명";   // 덱마다 setSubject()로 교체 — 특정 브랜드·기관명을 기본값에 넣지 않는다
function setSubject(t){ SUBJECT = t; }

// ---- 기본 도형 --------------------------------------------------------------
function rect(s,x,y,w,h,fill,line){ s.addShape(p.ShapeType.rect,{x,y,w,h,fill:{color:fill},line:line||{type:"none"}}); }
function hline(s,x,y,w,color,wt){ s.addShape(p.ShapeType.line,{x,y,w,h:0,line:{color:color||C.hair,width:wt||1}}); }

// ---- 좌상단 nav 칩 ----------------------------------------------------------
function chip(s,txt,w){
  rect(s,LX,0.34,w,0.40,C.navy);
  s.addText(txt,{x:LX,y:0.34,w,h:0.40,align:"center",valign:"middle",fontFace:F,fontSize:12,bold:true,color:C.white});
}

// ---- 헤더 — 본문 시작 y 반환 -----------------------------------------------
function head(s,chipTxt,chipW,title,sub,pageNo){
  chip(s,chipTxt,chipW);
  s.addText(SUBJECT,{x:CW-3.4+LX,y:0.34,w:3.4,h:0.40,align:"right",valign:"middle",fontFace:F,fontSize:12,color:C.muted});
  s.addText(title,{x:LX,y:0.82,w:CW,h:0.66,fontFace:F,fontSize:32,bold:true,color:C.navy});
  let cy = CY_NOSUB;
  if(sub){ s.addText(sub,{x:LX,y:1.50,w:CW,h:0.42,fontFace:F,fontSize:18,color:C.muted}); cy = CY_SUB; }
  hline(s,LX,7.06,CW,C.hair,1);
  s.addText(SUBJECT,{x:LX,y:7.10,w:8,h:0.30,fontFace:F,fontSize:12,color:C.muted});
  s.addText(String(pageNo),{x:CW-1+LX,y:7.10,w:1,h:0.30,align:"right",fontFace:F,fontSize:12,color:C.muted});
  return cy;
}

// ---- 표지 (모드 무관 고정 크기) --------------------------------------------
function cover(s,o){
  rect(s,0,0,13.333,7.5,C.navy);
  const cw=o.chipW||2.95;
  rect(s,LX,1.55,cw,0.52,C.orange);
  s.addText(o.chip,{x:LX,y:1.55,w:cw,h:0.52,align:"center",valign:"middle",fontFace:F,fontSize:14,bold:true,color:C.white});
  s.addText(o.title,{x:LX,y:2.25,w:CW,h:1.05,fontFace:F,fontSize:46,bold:true,color:C.white});
  s.addText(o.sub1,{x:LX,y:3.45,w:CW,h:0.5,fontFace:F,fontSize:20,bold:true,color:C.coverSub});
  if(o.sub2) s.addText(o.sub2,{x:LX,y:3.95,w:CW,h:0.42,fontFace:F,fontSize:15,color:C.coverSub2});
  s.addShape(p.ShapeType.line,{x:LX,y:4.55,w:3.7,h:0,line:{color:C.orange,width:3}});
  s.addText(o.desc,{x:LX,y:4.85,w:CW-0.5,h:1.0,fontFace:F,fontSize:14.5,color:C.coverSub,lineSpacingMultiple:1.18});
}

// ---- 섹션 디바이더 (네이비 배경, 모드 무관) --------------------------------
function divider(s,o){
  rect(s,0,0,13.333,7.5,C.navy);
  s.addText(o.num,{x:LX,y:2.05,w:4.0,h:1.5,fontFace:F,fontSize:88,bold:true,color:C.orange,valign:"bottom"});
  const cw=o.secW||3.3;
  rect(s,LX+0.06,3.74,cw,0.60,C.orange);
  s.addText(o.sec,{x:LX+0.06,y:3.74,w:cw,h:0.60,align:"center",valign:"middle",fontFace:F,fontSize:18,bold:true,color:C.white});
  s.addText(o.title,{x:LX,y:4.52,w:CW,h:0.9,fontFace:F,fontSize:36,bold:true,color:C.white});
  s.addText(o.desc,{x:LX,y:5.45,w:CW,h:0.5,fontFace:F,fontSize:16,color:C.coverSub2});
  s.addText(String(o.pageNo),{x:CW-1+LX,y:7.10,w:1,h:0.30,align:"right",fontFace:F,fontSize:12,color:C.coverSub2});
}

// ---- 번호 메시지 행 ---------------------------------------------------------
function msgRows(s,rows,startY){
  let y=startY;
  rows.forEach(r=>{
    rect(s,LX,y,0.62,0.62,C.navy);
    s.addText(String(r.n),{x:LX,y,w:0.62,h:0.62,align:"center",valign:"middle",fontFace:F,fontSize:S.msgN,bold:true,color:C.white});
    s.addText(r.t,{x:LX+0.86,y:y-0.04,w:CW-0.86,h:0.40,fontFace:F,fontSize:S.msgT,bold:true,color:C.navy});
    s.addText(r.d,{x:LX+0.86,y:y+0.40,w:CW-0.86,h:0.66,fontFace:F,fontSize:S.msgD,color:C.body,lineSpacingMultiple:1.02});
    y+=1.40;
  });
  return y;
}

// ---- 통계 카드 행 (회색 카드: 큰 navy 숫자 + 캡션) -------------------------
function statCards(s,cards,y,h){
  const n=cards.length,gap=0.24,w=(CW-gap*(n-1))/n;
  cards.forEach((c,i)=>{
    const x=LX+i*(w+gap);
    rect(s,x,y,w,h,C.panelGray);
    s.addText(c.num,{x:x+0.12,y:y+0.18,w:w-0.24,h:h-1.0,align:"center",valign:"middle",fontFace:F,fontSize:c.fs||32,bold:true,color:C.navy});
    s.addText(c.cap,{x:x+0.16,y:y+h-0.92,w:w-0.32,h:0.80,align:"center",valign:"top",fontFace:F,fontSize:S.statCap,color:C.muted,lineSpacingMultiple:1.05});
  });
}

// ---- 단계 카드 행 (컬러 tint: 제목 + 서브 + 설명 + 예시) -------------------
function stepCards(s,cards,y,h){
  const n=cards.length,gap=0.24,w=(CW-gap*(n-1))/n;
  cards.forEach((c,i)=>{
    const x=LX+i*(w+gap), isG=c.tint==="green", tc=isG?C.green:C.blue;
    rect(s,x,y,w,h,isG?C.panelGreen:C.panelBlue);
    s.addText(c.title,{x:x+0.18,y:y+0.22,w:w-0.36,h:0.62,align:"center",valign:"middle",fontFace:F,fontSize:S.stepT,bold:true,color:tc,lineSpacingMultiple:1.0});
    let yy=y+0.90;
    if(c.sub){ s.addText(c.sub,{x:x+0.16,y:yy,w:w-0.32,h:0.34,align:"center",fontFace:F,fontSize:S.stepSub,bold:true,color:C.muted}); yy+=0.40; }
    s.addText(c.body,{x:x+0.18,y:yy,w:w-0.36,h:y+h-yy-(c.eg?0.50:0.20),align:"center",valign:"top",fontFace:F,fontSize:S.stepB,color:C.body,lineSpacingMultiple:1.08});
    if(c.eg) s.addText(c.eg,{x:x+0.16,y:y+h-0.48,w:w-0.32,h:0.36,align:"center",valign:"middle",fontFace:F,fontSize:S.stepEg,italic:true,color:C.muted});
  });
}

// ---- 하단 네이비 배너 -------------------------------------------------------
function banner(s,txt,y){
  rect(s,LX,y,CW,0.66,C.navy);
  s.addText(txt,{x:LX+0.2,y,w:CW-0.4,h:0.66,valign:"middle",fontFace:F,fontSize:S.banner,bold:true,color:C.white});
}

// ---- 가운데 캡션 ------------------------------------------------------------
function caption(s,txt,y){
  s.addText(txt,{x:LX,y,w:CW,h:0.40,align:"center",fontFace:F,fontSize:S.caption,color:C.muted});
}

// ---- 블루/그린 패널 카드 ----------------------------------------------------
// opt(선택): {fs, valign}. ★v1.9 / ★v1.9.3 / ★v1.9.4 —
//   좁은 콜아웃(h<3.0: 미션·매칭·짧은 라벨박스)은 본문을 자동 "top" 정렬한다
//   (라벨 위쪽 침범 = 라벨 겹침을 구조적으로 차단, ★v1.9.3). 본문 폰트 기본값은
//   ★v1.9.4부터 다시 모드값(field=20pt, S.panelB)이다 — 20pt가 현장 가독성이 좋다.
//   빽빽해 20pt가 안 들어가면 opt.fs로 18/16으로 내린다(자동 18 강제는 폐지).
//   큰 2단 분석 패널(h≥3.0)은 기존대로 "middle"·모드값.
//   콜아웃 최소 높이(§1.2.1): h ≳ 0.80 + 줄수×줄높이 + 0.28 (줄높이 20pt≈0.32 / 18pt≈0.29).
//   → 20pt가 기본이므로 좁은 콜아웃 박스는 더 넉넉히 잡아야 한다(아래 경고가 잡아줌).
function panel(s,x,y,w,h,fill,titleColor,title,lines,opt){
  opt=opt||{};
  const narrow=h<3.0;
  const fs=opt.fs||S.panelB;                        // ★v1.9.4 기본 20pt(field)로 원복. opt.fs로 18/16 조정
  const va=opt.valign||(narrow?"top":"middle");     // ★v1.9.3 좁은 콜아웃은 자동 top(라벨 겹침 차단)
  rect(s,x,y,w,h,fill);
  s.addText(title,{x:x+0.28,y:y+0.22,w:w-0.56,h:0.44,valign:"middle",fontFace:F,fontSize:S.panelT,bold:true,color:titleColor});
  const body=lines.map(l=>({text:l,options:{bullet:{code:"2022"},color:C.body,fontFace:F,fontSize:fs,breakLine:true,paraSpaceAfter:8}}));
  const top=y+0.80,bh=h-0.80-0.28;
  s.addText(body,{x:x+0.32,y:top,w:w-0.60,h:bh,valign:va,lineSpacingMultiple:1.04});
  const cpl=Math.max(6,Math.floor((w-0.60)*(fs>=19?3.4:fs>=17?3.8:4.3)));
  let est=0; lines.forEach(l=>{est+=Math.max(1,Math.ceil(String(l).length/cpl));});
  const lh=fs>=19?0.32:fs>=17?0.29:0.27, minH=0.80+est*lh+0.28;
  if(h<minH-0.05) console.warn(`[panel] ${narrow?"좁은 콜아웃":"패널"} 높이 부족: h=${h.toFixed(2)} < 최소 ${minH.toFixed(2)} (줄수≈${est}, fs=${fs}) → 문장을 줄이거나 opt.fs를 낮추세요. (middle 정렬 큰 패널은 위로 넘쳐 제목과 겹칩니다)`);
}

// ---- 회색 면 + 큰 정의 문장 카드 -------------------------------------------
function bigCard(s,txt,y,h){
  rect(s,LX,y,CW,h,C.panelGray);
  s.addText(txt,{x:LX+0.4,y,w:CW-0.8,h,valign:"middle",align:"center",fontFace:F,fontSize:S.bigCard,bold:true,color:C.navy,lineSpacingMultiple:1.05});
}

// ---- 네이비 헤더 + 교차행 표 (fs: 폰트 오버라이드, 14pt 하한) --------------
function wtable(s,rows,x,y,w,colW,rh,fs){
  const fH=fs||S.tblH, fB=fs||S.tblB;
  const tblRows=[];
  tblRows.push(rows[0].map(c=>({text:c,options:{fill:{color:C.navy},color:C.white,bold:true,fontFace:F,fontSize:fH,align:"center",valign:"middle"}})));
  for(let i=1;i<rows.length;i++){
    const bg=(i%2===0)?C.panelGray:C.white;
    tblRows.push(rows[i].map(c=>({text:c,options:{fill:{color:bg},color:C.body,fontFace:F,fontSize:fB,align:"left",valign:"middle",margin:[2,6,2,6]}})));
  }
  s.addTable(tblRows,{x,y,w,colW,rowH:rh,border:{type:"solid",color:C.hair,pt:0.5},autoPage:false});
}

// ---- 토론 Q 행 (Q번호 + 질문 + 우측 태그칩) -------------------------------
// ★ field 20pt 룰 준수: 질문 본문 = S.qText(field 20pt), Q라벨 = S.qNum(22pt),
//   태그 = S.qTag(16pt). 모두 14pt 하한 충족. 기본 rowH는 모드에 맞춰 자동 조정
//   (field는 20pt라 2줄 질문이 흔하므로 1.18, theory는 0.84). 질문이 길어 3줄이면
//   rowH를 직접 키우거나 문장을 줄인다(질문 4개·rowH 1.18이면 startY 2.18에서 안전).
function qRows(s,rows,startY,rowH){
  const rh = rowH || (MODE==="field" ? 1.18 : 0.94);  // ★v1.9.7 theory 16pt에 맞춰 0.84→0.94
  let y=startY;
  rows.forEach(r=>{
    s.addText(r.q,{x:LX,y,w:1.08,h:rh-0.18,valign:"middle",fontFace:F,fontSize:S.qNum,bold:true,color:C.blue});
    s.addText(r.t,{x:LX+1.14,y,w:CW-1.14-2.70,h:rh-0.18,valign:"middle",fontFace:F,fontSize:S.qText,color:C.body,lineSpacingMultiple:1.02});
    rect(s,LX+CW-2.55,y+0.08,2.55,rh-0.36,C.panelGray);
    s.addText(r.tag,{x:LX+CW-2.55,y:y+0.08,w:2.55,h:rh-0.36,align:"center",valign:"middle",fontFace:F,fontSize:S.qTag,bold:true,color:C.navy});
    hline(s,LX,y+rh-0.14,CW,C.hair,0.75);
    y+=rh;
  });
}

// ---- [DEPRECATED ★v1.8] 앰버 프롬프트 박스 ----------------------------------
// ⚠ 신규 덱에서는 쓰지 말 것. promptBoxIn(앰버 + "[입력]" 라벨)으로 통일됐다.
//   구버전 헤더("프롬프트 · {도구} 입력창에 붙여넣기", [입력] 라벨 없음)와의
//   하위호환을 위해서만 남겨두며, 내부적으로 promptBoxIn으로 위임한다.
//   → 입력 박스는 모두 "[입력] 프롬프트 · {도구}" 헤더로 통일된다.
function promptBox(s,x,y,w,h,tool,bodyLines){
  return promptBoxIn(s,x,y,w,h,tool,bodyLines);
}

// ---- 세 산출물 박스 (입력 프롬프트 / 명령어 / 출력·생성물) ★v1.7 -------------
// 박스 종류를 색·헤더로 못박는다. 입력은 [입력], 출력은 [출력]을 접두로 단다.
//   promptBoxIn = 앰버(P.fill/P.acc) — 복붙용 프롬프트·메타프롬프트
//   cmdBox      = 회색 면 + 블루 헤더 — 슬래시·터미널 명령어(한 줄)
//   outputBox   = 회색 면 + 네이비 헤더 — Claude가 생성한 설정파일·결과(생성물)
// 색 의미: 앰버=입력 프롬프트, 블루 헤더=명령어, 네이비 헤더=출력. (본문 오렌지 금지 유지)

// 입력 프롬프트: 앰버 + "[입력] 프롬프트 · {도구}" 헤더 (promptBox의 [입력] 라벨판)
function promptBoxIn(s,x,y,w,h,tool,lines){
  rect(s,x,y,w,h,P.fill); rect(s,x,y,w,0.42,P.acc);
  s.addText("[입력] 프롬프트 · "+tool,{x:x+0.16,y,w:w-0.3,h:0.42,valign:"middle",fontFace:F,fontSize:13,bold:true,color:C.white});
  s.addText(lines.map(l=>({text:l,options:{breakLine:true}})),{x:x+0.22,y:y+0.54,w:w-0.44,h:h-0.66,valign:"top",fontFace:MONO,fontSize:13,color:P.ink,lineSpacingMultiple:1.06});
}

// 명령어: 회색 면 + 블루 헤더 + MONO 15pt navy bold (한 줄 슬래시·터미널 명령)
// label 예: "[입력] 명령어 · Claude Code에 입력"
function cmdBox(s,x,y,w,h,label,cmd){
  rect(s,x,y,w,h,C.panelGray); rect(s,x,y,w,0.42,C.blue);
  s.addText(label,{x:x+0.16,y,w:w-0.3,h:0.42,valign:"middle",fontFace:F,fontSize:13,bold:true,color:C.white});
  s.addText(cmd,{x:x+0.22,y:y+0.50,w:w-0.44,h:h-0.60,valign:"middle",fontFace:MONO,fontSize:15,bold:true,color:C.navy});
}

// 출력(생성물·결과): 회색 면 + 네이비 헤더 + MONO 13pt
// label 예: "[출력] Claude가 생성 · config.json" / "[출력] 결과 · 실행 로그"
function outputBox(s,x,y,w,h,label,lines){
  rect(s,x,y,w,h,C.panelGray); rect(s,x,y,w,0.42,C.navy);
  s.addText(label,{x:x+0.16,y,w:w-0.3,h:0.42,valign:"middle",fontFace:F,fontSize:13,bold:true,color:C.white});
  s.addText(lines.map(l=>({text:l,options:{breakLine:true}})),{x:x+0.22,y:y+0.54,w:w-0.44,h:h-0.66,valign:"top",fontFace:MONO,fontSize:13,color:C.body,lineSpacingMultiple:1.06});
}

// ---- 수식 PNG 배치 ----------------------------------------------------------
function eqC(s,path,w,y,ratio){ s.addImage({path,x:(13.333-w)/2,y,w,h:w/ratio}); }
function eqL(s,path,x,y,w,ratio){ s.addImage({path,x,y,w,h:w/ratio}); }

// ---- 회색 수식 카드 + 수식 PNG 중앙 배치 (수식 슬라이드 표준) ★v1.6 -----------
// 회색 카드(panelGray)를 그리고 그 안에 수식 PNG를 가로·세로 중앙 정렬한다.
// ew = 수식 너비(인치), ratio = PNG의 width/height. 카드 높이 ch는 수식 높이(ew/ratio)
// 보다 충분히 크게(underbrace 라벨 식이면 +여유). 패널과 겹치지 않게 카드 끝 < 패널 시작.
function eqInCard(s,cx,cy,cw,ch,path,ew,ratio){
  rect(s,cx,cy,cw,ch,C.panelGray);
  const h=ew/ratio, x=cx+(cw-ew)/2, y=cy+(ch-h)/2;
  s.addImage({path,x,y,w:ew,h});
}

// ---- 그림/차트를 가용 영역에 꽉 차게 배치 (여백 최소화) ★v1.5 ----------------
// 폭(최대 CW=12.09)을 우선 채우고, 높이가 넘치면 높이 기준으로 맞춘 뒤 수직 중앙정렬.
// 부제(takeaway)를 head()에 넣고 하단 caption은 생략하는 것을 기본으로 한다.
// yTop=2.05(부제 아래), yBot=6.96(푸터 hairline 위) 사이를 최대로 사용.
function figImg(s,path,ratio,opt){
  opt=opt||{};
  const yTop=opt.yTop||2.05, yBot=opt.yBot||6.96, maxW=opt.maxW||CW;
  const w=Math.min(maxW,(yBot-yTop)*ratio), h=w/ratio, y=yTop+((yBot-yTop)-h)/2;
  s.addImage({ path, x:(13.333-w)/2, y, w, h });
}

// ---- (A) 전체폭 와이드 그림 슬라이드 = head + figImg ★v1.6.1 --------------------
// 글씨 박스형 다이어그램(2.5:1 와이드 SVG→PNG)을 한 장으로. takeaway는 sub로 올린다.
// o: {chip, chipW, title, sub, pageNo, path, ratio}
function figureSlide(s,o){
  head(s, o.chip, o.chipW, o.title, o.sub||null, o.pageNo);
  figImg(s, o.path, o.ratio);
}

// ---- (B) 좌측 해설 패널 + 우측 원본 이미지 ★v1.6.1 -----------------------------
// 곡선·산점도·사진처럼 재현 불가한 이미지를 좌측 tint 패널 해설 + 우측 원본으로 싣는다.
// o: {chip, chipW, title, sub, pageNo, panelTitle, lines[], tint, path, ratio}
// tint: "green"/"orange"/그 외(blue). 우측 이미지는 남은 폭에 맞춰 높이 초과 시
// 높이 기준 축소 + 세로 중앙 + 얇은 hairline 테두리.
function figurePanelSlide(s,o){
  const cy = head(s, o.chip, o.chipW, o.title, o.sub||null, o.pageNo);
  const PW=3.45, gap=0.30, yTop=cy, yBot=6.92, ph=yBot-yTop;
  const isG=o.tint==="green", isO=o.tint==="orange";
  const fill=isG?C.panelGreen:(isO?P.fill:C.panelBlue);
  const tc  =isG?C.green:(isO?P.acc:C.blue);
  panel(s, LX, yTop, PW, ph, fill, tc, o.panelTitle, o.lines);
  const iw0=CW-PW-gap, ix=LX+PW+gap;
  const iw=Math.min(iw0, ph*o.ratio), ih=iw/o.ratio;
  const iy=yTop+(ph-ih)/2, ixc=ix+(iw0-iw)/2;
  s.addImage({ path:o.path, x:ixc, y:iy, w:iw, h:ih });
  s.addShape(p.ShapeType.rect,{x:ixc,y:iy,w:iw,h:ih,fill:{type:"none"},line:{color:C.hair,width:1}});
}

module.exports = { p,C,P,F,MONO,S,MODE,LX,CW,CY_SUB,CY_NOSUB,setSubject,
  rect,hline,chip,head,cover,divider,msgRows,statCards,stepCards,banner,caption,
  panel,bigCard,wtable,qRows,promptBox,promptBoxIn,cmdBox,outputBox,
  eqC,eqL,eqInCard,figImg,figureSlide,figurePanelSlide };
