import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime
from io import BytesIO
import pyecharts.options as opts
from pyecharts.charts import Bar, Pie, Line, Radar, Boxplot
from streamlit_echarts import st_pyecharts


# 设置页面标题和布局
st.set_page_config(page_title="教学管理系统", layout="wide")

# 数据库连接函数


@st.cache_resource
def get_database_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='daytime001',
        port=3306,
        db='ems',
        charset='utf8'
    )

# 数据库操作函数


def db_query(sql, params=None):
    conn = get_database_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or [])
            result = cursor.fetchall()
            return result, cursor.description
    except Exception as e:
        st.error(f"查询错误: {str(e)}")
        return None, None


def db_execute(sql, params=None):
    conn = get_database_connection()
    try:
        with conn.cursor() as cursor:
            affected_rows = cursor.execute(sql, params or [])
            conn.commit()
            return affected_rows
    except Exception as e:
        conn.rollback()
        st.error(f"执行错误: {str(e)}")
        return 0

# 登录界面


def login():
    # 注入简单的CSS样式
    st.markdown("""
        <style>
        /* 页面背景 */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* 标题样式 */
        .login-title {
            text-align: center;
            color: #2c3e50;
            padding: 1rem 0;
            margin-bottom: 0.5rem;
            margin-top: 8rem;  /* 显著增加顶部边距 */
        }
        
        .login-title h1 {
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        /* 输入框样式优化 */
        .stTextInput > div > div {
            background-color: rgba(255, 255, 255, 0.6);
        }
        
        .stTextInput input {
            background-color: rgba(255, 255, 255, 0.8) !important;
            border: 2px solid rgba(233, 236, 239, 0.8) !important;
            border-radius: 8px !important;
            padding: 0.8rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(5px) !important;
        }
        
        .stTextInput input:focus {
            border-color: rgba(74, 144, 226, 0.6) !important;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1) !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
        }
        
        .stTextInput input::placeholder {
            color: rgba(108, 117, 125, 0.8) !important;
            font-size: 0.95rem !important;
        }
        
        /* 标签文字样式 */
        .stTextInput label {
            color: #2c3e50 !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* 按钮样式 */
        .stButton > button {
            background: linear-gradient(135deg, rgba(74, 144, 226, 0.9) 0%, rgba(53, 122, 189, 0.9) 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            border-radius: 8px !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            letter-spacing: 1px !important;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            backdrop-filter: blur(5px) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
            background: linear-gradient(135deg, rgba(53, 122, 189, 0.95) 0%, rgba(44, 106, 160, 0.95) 100%) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* 错误提示样式 */
        .stAlert > div {
            padding: 1rem !important;
            border-radius: 8px !important;
            margin-top: 1rem !important;
            background-color: rgba(255, 229, 229, 0.9) !important;
            color: #cc0000 !important;
            border: none !important;
            font-size: 0.95rem !important;
            backdrop-filter: blur(5px) !important;
        }
        
        /* 表单容器样式 */
        .stForm > div {
            background-color: rgba(255, 255, 255, 0.3) !important;
            padding: 1.5rem !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02) !important;
            backdrop-filter: blur(10px) !important;
            border: none !important;
            margin-top: 0 !important;
        }
        
        /* 移除Streamlit默认的padding */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }
        
        /* 移除所有默认边框 */
        .stForm > div, .stTextInput > div > div, .stAlert > div {
            border: none !important;
        }
        
        /* 调整表单内部间距 */
        .stForm > div > div {
            gap: 1rem !important;
        }
        
        /* 调整输入框之间的间距 */
        .stTextInput {
            margin-bottom: 0.5rem !important;
        }
        
        /* 确保页面占满全高 */
        .main {
            min-height: 100vh !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 页面布局
    st.markdown("""
        <div class="login-title">
            <h1>🎓 教学管理系统</h1>
        </div>
    """, unsafe_allow_html=True)

    # 使用列布局确保表单居中
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("账号", placeholder="请输入账号")
            password = st.text_input(
                "密码", type="password", placeholder="请输入密码")
            submit = st.form_submit_button("登 录", use_container_width=True)

            if submit:
                if username == "admin" and password == "123456":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("账号或密码错误！")

# 课程管理界面


def course_management():
    st.markdown("""
        <div class="page-title">
            <h1>📚 课程管理</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        tab1, tab2 = st.tabs(["课程列表", "添加课程"])

        with tab1:
            # 显示课程列表
            results, description = db_query(
                "SELECT course.*, teacher.tname FROM course LEFT JOIN teacher ON course.tid = teacher.tid")
            if results:
                df = pd.DataFrame(results, columns=[
                    "课程号", "课程名", "学分", "教师编号", "授课教师"
                ])
                st.dataframe(df)

                # 修改课程信息
                with st.form("update_course"):
                    st.subheader("修改课程信息")
                    cid = st.text_input("课程号")

                    col1, col2 = st.columns(2)
                    with col1:
                        new_credit = st.number_input(
                            "新学分", min_value=0.0, step=0.5)
                    with col2:
                        # 获取所有教师列表供选择
                        teachers, _ = db_query(
                            "SELECT tid, tname FROM teacher")
                        teacher_options = {f"{t[0]} ({t[1]})": t[0]
                                           for t in teachers} if teachers else {}
                        new_tid = st.selectbox(
                            "新授课教师", options=list(teacher_options.keys()))

                    if st.form_submit_button("修改"):
                        if cid:
                            # 更新学分
                            credit_res = db_execute(
                                "UPDATE course SET credit = %s WHERE cid = %s",
                                [new_credit, cid]
                            )
                            # 更新教师
                            teacher_res = db_execute(
                                "UPDATE course SET tid = %s WHERE cid = %s",
                                [teacher_options[new_tid], cid]
                            )

                            if credit_res or teacher_res:
                                st.success("修改成功！")
                                st.rerun()
                            else:
                                st.error("修改失败！")
                        else:
                            st.warning("请输入课程号！")

        with tab2:
            # 添加课程表单
            with st.form("add_course"):
                cid = st.text_input("课程号")
                cname = st.text_input("课程名")
                credit = st.number_input("学分", min_value=0.0, step=0.5)

                # 获取所有教师列表供选择
                teachers, _ = db_query("SELECT tid, tname FROM teacher")
                teacher_options = {f"{t[0]} ({t[1]})": t[0]
                                   for t in teachers} if teachers else {}
                tid = st.selectbox(
                    "授课教师", options=list(teacher_options.keys()))

                if st.form_submit_button("添加"):
                    if all([cid, cname, credit, tid]):
                        res = db_execute(
                            "INSERT INTO course (cid, cname, credit, tid) VALUES (%s, %s, %s, %s)",
                            [cid, cname, credit, teacher_options[tid]]
                        )
                        if res:
                            st.success("添加成功！")
                            st.rerun()
                        else:
                            st.error("添加失败！")
                    else:
                        st.warning("请填写所有字段！")

# 学生管理界面


def student_management():
    st.markdown("""
        <div class="page-title">
            <h1>👨‍🎓 学生管理</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        tab1, tab2 = st.tabs(["学生列表", "添加学生"])

        with tab1:
            # 显示学生列表，使用province字段
            results, description = db_query("""
                SELECT sid, sname, sex, birthday, province, class,
                       TIMESTAMPDIFF(YEAR, birthday, CURDATE()) as age 
                FROM student
            """)
            if results:
                # 创建DataFrame并设置列名
                df = pd.DataFrame(results, columns=[
                    "学号", "姓名", "性别", "出生日期", "籍贯", "班级", "年龄"
                ])
                # 调整列顺序
                display_df = df[["学号", "姓名", "性别", "出生日期", "年龄", "班级", "籍贯"]]
                st.dataframe(display_df)

                # 删除学生功能
                with st.form("delete_student"):
                    sid = st.text_input("输入要删除的学生学号")
                    if st.form_submit_button("删除"):
                        if sid:
                            res = db_execute(
                                "DELETE FROM student WHERE sid = %s",
                                [sid]
                            )
                            if res:
                                st.success("删除成功！")
                                st.rerun()
                            else:
                                st.error("删除失败！")
                        else:
                            st.warning("请输入学号！")

        with tab2:
            # 修改添加学生表单，使用province字段
            with st.form("add_student"):
                sid = st.text_input("学号")
                sname = st.text_input("姓名")
                sex = st.selectbox("性别", ["男", "女"])
                birthday = st.date_input("出生日期")
                province = st.text_input("籍贯")  # 修改字段名和显示名
                class_name = st.text_input("班级")

                if st.form_submit_button("添加"):
                    if all([sid, sname, sex, birthday, province, class_name]):
                        res = db_execute(
                            "INSERT INTO student (sid, sname, sex, birthday, province, class) VALUES (%s, %s, %s, %s, %s, %s)",
                            [sid, sname, sex, birthday, province, class_name]
                        )
                        if res:
                            st.success("添加成功！")
                            st.rerun()
                        else:
                            st.error("添加失败！")
                    else:
                        st.warning("请填写所有字段！")

# 教师管理界面


def teacher_management():
    st.markdown("""
        <div class="page-title">
            <h1>👨‍🏫 教师管理</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        tab1, tab2 = st.tabs(["教师列表", "添加教师"])

        with tab1:
            # 显示教师列表
            results, description = db_query("SELECT * FROM teacher")
            if results:
                df = pd.DataFrame(results, columns=[
                    "教师编号", "教师姓名", "职称"
                ])
                st.dataframe(df)

                # 修改教师职称
                with st.form("update_teacher"):
                    tid = st.text_input("教师编号")
                    title = st.text_input("新职称")
                    if st.form_submit_button("修改职称"):
                        if all([tid, title]):
                            res = db_execute(
                                "UPDATE teacher SET title = %s WHERE tid = %s",
                                [title, tid]
                            )
                            if res:
                                st.success("修改成功！")
                                st.rerun()
                            else:
                                st.error("修改失败！")
                        else:
                            st.warning("请填写所有字段！")

        with tab2:
            # 添加教师表单
            with st.form("add_teacher"):
                tid = st.text_input("教师编号")
                tname = st.text_input("教师姓名")
                title = st.text_input("职称")

                if st.form_submit_button("添加"):
                    if all([tid, tname, title]):
                        res = db_execute(
                            "INSERT INTO teacher (tid, tname, title) VALUES (%s, %s, %s)",
                            [tid, tname, title]
                        )
                        if res:
                            st.success("添加成功！")
                            st.rerun()
                        else:
                            st.error("添加失败！")
                    else:
                        st.warning("请填写所有字段！")

# 成绩查询界面


def grade_management():
    st.markdown("""
        <div class="page-title">
            <h1>📊 成绩查询</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        # 成绩查询SQL
        sql = """
        SELECT student.sid, student.sname, student.class, student.sex, 
               TIMESTAMPDIFF(YEAR, student.birthday, CURDATE()) as age,
               course.cname, grade.score, teacher.tname
        FROM student, course, teacher, grade
        WHERE student.sid = grade.sid 
        AND course.cid = grade.cid 
        AND course.tid = teacher.tid
        ORDER BY student.sid,grade.score
        """

        results, description = db_query(sql)
        if results:
            df = pd.DataFrame(results, columns=[
                "学号", "姓名", "班级", "性别", "年龄", "课程名", "成绩", "教师姓名"
            ])

            # 显示成绩数据表
            st.subheader("成绩数据表")
            st.dataframe(df)

            # 导出Excel功能 - 直接导出下载
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='成绩单', index=False)

            st.download_button(
                label="导出成绩单",
                data=buffer.getvalue(),
                file_name="成绩单.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # 数据可视化部分
            st.subheader("成绩数据可视化")

            # 使用下拉框选择图表类型，设置宽度
            col1, col2 = st.columns([1, 5])  # 改为1:5的比例
            with col1:
                chart_type = st.selectbox(
                    "选择图表类型",
                    ["成绩等级分布", "课程成绩分析", "班级成绩对比"],
                    help="选择不同的图表类型来分析成绩数据"
                )

            if chart_type == "成绩等级分布":
                # 计算成绩分布
                def get_grade_level(score):
                    if score >= 90:
                        return '优秀 (90-100)'
                    elif score >= 80:
                        return '良好 (80-89)'
                    elif score >= 70:
                        return '中等 (70-79)'
                    elif score >= 60:
                        return '及格 (60-69)'
                    else:
                        return '不及格 (0-59)'

                df['成绩等级'] = df['成绩'].apply(get_grade_level)
                grade_dist = df['成绩等级'].value_counts().sort_index()

                # 使用简单饼图
                pie = (
                    Pie(init_opts=opts.InitOpts(height="400px", width="600px"))
                    .add(
                        series_name="成绩等级分布",
                        data_pair=[(k, v) for k, v in grade_dist.items()],
                        radius=["0%", "70%"],
                        center=["50%", "50%"],
                        label_opts=opts.LabelOpts(
                            position="outside",
                            formatter="{b}: {c}门\n{d}%",  # 只修改单位
                            font_size=12,
                            font_weight="bold"
                        )
                    )
                    .set_global_opts(
                        title_opts=opts.TitleOpts(
                            title="成绩等级分布",
                            subtitle=f"总课程数: {len(df['课程名'].unique())}门",
                            pos_left="center"
                        ),
                        legend_opts=opts.LegendOpts(
                            orient="vertical",
                            pos_left="5%",
                            pos_top="middle",
                            item_gap=12,
                            textstyle_opts=opts.TextStyleOpts(font_size=12)
                        )
                    )
                )
                st_pyecharts(pie)

            elif chart_type == "课程成绩分析":
                # 计算每门课程的平均分和及格率
                course_stats = df.groupby('课程名').agg({
                    '成绩': ['mean', lambda x: (x >= 60).mean() * 100]
                }).round(2)
                course_stats.columns = ['平均分', '及格率']

                # 创建双Y轴柱状图
                bar = (
                    Bar(init_opts=opts.InitOpts(
                        height="400px",
                        width="600px"))  # 缩短图表整体宽度
                    .add_xaxis(list(course_stats.index))
                    .add_yaxis(
                        "平均分",
                        list(course_stats['平均分']),
                        yaxis_index=0,
                        itemstyle_opts=opts.ItemStyleOpts(
                            color="#5470c6",
                            opacity=0.8
                        ),
                        bar_width=20,  # 进一步减小柱子宽度
                        gap="2%"       # 减小柱子间距
                    )
                    .extend_axis(
                        yaxis=opts.AxisOpts(
                            name="及格率(%)",
                            min_=0,
                            max_=100,
                            position="right",
                            interval=20,  # 设置刻度间隔
                            axisline_opts=opts.AxisLineOpts(
                                linestyle_opts=opts.LineStyleOpts(
                                    color="#91cc75")
                            ),
                            axislabel_opts=opts.LabelOpts(
                                formatter="{value}%",
                                margin=12  # 增加标签边距
                            )
                        )
                    )
                    .set_global_opts(
                        title_opts=opts.TitleOpts(
                            title="课程成绩分析",
                            pos_left="center"  # 标题居中
                        ),
                        xaxis_opts=opts.AxisOpts(
                            axislabel_opts=opts.LabelOpts(rotate=-15),
                            axisline_opts=opts.AxisLineOpts(
                                linestyle_opts=opts.LineStyleOpts(width=2)
                            )
                        ),
                        yaxis_opts=opts.AxisOpts(
                            name="分数",
                            min_=0,
                            max_=100,
                            interval=10,  # 设置刻度间隔
                            axisline_opts=opts.AxisLineOpts(
                                linestyle_opts=opts.LineStyleOpts(width=2)
                            ),
                            axislabel_opts=opts.LabelOpts(margin=12)  # 增加标签边距
                        ),
                        tooltip_opts=opts.TooltipOpts(
                            trigger="axis",
                            axis_pointer_type="cross"
                        ),
                        legend_opts=opts.LegendOpts(
                            pos_top="5%",
                            pos_right="10%"  # 图例居右
                        )
                    )
                )

                line = (
                    Line()
                    .add_xaxis(list(course_stats.index))
                    .add_yaxis(
                        "及格率",
                        list(course_stats['及格率']),
                        yaxis_index=1,
                        itemstyle_opts=opts.ItemStyleOpts(color="#91cc75")
                    )
                )

                bar.overlap(line)
                st_pyecharts(bar)

            elif chart_type == "班级成绩对比":
                # 计算每个班级的平均分和标准差
                class_stats = df.groupby(['班级', '课程名'])[
                    '成绩'].agg(['mean', 'std']).round(2)
                class_avg = class_stats['mean'].unstack()

                # 创建雷达图
                radar = (
                    Radar(init_opts=opts.InitOpts(
                        height="800px",     # 继续增加高度
                        width="1200px"))    # 继续增加宽度
                    .add_schema(
                        schema=[
                            opts.RadarIndicatorItem(name=course, max_=100)
                            for course in class_avg.columns
                        ],
                        splitarea_opt=opts.SplitAreaOpts(
                            is_show=True,
                            areastyle_opts=opts.AreaStyleOpts(opacity=1)
                        ),
                        textstyle_opts=opts.TextStyleOpts(font_size=12),
                        radius="85%"  # 继续增加雷达图的半径
                    )
                )

                colors = ["#5470c6", "#91cc75", "#fac858", "#ee6666"]
                for idx, class_name in enumerate(class_avg.index):
                    radar.add(
                        class_name,
                        [list(class_avg.loc[class_name])],
                        color=colors[idx % len(colors)],
                        linestyle_opts=opts.LineStyleOpts(width=2)
                    )

                radar.set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="班级成绩雷达图",
                        pos_left="center"  # 只添加标题居中
                    ),
                    legend_opts=opts.LegendOpts(pos_right="5%")
                )
                st_pyecharts(radar)

# 主界面


def inject_sidebar_style():
    st.markdown("""
        <style>
        /* 侧边栏背景和整体样式 */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem 1rem;
            border-right: 1px solid #dee2e6;
        }
        
        /* 侧边栏标题样式 */
        .sidebar-title {
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .sidebar-title h2 {
            color: white;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        /* 菜单项样式 */
        .stRadio > label {
            display: none;  /* 隐藏Radio标签文本 */
        }
        .stRadio > div[role="radiogroup"] {
            border-radius: 10px;
            background: white;
            padding: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stRadio > div[role="radiogroup"] > label {
            color: #495057 !important;
            font-size: 1rem;
            font-weight: 500;
            background: transparent;
            border-radius: 8px;
            padding: 0.8rem 1rem;
            margin: 0.2rem 0;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }
        .stRadio > div[role="radiogroup"] > label:hover {
            background: #f8f9fa;
            border-color: #4a90e2;
            transform: translateX(3px);
            color: #4a90e2 !important;
        }
        .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
            background: #4a90e2;
            color: white !important;
            box-shadow: 0 2px 4px rgba(74, 144, 226, 0.2);
        }
        
        /* 分割线样式 */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, 
                rgba(74, 144, 226, 0) 0%, 
                rgba(74, 144, 226, 0.2) 50%, 
                rgba(74, 144, 226, 0) 100%);
            margin: 1.5rem 0;
        }
        
        /* 退出按钮样式 */
        .stButton button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%) !important;
            color: white !important;
            padding: 0.8rem 1.5rem !important;
            border-radius: 8px !important;
            border: none !important;
            width: 50% !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 4px rgba(255, 82, 82, 0.2) !important;
            transition: all 0.2s ease !important;
            display: block !important;
            margin: 0 auto !important; /* 按钮居中 */
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #ff5252 0%, #ff4242 100%) !important;
            box-shadow: 0 4px 8px rgba(255, 82, 82, 0.3) !important;
            transform: translateY(-1px) !important;
        }
        .stButton button:active {
            transform: translateY(1px) !important;
        }
        
        /* 工具提示样式 */
        button[data-baseweb="tooltip"] {
            background: rgba(74, 144, 226, 0.1);
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)


def inject_main_content_style():
    st.markdown("""
        <style>
        /* 主内容区域样式 */
        section.main > div {
            padding: 1rem 2rem;
            max-width: none;
        }
        
        # /* 页面标题样式 */
        # .page-title {
        #     background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        #     padding: 1.2rem 2rem;
        #     border-radius: 12px;
        #     margin-bottom: 1.5rem;
        #     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        # }
        # .page-title h1 {
        #     color: #2c3e50;
        #     font-size: 1.8rem;
        #     font-weight: 600;
        #     margin: 0;
        #     display: flex;
        #     align-items: center;
        #     gap: 0.8rem;
        # }
        
        /* 数据表格样式 */
        .stDataFrame {
            background: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        .dataframe {
            width: 100%;
            margin-bottom: 1rem;
            border-collapse: separate;
            border-spacing: 0;
        }
        .dataframe th {
            background: #f8f9fa;
            padding: 0.75rem 1rem;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #dee2e6;
            text-align: center;
        }
        .dataframe td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #e9ecef;
            color: #495057;
        }
        .dataframe tr:last-child td {
            border-bottom: none;
        }
        .dataframe tr:hover td {
            background-color: #f8f9fa;
        }
        
        /* 表单样式 */
        .stForm > div {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            margin-bottom: 1rem;
        }
        .stTextInput > div > div, .stNumberInput > div > div {
            background: #ffffff;
        }
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            border: 1px solid #ced4da;
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            font-size: 0.95rem;
            transition: border-color 0.15s ease-in-out;
        }
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
            border-color: #6c757d;
            box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.1);
        }
        
        /* 按钮样式 */
        section.main .stButton > button {
            background: #6c757d !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1.5rem !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            width: auto !important;
            margin: 0.5rem 0 !important;
            box-shadow: none !important;
        }
        section.main .stButton > button:hover {
            background: #5a6268 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        section.main .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* 标签页样式 */
        .stTabs > div > div {
            gap: 0.5rem;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .stTabs button[role="tab"] {
            background: transparent;
            border: none;
            color: #495057;
            padding: 0.5rem 1rem;
            font-weight: 500;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        .stTabs button[role="tab"][aria-selected="true"] {
            background: #6c757d;
            color: white;
        }
        .stTabs button[role="tab"]:hover:not([aria-selected="true"]) {
            background: rgba(108, 117, 125, 0.1);
            color: #6c757d;
        }
        
        /* 图表容器样式 */
        div[data-testid="stMetric"], div[data-testid="stMetricValue"] {
            background: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* 提示信息样式 */
        .stAlert {
            padding: 0.75rem 1rem;
            border-radius: 6px;
            margin: 1rem 0;
        }
        .element-container iframe {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)


def main():
    inject_sidebar_style()
    inject_main_content_style()

    # 侧边栏标题
    st.sidebar.markdown("""
        <div class="sidebar-title">
            <h2>教学管理系统</h2>
        </div>
    """, unsafe_allow_html=True)

    # 侧边栏菜单
    menu_options = {
        "📚 课程管理": "course",
        "👨‍🎓 学生管理": "student",
        "👨‍🏫 教师管理": "teacher",
        "📊 成绩查询": "grade",
    }

    # 修复空label警告
    choice = st.sidebar.radio(
        "功能菜单",  # 添加label
        list(menu_options.keys()),
        label_visibility="collapsed"  # 隐藏label但保持可访问性
    )

    # 添加分隔线
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    # 退出按钮
    if st.sidebar.button("退出登录", key="logout"):
        st.session_state['authenticated'] = False
        st.rerun()

    # 根据选择显示不同的功能界面
    if "课程管理" in choice:
        course_management()
    elif "学生管理" in choice:
        student_management()
    elif "教师管理" in choice:
        teacher_management()
    elif "成绩查询" in choice:
        grade_management()


# 主程序入口
if __name__ == "__main__":
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        login()
    else:
        main()
