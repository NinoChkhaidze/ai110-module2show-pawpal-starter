import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Owner & Pet setup (persisted in session state) ---
with st.form("owner_form"):
    st.subheader("Owner & Pet Setup")
    col1, col2, col3 = st.columns(3)
    with col1:
        owner_name = st.text_input("Owner name", value="Jordan")
    with col2:
        start_hour = st.number_input("Available from (hour)", min_value=0, max_value=23, value=8)
    with col3:
        end_hour = st.number_input("Available until (hour)", min_value=0, max_value=23, value=18)
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)
    submitted = st.form_submit_button("Save owner & pet")

if submitted or "owner" not in st.session_state:
    pet = Pet(age=int(pet_age))
    # carry over existing tasks when owner is updated
    if "owner" in st.session_state:
        pet.tasks = st.session_state.owner.pet.tasks
    st.session_state.owner = Owner(
        name=owner_name,
        available_start=int(start_hour) * 60,
        available_end=int(end_hour) * 60,
        pet=pet
    )

owner = st.session_state.owner

st.divider()

# --- Add task form ---
st.subheader("Add a Care Task")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    owner.pet.add_task(Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority
    ))
    st.success(f"Added: {task_title}")

# --- Task list ---
pending = owner.pet.get_pending_tasks()
if pending:
    _preview_scheduler = Scheduler(owner)
    sorted_pending = _preview_scheduler.sort_by_time(pending)
    st.markdown("**Current tasks (sorted by start time):**")
    st.table([
        {
            "Task": t.title,
            "Start": t.start_time if t.start_time else "—",
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority.capitalize(),
        }
        for t in sorted_pending
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate schedule ---
st.subheader("Generate Today's Schedule")
st.caption(f"Time window: {start_hour}:00 – {end_hour}:00 ({(int(end_hour) - int(start_hour)) * 60} min available)")

if st.button("Generate schedule"):
    if not pending:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        scheduled = scheduler.generate_schedule()

        # --- Conflict warnings (shown first so owner sees them immediately) ---
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("⚠️ Schedule conflicts detected — two or more tasks overlap in time. Please adjust start times or durations.")
            for warning in conflicts:
                # Extract the two task names for a plain-English message
                st.warning(warning)

        # --- Scheduled tasks table ---
        if scheduled:
            st.success(f"Schedule ready — {len(scheduled)} task(s) fit in your time window.")
            sorted_scheduled = scheduler.sort_by_time(scheduled)
            st.table([
                {
                    "Start": t.start_time,
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority.capitalize(),
                }
                for t in sorted_scheduled
            ])

        # --- Skipped tasks ---
        if scheduler.skipped_tasks:
            st.warning(f"{len(scheduler.skipped_tasks)} task(s) didn't fit in today's window and were skipped.")
            st.table([
                {
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority.capitalize(),
                }
                for t in scheduler.skipped_tasks
            ])
