
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Intelligent Timetable Planner",
    page_icon="📚",
    layout="wide"
)



# =====================================
# 2. COLORFUL WEBSITE DESIGN
# =====================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #eef5ff, #f5f0ff);
    color: #243451 !important;
}

/* Main content */
.main .block-container {
    padding-top: 2rem;
}

/* All headings */
h1 {
    color: #273c75 !important;
    font-weight: 800 !important;
}

h2 {
    color: #344e9b !important;
    font-weight: 700 !important;
}

h3 {
    color: #5145a5 !important;
    font-weight: 700 !important;
}

/* Normal text */
p, label, li, span {
    color: #334155;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #dbeafe, #ede9fe);
}

section[data-testid="stSidebar"] * {
    color: #253765 !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #eaf2ff);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #c7d8fa;
    box-shadow: 0 4px 12px rgba(60, 80, 140, 0.10);
}

div[data-testid="stMetric"] label {
    color: #52658b !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #3448a5 !important;
    font-weight: 800;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #4776e6, #8e54e9);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton button:hover {
    background: linear-gradient(90deg, #365dc7, #7138c7);
    color: white !important;
    transform: translateY(-2px);
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    background-color: white !important;
    color: #253765 !important;
    border-radius: 8px;
}

/* Data tables */
div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #d5def0;
    overflow: hidden;
}

/* Information boxes */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Progress bar */
div[data-testid="stProgressBar"] > div {
    background-color: #dbeafe;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #4776e6, #14b8a6);
}

/* Horizontal divider */
hr {
    border-color: #cbd5e1;
}

/* Radio buttons */
.stRadio label {
    color: #253765 !important;
}

/* Select box text */
.stSelectbox label,
.stMultiSelect label,
.stTextInput label {
    color: #253765 !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# 3. SESSION STATE
# =====================================

if "subjects" not in st.session_state:
    st.session_state.subjects = pd.DataFrame({
        "Subject": ["Mathematics", "Python", "DBMS", "DMS"],
        "Priority": [5, 4, 3, 5],
        "Difficulty": [5, 3, 3, 4],
        "Hours per Week": [5, 4, 3, 4]
    })

if "timetable" not in st.session_state:
    st.session_state.timetable = pd.DataFrame()

# =====================================
# 4. TIMETABLE GENERATION FUNCTION
# =====================================

def generate_timetable(
    subjects,
    days,
    start_hour,
    end_hour,
    session_minutes,
    break_minutes
):

    schedule = []

    remaining = {
        row["Subject"]: int(row["Hours per Week"]) * 60
        for _, row in subjects.iterrows()
    }

    previous_subject = None

    subject_details = {
        row["Subject"]: {
            "priority": int(row["Priority"]),
            "difficulty": int(row["Difficulty"])
        }
        for _, row in subjects.iterrows()
    }

    for day in days:

        current = datetime.combine(
            datetime.today().date(),
            datetime.min.time()
        ).replace(hour=start_hour)

        end_time = current.replace(hour=end_hour)

        while current + timedelta(minutes=session_minutes) <= end_time:

            available = [
                subject for subject in remaining
                if remaining[subject] >= session_minutes
            ]

            if not available:
                break

            def score(subject):

                priority = subject_details[subject]["priority"]
                difficulty = subject_details[subject]["difficulty"]

                value = (
                    priority * 2
                    + difficulty
                    + remaining[subject] / 60
                )

                if subject == previous_subject:
                    value -= 3

                return value

            selected = max(available, key=score)

            finish = current + timedelta(minutes=session_minutes)

            schedule.append({
                "Day": day,
                "Start Time": current.strftime("%I:%M %p"),
                "End Time": finish.strftime("%I:%M %p"),
                "Subject": selected,
                "Duration": session_minutes
            })

            remaining[selected] -= session_minutes

            previous_subject = selected

            current = finish + timedelta(minutes=break_minutes)

    return pd.DataFrame(schedule), remaining


# =====================================
# 5. SIDEBAR NAVIGATION
# =====================================

st.sidebar.title("📚 Smart Planner")

pages = [
    "Dashboard",
    "Manage Subjects",
    "Generate Timetable",
    "Weekly Timetable",
    "About Project"
]

if "dashboard_navigation" in st.session_state:

    default_page = st.session_state.pop(
        "dashboard_navigation"
    )

else:
    default_page = "Dashboard"

page = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(default_page),
    key="main_navigation"
)
st.sidebar.markdown("---")
st.sidebar.success("Study Smart. Achieve More!")



# =====================================
# 6. PROFESSIONAL DASHBOARD
# =====================================

if page == "Dashboard":

    st.markdown("""
<h1 style="
    background: linear-gradient(90deg, #315bd5, #8e54e9, #0d9488);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 38px;
">
📚 Intelligent Timetable Planner
</h1>
""", unsafe_allow_html=True)

    st.write(
        "Welcome to your AI-powered academic planning dashboard."
    )

    st.markdown("---")

    subjects = st.session_state.subjects
    timetable = st.session_state.timetable

    # Dashboard metrics

    total_subjects = len(subjects)

    planned_hours = subjects["Hours per Week"].sum()

    total_sessions = len(timetable)

    scheduled_hours = (
        timetable["Duration"].sum() / 60
        if not timetable.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Total Subjects",
            total_subjects
        )

    with col2:
        st.metric(
            "⏰ Planned Hours",
            f"{planned_hours} hrs"
        )

    with col3:
        st.metric(
            "📅 Study Sessions",
            total_sessions
        )

    with col4:
        st.metric(
            "✅ Scheduled Hours",
            f"{scheduled_hours:.1f} hrs"
        )

    st.markdown("---")

    # Subject priority chart

    st.subheader("📊 Subject Priority Analysis")

    if not subjects.empty:

        priority_data = subjects[
            ["Subject", "Priority"]
        ].set_index("Subject")

        st.bar_chart(
            priority_data,
            y="Priority",
            color="#3989D6"
        )

    st.markdown("---")

    # Study hours comparison

    st.subheader("📈 Study Hours Analysis")

    if not subjects.empty:

        if not timetable.empty:

            actual_hours = (
                timetable.groupby("Subject")["Duration"]
                .sum() / 60
            )

        else:

            actual_hours = pd.Series(dtype=float)

        comparison = subjects[
            ["Subject", "Hours per Week"]
        ].copy()

        comparison["Scheduled Hours"] = (
            comparison["Subject"]
            .map(actual_hours)
            .fillna(0)
        )

        comparison = comparison.rename(
            columns={
                "Hours per Week": "Target Hours"
            }
        )

        comparison_chart = comparison.set_index("Subject")[
            ["Target Hours", "Scheduled Hours"]
        ]

        st.bar_chart(
            comparison_chart,
            color=["#2563eb", "#14b8a6"]
        )

    st.markdown("---")

    # Weekly progress

    st.subheader("🎯 Weekly Study Progress")

    if planned_hours > 0:

        progress = min(
            scheduled_hours / planned_hours,
            1.0
        )

        st.progress(progress)

        st.write(
            f"{scheduled_hours:.1f} of "
            f"{planned_hours} planned hours scheduled."
        )

        st.caption(
            f"Schedule coverage: {progress * 100:.1f}%"
        )

    else:

        st.info("Add subjects to calculate study progress.")

    st.markdown("---")

    # Weekly timetable preview

    st.subheader("📅 Timetable Preview")

    if not timetable.empty:

        st.dataframe(
            timetable.head(10),
            use_container_width=True,
            hide_index=True
        )

        if len(timetable) > 10:

            st.caption(
                "Showing the first 10 sessions. "
                "Visit Weekly Timetable to see the complete schedule."
            )

    else:

        st.info(
            "Your timetable is not generated yet. "
            "Go to Generate Timetable to get started."
        )

    st.markdown("---")

    st.subheader("🚀 Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📖 Manage My Subjects",
            use_container_width=True
        ):

            st.session_state["dashboard_navigation"] = (
                "Manage Subjects"
            )
            st.rerun()

    with col2:

        if st.button(
            "🧠 Generate Timetable",
            use_container_width=True
        ):

            st.session_state["dashboard_navigation"] = (
                "Generate Timetable"
            )
            st.rerun()

# =====================================
# 7. MANAGE SUBJECTS
# =====================================

elif page == "Manage Subjects":

    st.title("📖 Manage Your Subjects")

    st.write("Add, edit or delete your academic subjects.")

    edited = st.data_editor(
        st.session_state.subjects,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )

    if st.button("💾 Save Subjects"):

        if edited.empty:
            st.error("Add at least one subject.")

        elif (
            edited["Subject"].isna().any()
            or edited["Subject"].astype(str).str.strip().eq("").any()
            or edited["Subject"].duplicated().any()
            or edited[
                ["Priority", "Difficulty", "Hours per Week"]
            ].isna().any().any()
        ):
            st.error("Please enter valid and unique subject details.")

        elif (
            (edited["Priority"] < 1).any()
            or (edited["Priority"] > 5).any()
            or (edited["Difficulty"] < 1).any()
            or (edited["Difficulty"] > 5).any()
            or (edited["Hours per Week"] < 1).any()
        ):
            st.error("Check your priority, difficulty and study hours.")

        else:
            st.session_state.subjects = edited.reset_index(drop=True)
            st.success("Subjects saved successfully!")

# =====================================
# 8. GENERATE TIMETABLE
# =====================================

elif page == "Generate Timetable":

    st.title("🧠 Generate Intelligent Timetable")

    st.write(
        "Choose your study days and available timings."
    )

    days = st.multiselect(
        "Select Study Days",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ],
        default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )

    col1, col2 = st.columns(2)

    with col1:
        start_hour = st.selectbox(
            "Start Time",
            list(range(5, 19)),
            index=4
        )

    with col2:
        end_hour = st.selectbox(
            "End Time",
            list(range(10, 24)),
            index=8
        )

    col3, col4 = st.columns(2)

    with col3:
        session_minutes = st.selectbox(
            "Study Session Duration",
            [25, 30, 45, 50, 60, 90],
            index=3
        )

    with col4:
        break_minutes = st.selectbox(
            "Break Duration",
            [5, 10, 15, 20, 30],
            index=2
        )

    st.subheader("Your Subject Details")

    st.dataframe(
        st.session_state.subjects,
        use_container_width=True,
        hide_index=True
    )

    if st.button("✨ Generate My Timetable"):

        subjects = st.session_state.subjects

        if subjects.empty:
            st.error("Please add subjects first.")

        elif not days:
            st.error("Please select your study days.")

        elif start_hour >= end_hour:
            st.error("End time must be later than start time.")

        else:

            result, remaining = generate_timetable(
                subjects,
                days,
                start_hour,
                end_hour,
                session_minutes,
                break_minutes
            )

            st.session_state.timetable = result

            if result.empty:
                st.warning("No study sessions could be generated.")

            else:

                st.success("Your timetable is ready!")

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

                total_hours = result["Duration"].sum() / 60

                st.metric(
                    "Total Scheduled Study Hours",
                    f"{total_hours:.1f} Hours"
                )

                unallocated = {
                    subject: minutes
                    for subject, minutes in remaining.items()
                    if minutes > 0
                }

                if unallocated:
                    st.warning(
                        "Some subject study-hour targets could not fit "
                        "into the available schedule."
                    )
                    for subject, minutes in unallocated.items():
                        st.write(
                            f"{subject}: {minutes // 60}h "
                            f"{minutes % 60}m remaining"
                        )

# =====================================
# 9. WEEKLY TIMETABLE
# =====================================

elif page == "Weekly Timetable":

    st.title("📅 Your Weekly Timetable")

    timetable = st.session_state.timetable

    if timetable.empty:

        st.info(
            "No timetable available. "
            "Please generate your timetable first."
        )

    else:

        selected_day = st.selectbox(
            "Choose a Day",
            timetable["Day"].drop_duplicates().tolist()
        )

        daily = timetable[
            timetable["Day"] == selected_day
        ]

        st.subheader(f"Schedule for {selected_day}")

        for _, row in daily.iterrows():

            st.markdown(f"""
            <div style="
                background-color:white;
                padding:18px;
                margin:10px 0;
                border-radius:12px;
                border-left:5px solid #2563eb;
            ">
                <h3 style="color:#173b65;">
                    📘 {row['Subject']}
                </h3>
                <p style="color:#64748b;">
                    {row['Start Time']} - {row['End Time']}
                </p>
                <b>{row['Duration']} Minutes</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        csv = timetable.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Weekly Timetable",
            data=csv,
            file_name="weekly_timetable.csv",
            mime="text/csv"
        )

# =====================================
# 10. ABOUT PROJECT
# =====================================

elif page == "About Project":

    st.title("ℹ️ About Intelligent Timetable Planner")

    st.markdown("""
    ### Project Overview

    The Intelligent Timetable Planner is an AI-based
    study scheduling application designed to help students
    organize their academic activities efficiently.

    ### Main Objectives

    - Automatic timetable generation.
    - Subject priority analysis.
    - Difficulty-based study allocation.
    - Time management.
    - Automatic break scheduling.
    - Personalized study planning.

    ### Technologies Used

    - Python
    - Streamlit
    - Pandas
    - Intelligent Scheduling Algorithm

    ### How It Works

    1. Students enter their subjects.
    2. The system analyzes subject priorities.
    3. The system considers subject difficulty.
    4. The algorithm selects suitable study sessions.
    5. A weekly timetable is automatically generated.

    ### Future Enhancements

    - Machine Learning integration.
    - Student performance analysis.
    - Exam preparation planner.
    - Personalized recommendations.
    - Google Calendar integration.
    """)

# =====================================
# END OF APPLICATION
# =====================================
