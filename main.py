import streamlit as st
from datetime import datetime
import base64

def create_print_html(data):
    """프린트용 HTML 생성"""
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>연구노트</title>
<style>
body {{
font-family: 'Malgun Gothic', sans-serif;
margin: 5px;
line-height: 1.5;
}}
.header {{
text-align: center;
color: black;
font-weight: bold;
font-size: 20px;
margin-bottom: 20px;
border-bottom: 2px solid black;
padding-bottom: 8px;
}}
.signature-section {{
margin-bottom: 20px;
}}
.section {{
margin-bottom: 15px;
}}
.section-title {{
font-weight: bold;
margin-bottom: 5px;
font-size: 14px;
}}
.content {{
border: 1px solid #333;
padding: 8px;
background-color: #fafafa;
word-wrap: break-word;
white-space: pre-wrap;
line-height: 1.4;
min-height: auto;
font-size: 10pt;
}}
@media print {{
body {{
margin: 0;
}}
.section {{
page-break-inside: avoid;
}}
}}
</style>
</head>
<body>
<div class="header">연구노트</div>

<div class="signature-section">
<span><strong>작성자:</strong> {data.get('작성자_이름', '')}</span>
<span style="display: inline-block; border-bottom: 1px solid #333; width: 80px; margin: 0 20px;"></span>
<span><strong>검토자:</strong> {data.get('검토자_이름', '')}</span>
<span style="display: inline-block; border-bottom: 1px solid #333; width: 80px; margin: 0 20px;"></span>
</div>

<div class="section">
<div class="section-title">1. 연구진행 : {data.get('selected_stage', '선택안함')}</div>
</div>

<div class="section">
<div class="section-title">2. 연구명칭 :</div>
<div class="content">
{data.get('연구명칭', '')}
</div>
</div>

<div class="section">
<div class="section-title">3. 연구목표 :</div>
<div class="content">
{data.get('연구목표', '')}
</div>
</div>

<div class="section">
<div class="section-title">4. 연구내용 :</div>
<div class="content">
<div><strong>1) 재료 및 양식:</strong> {data.get('재료양식', '')}</div>
<br>
<div><strong>2) 시험방법:</strong> {data.get('시험방법', '')}</div>
</div>
</div>

<div class="section">
<div class="section-title">5. 연구의 주요이슈 :</div>
<div class="content">
{data.get('주요이슈', '')}
</div>
</div>

<div class="section">
<div class="section-title">6. 주요이슈 해결방안 :</div>
<div class="content">
{data.get('해결방안', '')}
</div>
</div>

<div class="section">
<div class="section-title">7. 향후 계획 :</div>
<div class="content">
{data.get('향후계획', '')}
</div>
</div>"""

    # 업로드된 파일이 있을 때만 별첨 섹션 추가
    if 'uploaded_files' in data and data['uploaded_files']:
        html_content += """
<div class="section">
<div class="section-title">8. 별첨(첨부 연구데이터)</div>"""
        
        for i, file_info in enumerate(data['uploaded_files']):
            html_content += f"""
<div style="margin-bottom: 5px;">
<p><strong>{i+1}. {file_info['name']}</strong></p>
<img src="data:{file_info['type']};base64,{file_info['data']}" 
style="max-width: 100%; height: auto; border: 1px solid #333; margin-top: 3px;" 
alt="{file_info['name']}">
</div>"""
        
        html_content += """
</div>"""
    
    html_content += """
</body>
</html>
"""
    return html_content

def main():
    st.set_page_config(page_title="연구노트 작성", layout="wide")
    
    st.title("🔬 연구노트")
    st.markdown("---")
    
    # 세션 상태 초기화
    if 'data' not in st.session_state:
        st.session_state.data = {}
    
    # 작성자/검토자 정보
    st.subheader("👥 작성자 및 검토자 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        작성자_이름 = st.text_input("작성자 이름", value=st.session_state.data.get('작성자_이름', ''), placeholder="작성자 이름을 입력하세요")
        st.session_state.data['작성자_이름'] = 작성자_이름
    
    with col2:
        검토자_이름 = st.text_input("검토자 이름", value=st.session_state.data.get('검토자_이름', ''), placeholder="검토자 이름을 입력하세요")
        st.session_state.data['검토자_이름'] = 검토자_이름
    
    st.markdown("---")
    
    # 1. 연구진행
    st.subheader("1. 연구진행 : E/S (단계 및 기획)")
    col1, col2, col3, col4 = st.columns(4)
    
    if 'selected_stage' not in st.session_state.data:
        st.session_state.data['selected_stage'] = None
    
    with col1:
        if st.button("기획", type="primary" if st.session_state.data['selected_stage'] == "기획" else "secondary"):
            st.session_state.data['selected_stage'] = "기획"
            st.rerun()
    
    with col2:
        if st.button("E/S", type="primary" if st.session_state.data['selected_stage'] == "E/S" else "secondary"):
            st.session_state.data['selected_stage'] = "E/S"
            st.rerun()
    
    with col3:
        if st.button("Pilot", type="primary" if st.session_state.data['selected_stage'] == "Pilot" else "secondary"):
            st.session_state.data['selected_stage'] = "Pilot"
            st.rerun()
    
    with col4:
        if st.button("허가완료/양산이관", type="primary" if st.session_state.data['selected_stage'] == "허가완료/양산이관" else "secondary"):
            st.session_state.data['selected_stage'] = "허가완료/양산이관"
            st.rerun()
    
    # 선택된 단계 표시
    if st.session_state.data['selected_stage']:
        st.success(f"✅ 선택된 연구단계: **{st.session_state.data['selected_stage']}**")
    else:
        st.warning("⚠️ 연구단계를 선택해주세요")
    
    st.markdown("---")
    
    # 2. 연구명칭
    st.subheader("2. 연구명칭")
    연구명칭 = st.text_input("연구명칭을 입력하세요", value=st.session_state.data.get('연구명칭', ''), placeholder="예) Drainage catheter")
    st.session_state.data['연구명칭'] = 연구명칭
    
    # 3. 연구목표
    st.subheader("3. 연구목표")
    연구목표 = st.text_area("연구목표를 입력하세요", value=st.session_state.data.get('연구목표', ''), height=120, placeholder="연구의 목표와 기대효과를 입력하세요")
    st.session_state.data['연구목표'] = 연구목표
    
    # 4. 연구내용
    st.subheader("4. 연구내용")
    재료양식 = st.text_area("1) 재료 및 양식", value=st.session_state.data.get('재료양식', ''), height=100, placeholder="사용할 재료와 양식을 입력하세요")
    st.session_state.data['재료양식'] = 재료양식
    
    시험방법 = st.text_area("2) 시험방법", value=st.session_state.data.get('시험방법', ''), height=100, placeholder="시험 방법과 절차를 입력하세요")
    st.session_state.data['시험방법'] = 시험방법
    
    # 5. 연구의 주요이슈
    st.subheader("5. 연구의 주요이슈")
    주요이슈 = st.text_area("주요이슈를 입력하세요", value=st.session_state.data.get('주요이슈', ''), height=120, placeholder="연구 과정에서 발생한 주요 이슈들을 입력하세요")
    st.session_state.data['주요이슈'] = 주요이슈
    
    # 6. 주요이슈 해결방안
    st.subheader("6. 주요이슈 해결방안")
    해결방안 = st.text_area("해결방안을 입력하세요", value=st.session_state.data.get('해결방안', ''), height=120, placeholder="주요 이슈들에 대한 해결방안을 입력하세요")
    st.session_state.data['해결방안'] = 해결방안
    
    # 7. 향후 계획
    st.subheader("7. 향후 계획")
    향후계획 = st.text_area("향후 계획을 입력하세요", value=st.session_state.data.get('향후계획', ''), height=120, placeholder="향후 연구 계획과 일정을 입력하세요")
    st.session_state.data['향후계획'] = 향후계획
    
    # 8. 별첨
    st.subheader("8. 별첨(첨부 연구데이터)")
    uploaded_files = st.file_uploader(
        "이미지 파일을 선택하세요", 
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        accept_multiple_files=True,
        help="여러 개의 이미지 파일을 업로드할 수 있습니다."
    )
    
    # 파일 처리
    if uploaded_files:
        st.session_state.data['uploaded_files'] = []
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            file_base64 = base64.b64encode(file_bytes).decode()
            file_info = {
                'name': uploaded_file.name,
                'type': uploaded_file.type,
                'data': file_base64
            }
            st.session_state.data['uploaded_files'].append(file_info)
        
        st.write("**📁 업로드된 이미지:**")
        for i, file_info in enumerate(st.session_state.data['uploaded_files']):
            st.write(f"**{i+1}. {file_info['name']}**")
            file_bytes = base64.b64decode(file_info['data'])
            st.image(file_bytes, caption=file_info['name'], use_column_width=True)
    
    elif 'uploaded_files' in st.session_state.data:
        st.write("**📁 업로드된 이미지:**")
        for i, file_info in enumerate(st.session_state.data['uploaded_files']):
            st.write(f"**{i+1}. {file_info['name']}**")
            file_bytes = base64.b64decode(file_info['data'])
            st.image(file_bytes, caption=file_info['name'], use_column_width=True)
    
    st.markdown("---")
    
    # 버튼들
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🖨️ 프린트", type="primary", use_container_width=True):
            html_content = create_print_html(st.session_state.data)
            
            st.download_button(
                label="📄 HTML 파일 다운로드 (프린트용)",
                data=html_content,
                file_name=f"연구노트_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
            
            st.success("✅ 프린트용 HTML이 생성되었습니다!")
            st.info("📋 위의 '📄 HTML 파일 다운로드' 버튼을 클릭하여 파일을 다운로드한 후, 브라우저에서 열어서 프린트하세요.")
            
            with st.expander("📋 프린트 미리보기"):
                st.components.v1.html(html_content, height=800, scrolling=True)
    
    with col3:
        if st.button("🔄 초기화", type="secondary", use_container_width=True):
            st.session_state.data = {}
            st.rerun()

if __name__ == "__main__":
    main()
    # streamlit run 연구일지.py
