import streamlit as st

st.set_page_config(page_title="Trang chủ", page_icon="🏠", layout="wide")

# Dùng CSS variable của Streamlit: tự động thích ứng System / Light / Dark
st.markdown("""
<style>
.hero-title {
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--primary-color);
    margin-bottom: 4px;
}
.hero-heading {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-color);
    line-height: 1.35;
    margin: 0 0 12px 0;
}
.hero-desc {
    font-size: 1rem;
    color: var(--text-color);
    opacity: 0.75;
    line-height: 1.75;
    max-width: 800px;
    margin-bottom: 16px;
}
.badge {
    display: inline-block;
    background-color: var(--secondary-background-color);
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    border-radius: 4px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 4px;
}
.divider {
    border: none;
    border-top: 1px solid var(--secondary-background-color);
    margin: 28px 0;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
/* Team table */
.team-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.93rem;
    border-bottom: 1px solid var(--secondary-background-color);
}
.team-table th {
    text-align: left;
    padding: 8px 14px;
    color: var(--primary-color);
    border-bottom: 2px solid var(--primary-color);
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.team-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--secondary-background-color) !important;
    color: var(--text-color);
}
/* Feature list */
.feature-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px 24px;
    margin-top: 8px;
}
.feature-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 10px 0;
    border-bottom: 1px solid var(--secondary-background-color);
}
.feature-icon { font-size: 1.3rem; flex-shrink: 0; margin-top: 1px; }
.feature-title {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-color);
    margin-bottom: 2px;
}
.feature-desc {
    font-size: 0.82rem;
    color: var(--text-color);
    opacity: 0.65;
    line-height: 1.5;
}
/* KT list */
.kt-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px 32px;
    margin-top: 8px;
}
.kt-item {
    padding: 10px 0 10px 12px;
    border-left: 3px solid var(--primary-color);
}
.kt-item strong {
    font-size: 0.9rem;
    color: var(--text-color);
    display: block;
    margin-bottom: 4px;
}
.kt-item p {
    font-size: 0.82rem;
    color: var(--text-color);
    opacity: 0.65;
    margin: 0;
    line-height: 1.5;
}
/* Instructor */
.instructor {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
}
.instructor-avatar {
    font-size: 2.2rem;
    flex-shrink: 0;
}
.instructor-name {
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-color);
}
.instructor-sub {
    font-size: 0.82rem;
    color: var(--text-color);
    opacity: 0.6;
    margin-top: 2px;
    line-height: 1.5;
}
.footer {
    text-align: center;
    font-size: 0.78rem;
    color: var(--text-color);
    opacity: 0.45;
    margin-top: 40px;
    padding-top: 16px;
    border-top: 1px solid var(--secondary-background-color);
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">Đồ án học phần • Các hệ cơ sở tri thức</p>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-heading">HỆ THỐNG SINH ĐỀ TRẮC NGHIỆM VÀ CHẤM ĐIỂM</h1>', unsafe_allow_html=True)
st.markdown("""
<span class="hero-desc">
    Tự động sinh đề trắc nghiệm theo môn học, phân loại độ khó chính xác,
    chấm điểm và đánh giá năng lực sinh viên dựa trên mô hình tri thức kết hợp LLM.
</span>
<div>
    <span class="badge">🐍 Nhập môn Python</span>
    <span class="badge">📊 Cấu trúc dữ liệu &amp; Giải thuật</span>
    <span class="badge">🤖 LLM + Ontology</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

# ── Nhóm thực hiện + Giảng viên ───────────────────────────────────────────────
col1, col2 = st.columns([3, 1.2], gap="large")

with col1:
    st.markdown('<p class="section-title">👥 Nhóm thực hiện</p>', unsafe_allow_html=True)
    st.markdown("""
    <table class="team-table">
        <thead>
            <tr>
                <td>MSHV</td>
                <td>Họ và tên</td>
                <td>Email học viên</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>KHMT836007</td>
                <td><strong>Nguyễn Thị Mỹ Hạnh</strong></td>
                <td>hanhntm.KHMT036@pg.hcmue.edu.vn</td>
            </tr>
            <tr>
                <td>KHMT836021</td>
                <td><strong>Bùi Nguyên Nghĩa</strong></td>
                <td>nghiabn.KHMT036@pg.hcmue.edu.vn</td>
            </tr>
            <tr>
                <td>KHMT836031</td>
                <td><strong>Nguyễn Đức Thành</strong></td>
                <td>thanhnd.KHMT036@pg.hcmue.edu.vn</td>
            </tr>
        </tbody>
    </table>
                
    <p style="font-size:0.8rem;color:var(--text-color);opacity:0.5;margin-top:10px;">
        Học viên Cao học Khóa 36 - Ngành Khoa học Máy tính &nbsp;&nbsp;
    </p>
    <p style="font-size:0.8rem;color:var(--text-color);opacity:0.5;margin-top:0px;">
        Trường Đại học Sư phạm TP. Hồ Chí Minh
    </p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<p class="section-title">🎓 Giảng viên hướng dẫn</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="instructor">
        <div class="instructor-avatar">👨‍🏫</div>
        <div>
            <div class="instructor-name">PGS. TS. Nguyễn Đình Hiển</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

# ── Kỹ thuật biểu diễn tri thức ───────────────────────────────────────────────
st.markdown('<p class="section-title">🧠 Các kỹ thuật biểu diễn tri thức</p>', unsafe_allow_html=True)
st.markdown("""
<div class="kt-row">
    <div class="kt-item">
        <strong>📐 Ontology (Web Ontology Language)</strong>
        <p>Biểu diễn cấu trúc tri thức: môn học → chủ đề → khái niệm → câu hỏi. Định nghĩa rõ mối quan hệ giữa các thực thể tri thức.</p>
    </div>
    <div class="kt-item">
        <strong>📏 Item Response Theory (IRT)</strong>
        <p>Mô hình xác suất đánh giá độ khó, độ phân biệt và tỉ lệ đoán mò cho từng câu hỏi dựa trên dữ liệu phản hồi thực tế.</p>
    </div>
    <div class="kt-item">
        <strong>🔗 Luật suy luận (Production Rules)</strong>
        <p>Hệ luật IF–THEN: nếu sinh viên yếu chủ đề X thì tăng tần suất câu hỏi chủ đề X; nếu độ khó trung bình lớn thì xếp loại khó.</p>
    </div>
    <div class="kt-item">
        <strong>🤖 LLM (Large Language Model)</strong>
        <p>Sinh câu hỏi mới theo chủ đề định sẵn, xác định độ khó tự động, làm giàu ngân hàng câu hỏi khi cần mở rộng.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

# ── Tính năng đã thực hiện ────────────────────────────────────────────────────
st.markdown('<p class="section-title">⚡ Những tính năng đã thực hiện</p>', unsafe_allow_html=True)
st.markdown("""
<div class="feature-row">
    <div class="feature-item">
        <div class="feature-icon">🎲</div>
        <div>
            <div class="feature-title">Sinh đề linh hoạt</div>
            <div class="feature-desc">Chọn môn học, số câu, mức độ khó (dễ/trung bình/khó/xáo trộn).</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🔀</div>
        <div>
            <div class="feature-title">Xáo trộn thứ tự đáp án</div>
            <div class="feature-desc">Thứ tự A/B/C/D thay đổi mỗi lần sinh đề, hệ thống vẫn chấm điểm chính xác.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">⏱️</div>
        <div>
            <div class="feature-title">Đồng hồ đếm thời gian</div>
            <div class="feature-desc">Tự động bắt đầu khi tạo đề, hiển thị trực tiếp trên giao diện.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">✅</div>
        <div>
            <div class="feature-title">Chấm điểm tự động</div>
            <div class="feature-desc">Điểm thang 10, thống kê đúng/sai và đáp án đúng từng câu sau khi nộp bài.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📚</div>
        <div>
            <div class="feature-title">Ngân hàng câu hỏi tiếng Việt</div>
            <div class="feature-desc">Phân loại theo môn học, chủ đề, khái niệm, độ khó phục vụ biểu diễn tri thức.</div>
        </div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">🔒</div>
        <div>
            <div class="feature-title">Bảo mật nội dung</div>
            <div class="feature-desc">Vô hiệu hóa copy nội dung đề thi, khoá cấu hình trong lúc làm bài.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    © 2026 Nhóm KHMT036 &nbsp;·&nbsp; Trường Đại học Sư phạm TP.HCM &nbsp;·&nbsp; Học phần: Các hệ cơ sở tri thức
</div>
""", unsafe_allow_html=True)
