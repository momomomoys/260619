import streamlit as st

st.set_page_config(
    page_title="🎀 나에게 딱 맞는 학과 찾기",
    page_icon="🎨",
    layout="centered"
)

# CSS
st.markdown("""
<style>

.main {
    background: linear-gradient(180deg,#fff0f6,#ffe8f5);
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:#ff4fa3;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:#666;
}

.question-box{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    margin-bottom:15px;
}

.result-box{
    background:linear-gradient(135deg,#ffd6ec,#ffe9b3);
    padding:25px;
    border-radius:25px;
    color:black;
}

</style>
""", unsafe_allow_html=True)

# 제목

st.markdown(
    '<div class="title">🎀 디자인 적성 테스트 🎀</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">💖 나에게 맞는 학과는 시각디자인과? 영상애니메이션과?</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# 점수 저장

if "visual" not in st.session_state:
    st.session_state.visual = 0

if "animation" not in st.session_state:
    st.session_state.animation = 0

questions = [

("🌸 쉬는 시간에 더 하고 싶은 것은?",
 ["🎨 굿즈 디자인하기",
  "🎬 애니메이션 영상 만들기"]),

("🧸 SNS에서 더 자주 보는 것은?",
 ["💖 감성 포스터·브랜딩",
  "✨ 애니메이션 편집 영상"]),

("🎁 학교 축제를 맡게 된다면?",
 ["🎨 포스터와 배너 디자인",
  "🎥 홍보 영상 제작"]),

("📱 가장 좋아하는 취미는?",
 ["🖌️ 캐릭터 굿즈 그리기",
  "🎞️ 쇼츠·릴스 편집"]),

("🌈 더 설레는 것은?",
 ["💖 나만의 브랜드 만들기",
  "🌟 캐릭터에 생명 불어넣기"]),

("🎀 그림을 그릴 때?",
 ["색감과 배치에 신경쓴다",
  "움직임과 표정에 신경쓴다"]),

("🍀 미래에 하고 싶은 일은?",
 ["광고·브랜드 디자인",
  "애니메이터·영상 크리에이터"]),

("🎨 좋아하는 콘텐츠는?",
 ["예쁜 패키지·굿즈",
  "웹툰·애니·유튜브"]),

("💻 컴퓨터 작업이라면?",
 ["포토샵 디자인",
  "영상 편집"]),

("✨ 친구들이 나를 뭐라고 할까?",
 ["감각이 좋다",
  "상상력이 풍부하다"])
]

for i, (q, options) in enumerate(questions):

    st.markdown(
        f"""
        <div class="question-box">
        <h4>{i+1}. {q}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "",
        options,
        key=f"q{i}"
    )

    if answer == options[0]:
        pass

st.markdown("---")

if st.button("💖 결과 확인하기", use_container_width=True):

    visual = 0
    animation = 0

    answers = [st.session_state[f"q{i}"] for i in range(10)]

    for a, (q, opts) in zip(answers, questions):

        if a == opts[0]:
            visual += 1
        else:
            animation += 1

    st.balloons()

    if visual >= animation:

        st.markdown(f"""
        <div class="result-box">
        <h1>🎨 시각디자인과 추천!</h1>

        <h3>💖 당신은 색감과 디자인 감각이 뛰어난 편이에요!</h3>

        <ul>
        <li>🌸 브랜딩 디자인</li>
        <li>🎁 굿즈 디자인</li>
        <li>📱 SNS 콘텐츠 디자인</li>
        <li>🎨 일러스트레이터</li>
        <li>🛍 패키지 디자이너</li>
        </ul>

        <h3>✨ 추천 취미</h3>

        🎀 스티커 제작<br>
        🎀 캐릭터 굿즈 만들기<br>
        🎀 포스터 디자인<br>
        🎀 다꾸(다이어리 꾸미기)<br>
        🎀 아이패드 드로잉
        </div>
        """, unsafe_allow_html=True)

        st.image(
            "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1200"
        )

    else:

        st.markdown(f"""
        <div class="result-box">
        <h1>🎬 영상애니메이션과 추천!</h1>

        <h3>🌟 당신은 상상력과 스토리 표현력이 뛰어나요!</h3>

        <ul>
        <li>🎞 애니메이터</li>
        <li>🎬 영상 편집자</li>
        <li>🎨 캐릭터 디자이너</li>
        <li>📺 콘텐츠 크리에이터</li>
        <li>🎮 게임 원화가</li>
        </ul>

        <h3>✨ 추천 취미</h3>

        🎀 웹툰 그리기<br>
        🎀 애니메이션 감상<br>
        🎀 브이로그 제작<br>
        🎀 쇼츠 편집<br>
        🎀 캐릭터 창작
        </div>
        """, unsafe_allow_html=True)

        st.image(
            "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44f?w=1200"
        )

    st.markdown("## 🌈 적성 결과")

    st.progress(max(visual, animation) / 10)

    st.write(f"🎨 시각디자인 적성 : {visual}/10")
    st.write(f"🎬 영상애니메이션 적성 : {animation}/10")

    if visual > animation:
        st.success("💖 감각적인 디자인 분야에 강점이 있어요!")
    else:
        st.success("🌟 움직이는 콘텐츠와 스토리 표현에 강점이 있어요!")

st.markdown("---")
st.caption("🎀 중학생 진로체험용 디자인 적성 테스트")
