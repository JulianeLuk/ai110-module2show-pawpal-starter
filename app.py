import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


def import_pandas_and_create_df(data):
	import pandas as pd
	return pd.DataFrame(data)


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+"""
)

with st.expander("Overview", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

"""
    )
""""""


st.divider()

# Initialize session state once
if "owner" not in st.session_state:
	st.session_state.owner = Owner(name="Jordan", time_available_minutes=120)
	st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.subheader("Owner Settings")
owner.time_available_minutes = st.slider(
	"Daily time available (minutes)", min_value=30, max_value=240, value=owner.time_available_minutes
)

st.subheader("Manage Pets")
col1, col2 = st.columns(2)
with col1:
	new_pet_name = st.text_input("New pet name", value="")
	species = st.selectbox("Species", ["dog", "cat", "other"])
	age = st.number_input("Age", min_value=1, max_value=50, value=3)

with col2:
	if st.button("Add Pet"):
		if new_pet_name:
			new_pet = Pet(name=new_pet_name, species=species, age=age)
			owner.add_pet(new_pet)
			st.success(f"✓ Added pet: {new_pet_name}")
		else:
			st.error("Please enter a pet name.")

if owner.pets:
	st.write("**Current Pets:**")
	for pet in owner.pets:
		st.write(f"- {pet.name} ({pet.species}, age {pet.age}) - {len(pet.tasks)} task(s)")
else:
	st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to your pets for scheduling.")

if owner.pets:
	selected_pet = st.selectbox("Select pet", [pet.name for pet in owner.pets])
	task_title = st.text_input("Task title", value="")
	col1, col2, col3 = st.columns(3)
	with col1:
		duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15)
	with col2:
		priority = st.selectbox("Priority", ["low", "medium", "high"])
	with col3:
		preferred_time = st.selectbox("Preferred time", ["08:00", "12:00", "14:00", "18:00", "20:00"])

	if st.button("Add Task"):
		if task_title:
			import uuid
			task_id = f"T{uuid.uuid4().hex[:8]}"
			task = Task(
				task_id=task_id,
				title=task_title,
				duration_minutes=int(duration),
				priority=priority,
				preferred_time=preferred_time,
			)
			success = owner.add_task_to_pet(selected_pet, task)
			if success:
				st.success(f"✓ Added task '{task_title}' to {selected_pet}")
			else:
				st.error(f"Pet '{selected_pet}' not found.")
		else:
			st.error("Please enter a task title.")

	st.write("**Tasks by Pet:**")
	for pet in owner.pets:
		if pet.tasks:
			st.write(f"**{pet.name}**")
			for task in pet.tasks:
				status = "✓" if task.completed else "○"
				st.write(
					f"  {status} {task.title} - {task.duration_minutes} min "
					f"({task.priority}) @ {task.preferred_time}"
				)
		else:
			st.write(f"**{pet.name}** - no tasks")
else:
	st.info("Add a pet first to assign tasks.")
st.divider()

st.subheader("Build Schedule")
st.caption("Generate today's optimized schedule based on priorities and time availability.")

if st.button("Generate schedule"):
	if not owner.pets or not owner.get_all_tasks():
		st.warning("Add pets and tasks first to generate a schedule.")
	else:
		plan = scheduler.generate_daily_plan(owner)
		all_tasks = owner.get_all_tasks()

		st.success("✓ Schedule generated!")

		# ===== CONFLICT DETECTION =====
		conflicts = scheduler.detect_conflicts(all_tasks)
		if conflicts:
			st.markdown("### ⚠️ Scheduling Conflicts Detected")
			for conflict_msg in conflicts:
				st.warning(conflict_msg)
			st.markdown(
				"💡 **Tip:** Consider rescheduling one of the conflicting tasks to avoid double-booking your pets."
			)

		# ===== TODAY'S SORTED SCHEDULE =====
		st.markdown("### 📅 Today's Schedule (By Time)")
		if plan:
			total_minutes = sum(task.duration_minutes for task in plan)
			
			# Display as a professional table
			schedule_data = []
			for idx, task in enumerate(plan, start=1):
				schedule_data.append({
					"#": idx,
					"Task": task.title,
					"Pet": task.pet_name,
					"Time": task.preferred_time,
					"Duration": f"{task.duration_minutes} min",
					"Priority": task.priority.upper(),
				})
			
			st.dataframe(
				import_pandas_and_create_df(schedule_data),
				use_container_width=True,
				hide_index=True,
			)
			
			col1, col2, col3 = st.columns(3)
			with col1:
				st.metric("Tasks Today", len(plan))
			with col2:
				st.metric("Total Time", f"{total_minutes} min")
			with col3:
				time_left = owner.time_available_minutes - total_minutes
				st.metric("Time Left", f"{time_left} min")
		else:
			st.info("No tasks could fit within the time limit.")

		st.divider()

		# ===== PLAN EXPLANATION =====
		st.markdown("### 📝 Plan Explanation")
		st.info(scheduler.last_explanation)

		# ===== SKIPPED TASKS WARNING =====
		if scheduler.last_skipped:
			st.markdown("### ⏭️ Tasks Not Scheduled (Time Limit)")
			skipped_data = []
			for task in scheduler.last_skipped:
				skipped_data.append({
					"Task": task.title,
					"Pet": task.pet_name,
					"Duration": f"{task.duration_minutes} min",
					"Priority": task.priority.upper(),
				})
			st.dataframe(
				import_pandas_and_create_df(skipped_data),
				use_container_width=True,
				hide_index=True,
			)
			st.caption("💡 Increase available time or mark some tasks complete to fit more tasks.")

st.divider()

# ===== TASK ANALYSIS TOOLS =====
st.subheader("📊 Task Analysis")
st.caption("Explore, filter, and sort all tasks to understand your pet care workload.")

analysis_mode = st.radio(
	"Select analysis view:",
	["All Tasks (Sorted by Time)", "Tasks by Pet", "Tasks by Status"]
)

all_tasks = owner.get_all_tasks()

if analysis_mode == "All Tasks (Sorted by Time)":
	if all_tasks:
		sorted_tasks = scheduler.sort_by_time(all_tasks)
		st.markdown("##### ⏰ Tasks in Chronological Order")
		
		task_data = []
		for task in sorted_tasks:
			task_data.append({
				"Time": task.preferred_time if task.preferred_time != "any" else "Flexible",
				"Task": task.title,
				"Pet": task.pet_name,
				"Duration": f"{task.duration_minutes} min",
				"Priority": task.priority.upper(),
				"Status": "✓ Done" if task.completed else "○ Pending",
			})
		
		st.dataframe(
			import_pandas_and_create_df(task_data),
			use_container_width=True,
			hide_index=True,
		)
	else:
		st.info("No tasks yet. Add tasks above.")

elif analysis_mode == "Tasks by Pet":
	if owner.pets:
		selected_analysis_pet = st.selectbox(
			"Choose a pet:",
			[pet.name for pet in owner.pets],
			key="pet_analysis"
		)
		
		pet_tasks = scheduler.filter_by_pet(all_tasks, selected_analysis_pet)
		
		if pet_tasks:
			st.markdown(f"##### Tasks for **{selected_analysis_pet}**")
			
			pet_task_data = []
			for task in pet_tasks:
				pet_task_data.append({
					"Task": task.title,
					"Time": task.preferred_time if task.preferred_time != "any" else "Flexible",
					"Duration": f"{task.duration_minutes} min",
					"Priority": task.priority.upper(),
					"Status": "✓ Done" if task.completed else "○ Pending",
				})
			
			st.dataframe(
				import_pandas_and_create_df(pet_task_data),
				use_container_width=True,
				hide_index=True,
			)
			
			col1, col2 = st.columns(2)
			with col1:
				st.metric("Total Tasks", len(pet_tasks))
			with col2:
				total_dur = sum(t.duration_minutes for t in pet_tasks)
				st.metric("Total Duration", f"{total_dur} min")
		else:
			st.info(f"No tasks for {selected_analysis_pet} yet.")
	else:
		st.info("Add a pet first.")

elif analysis_mode == "Tasks by Status":
	col1, col2 = st.columns(2)
	
	with col1:
		st.markdown("##### ○ Pending Tasks")
		pending = scheduler.filter_by_status(all_tasks, completed=False)
		if pending:
			pending_data = []
			for task in pending:
				pending_data.append({
					"Task": task.title,
					"Pet": task.pet_name,
					"Time": task.preferred_time if task.preferred_time != "any" else "Flexible",
					"Duration": f"{task.duration_minutes} min",
				})
			st.dataframe(
				import_pandas_and_create_df(pending_data),
				use_container_width=True,
				hide_index=True,
			)
			st.metric("Pending", len(pending))
		else:
			st.success("All tasks completed! 🎉")
	
	with col2:
		st.markdown("##### ✓ Completed Tasks")
		completed = scheduler.filter_by_status(all_tasks, completed=True)
		if completed:
			completed_data = []
			for task in completed:
				completed_data.append({
					"Task": task.title,
					"Pet": task.pet_name,
					"Duration": f"{task.duration_minutes} min",
				})
			st.dataframe(
				import_pandas_and_create_df(completed_data),
				use_container_width=True,
				hide_index=True,
			)
			st.metric("Completed", len(completed))
		else:
			st.info("No completed tasks yet.")

