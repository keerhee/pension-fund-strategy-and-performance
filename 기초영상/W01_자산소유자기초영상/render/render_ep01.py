"""W01 EP.01 'BlackRock의 $11조는 누구 돈?' — 자본시장 생태계. 돈은 위에서 아래로 흐른다:
자산소유자(최종 자금의 원천 · 위임의 주체) → 자산운용사(대리인) → 투자은행(발행 · 주선 · 중개) → 거래소 · 인프라(체결 · 청산 · 예탁), 수익은 점선으로 주인에게 환류.
BlackRock $11조도 결국 자산소유자의 돈 — 의사결정의 최종 책임은 언제나 자산소유자에게. (W01 강의본 2·4·5·6장 · 기획표 EP01_Cuts 그대로)"""
from wkit import *

EQ = []
TIERS = [("자산소유자", "연기금 · 국부펀드 · 보험 · 엔다우먼트", "돈의 주인 · 위임의 주체", NAVY),
         ("자산운용사", "BlackRock · PIMCO · 미래에셋", "대리인 — 맡아서 굴린다", BLUE),
         ("투자은행", "Goldman · Morgan Stanley · KB", "발행 · 주선 · 중개", TEAL),
         ("거래소 · 인프라", "NYSE · KRX · DTCC", "체결 · 청산 · 예탁", GREY)]


def cut1(t): return title(t, "EP.01 · BlackRock의 $11조는 누구 돈?", 1000)


def cut2(t):
    body = (label("세계 최대 운용사", 0, -110, 36, "#555", 800)
            + label("BlackRock 운용자산", 0, -40, 40, NAVY, 900) + punch("$11조", 0, 45, 96, fill=GOLD, sw=11)
            + label("펭: “세계 최고 부자 회사!”", 0, 160, 38, BLUE, 900))
    return problem(t, "세계 최대 부자?", GOLD, "#FBF1DD", "펭의 경제 뉴스 스크랩", body, ["BlackRock이 세계에서", "제일 돈이 많은 거죠?"], "부자 1위!")


def cut3(t): return twist(t, ["그 돈은 BlackRock 돈이 아니야.", "연기금 · 국부펀드가 맡긴 돈이지."], "주인은 따로!", size=46, sfx_size=150)


def cut4(t):
    s = explainer_frame(t, "돈은 위에서 아래로", "흐름의 순서가 곧 권력의 순서 — 점선의 환류(수익 귀속)까지가 한 사이클")
    for i, (nm, ex, role, c) in enumerate(TIERS):
        g = back(prog(t, .5 + .6 * i, .4))
        if g <= 0: continue
        y = 450 + 150 * i
        s.append(f'<g transform="translate(450,{y}) scale({g:.3f})"><rect x="-370" y="-55" width="740" height="110" rx="18" fill="{c}"/>'
                 + label(nm, -215, -14, 34, "#fff", 900) + label(role, -215, 26, 22, "#fff", 800)
                 + label(ex, 160, 0, 20, YELLOW, 900) + "</g>")
        if i > 0 and t > .5 + .6 * i:
            s.append(f'<g opacity="{ease_out(prog(t, .5 + .6 * i, .3)):.2f}"><line x1="450" y1="{y-95}" x2="450" y2="{y-62}" stroke="{NAVY}" stroke-width="6"/>'
                     f'<polygon points="438,{y-66} 462,{y-66} 450,{y-56}" fill="{NAVY}"/></g>')
    if t > 3.2:
        a = ease_out(prog(t, 3.2, .5))
        s.append(f'<g opacity="{a:.2f}"><path d="M 825 900 C 925 900, 925 450, 825 450" fill="none" stroke="{GREEN}" stroke-width="6" stroke-dasharray="14 10"/>'
                 f'<polygon points="825,450 848,438 848,462" fill="{GREEN}"/>' + label("수익은", 965, 650, 24, GREEN, 900) + label("주인에게", 965, 685, 24, GREEN, 900) + "</g>")
    s.append(chip("BlackRock $11조도 결국 자산소유자의 돈", 540, 1030, GOLD, back(prog(t, 4.2, .4)), w=760, size=34))
    s.append(chip("운용사는 대리인 — 최종 책임은 언제나 자산소유자", 540, 1130, NAVY, back(prog(t, 4.8, .4)), w=880, size=32))
    s += explainer_tail(t, "흐름의 꼭대기에 서야 위임 · 보수가 보인다", "16주의 첫 질문 — “우리는 누구의 돈을 운용하는가”",
                        ["$11조는 수많은 주인의 돈을", "모아 맡은 거야."], a0=6.2)
    return s


def cut5(t): return relief(t, ["그럼 책임은", "누가 져요?"], ["맡긴 사람이야. 의사결정의 최종 책임은", "늘 자산소유자에게 있어."],
                           "주인이 책임!", "체크: 주인 · 대리인 · 위임 · 환류", happy=True, a_size=44, sfx_size=120)


def cut6(t): return next_cut(t, TEAL, "1bp의 무게", "주인은 무엇으로 버나?", topic_size=180)


META = dict(
    episode="EP.01", title="BlackRock의 $11조는 누구 돈?",
    concept="자본시장 생태계 — 돈은 자산소유자(최종 자금의 원천 · 위임의 주체) → 운용사(대리인) → 투자은행 → 거래소로 흐르고, 수익은 다시 주인에게 환류한다. 세계 최대 운용사 BlackRock의 $11조도 결국 자산소유자의 돈이며, 의사결정의 최종 책임은 언제나 자산소유자에게 있다. 16주 과정의 첫 질문: “우리는 누구의 돈을 운용하는가”",
    source="W01 강의본 2장(자산소유자는 생태계의 정점 — BlackRock $11조도 결국 자산소유자의 돈) · 4장(돈은 위에서 아래로 흐른다 — 점선의 환류까지 한 사이클) · 5장(4대 참여자 — 역할과 대표 기관, 운용사는 대리인 · 최종 책임은 자산소유자) · 6장(정점인 세 이유) · 기획표 EP01_Cuts",
    cuts=[{"n": 2, "notice": "펭의 경제 뉴스 스크랩 · 세계 최대 운용사 · BlackRock 운용자산 $11조 · 펭: “세계 최고 부자 회사!”", "bubble": ["BlackRock이 세계에서", "제일 돈이 많은 거죠?"], "sfx": "부자 1위!"},
          {"n": 3, "bubble": ["그 돈은 BlackRock 돈이 아니야.", "연기금 · 국부펀드가 맡긴 돈이지."], "sfx": "주인은 따로!"},
          {"n": 4, "flow": [t_[0] + " — " + t_[2] for t_ in TIERS], "loop": "수익은 주인에게(점선 환류)", "chips": ["BlackRock $11조도 결국 자산소유자의 돈", "운용사는 대리인 — 최종 책임은 언제나 자산소유자"],
           "summary": "흐름의 꼭대기에 서야 위임 · 보수가 보인다", "bubble": ["$11조는 수많은 주인의 돈을", "모아 맡은 거야."]},
          {"n": 5, "bubbles": [["그럼 책임은", "누가 져요?"], ["맡긴 사람이야. 의사결정의 최종 책임은", "늘 자산소유자에게 있어."]], "sfx": "주인이 책임!"},
          {"n": 6, "text": ["다음 화", "1bp의 무게", "주인은 무엇으로 버나?"]}],
    **{"fact-check": "BlackRock $11조는 강의본 2장 표기(운용자산, 시점에 따라 다름 — 원자료 직접 확인 안 함). 대표 기관 예시는 강의본 5장 표. 이 화는 개념 화라 손계산 대신 흐름도로 구성했다(기획표 EP01_Cuts). 'BlackRock 돈이 아니다'는 운용자산(AUM) 기준이며 BlackRock 자체의 자기자본은 별개."})

if __name__ == "__main__": main([cut1, cut2, cut3, cut4, cut5, cut6], "01", META)
