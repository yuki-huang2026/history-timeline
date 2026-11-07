import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 页面基础设置（必须放在第一行）
st.set_page_config(page_title="时空经纬：AI历史工具", layout="wide")

# 2. 注入自定义 CSS 样式，打造古风界面
st.markdown("""
    <style>
    .stApp {
        background-color: #F5DEB3; /* 宣纸黄背景 */
        font-family: 'KaiTi', '楷体', serif;
    }
    h1 { color: #8B0000; text-align: center; }
    .stButton>button {
        background-color: #8B0000; color: white; border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 页面头部
st.title("📜 时空经纬：历史脉络探索工具")
st.write("提示：输入你想查询的朝代，点击按钮生成时间轴，点击红点查看史料对比。")

# 4. 交互区域：输入框和按钮
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("请输入朝代或历史事件（如：宋朝、明朝、安史之乱）：", value="", placeholder="在这里输入...")
with col2:
    st.write("") # 占位
    st.write("") # 占位
    generate_btn = st.button("🚀 生成时间轴")

# 5. 核心逻辑：当用户点击按钮时
if generate_btn:
    if not user_input:
        st.warning("⚠️ 请先输入一个历史时期！")
    else:
        with st.spinner("AI 正在翻阅史书，请稍候..."):
            # 【重点】这里目前是用假数据模拟。明天我们将把这里换成调用 GeniOS 的 API 代码！
            # 为了让程序认识所有输入，我们根据用户输入动态生成数据
            mock_data = [
                {"name": f"{user_input}初期", "year": "600年", "desc": f"关于{user_input}初期的真实记载。"},
                {"name": f"{user_input}盛世", "year": "700年", "desc": f"{user_input}鼎盛时期的政治与经济状况。"},
                {"name": f"{user_input}转折", "year": "800年", "desc": "重大历史事件发生，制度出现变革。"},
                {"name": f"{user_input}末期", "year": "900年", "desc": "社会矛盾加剧，走向终结。"}
            ]
            
            # 将 Python 数据转为 JSON 字符串，传给前端 JS
            data_json = json.dumps(mock_data, ensure_ascii=False)
            
            # 6. 构建 ECharts 前端代码
            html_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
                <style>
                    #main {{ width: 100%; height: 350px; }}
                    #detail-card {{
                        display: none; margin-top: 20px; padding: 20px; 
                        background-color: #FFF8DC; border-left: 6px solid #8B0000;
                        border-radius: 5px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                        font-family: 'KaiTi', '楷体', serif; color: #333;
                    }}
                    h3 {{ margin-top: 0; color: #8B0000; }}
                </style>
            </head>
            <body>
                <div id="main"></div>
                <div id="detail-card">
                    <h3 id="detail-title"></h3>
                    <p id="detail-content"></p>
                </div>
                <script>
                    var chartDom = document.getElementById('main');
                    var myChart = echarts.init(chartDom);
                    
                    // 接收 Python 传过来的动态数据
                    var data = {data_json}; 
                    
                    var option = {{
                        title: {{ text: '{user_input} 历史脉络', left: 'center', textStyle: {{ color: '#8B0000', fontFamily: 'KaiTi' }} }},
                        tooltip: {{ trigger: 'item' }},
                        xAxis: {{
                            type: 'category',
                            data: data.map(item => item.year),
                            axisLine: {{ lineStyle: {{ color: '#8B0000', width: 2 }} }},
                            axisLabel: {{ color: '#333', fontSize: 14 }}
                        }},
                        yAxis: {{ show: false }},
                        series: [{{
                            type: 'line',
                            data: data.map(item => item.year),
                            symbol: 'circle',
                            symbolSize: 20,
                            itemStyle: {{ color: '#8B0000' }},
                            lineStyle: {{ width: 3, color: '#D2B48C' }},
                            label: {{ show: true, position: 'bottom', formatter: '{{b}}', color: '#333', fontSize: 14 }}
                        }}]
                    }};
                    myChart.setOption(option);

                    // 点击事件
                    myChart.on('click', function (params) {{
                        if(params.componentType === 'series') {{
                            var item = data[params.dataIndex];
                            document.getElementById('detail-title').innerText = item.name + " (" + item.year + ")";
                            document.getElementById('detail-content').innerText = item.desc;
                            document.getElementById('detail-card').style.display = 'block';
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            # 渲染页面
            components.html(html_code, height=500)
