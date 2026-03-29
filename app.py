import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

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

		st.success("✓ Schedule generated!")

		st.write("### Today's Schedule")
		if plan:
			total_minutes = sum(task.duration_minutes for task in plan)
			st.write(f"**{len(plan)} task(s), {total_minutes} minutes total**")

			for idx, task in enumerate(plan, start=1):
				col1, col2, col3, col4 = st.columns(4)
				with col1:
					st.write(f"**{idx}. {task.title}**")
				with col2:
					st.write(f"{task.duration_minutes} min")
				with col3:
					st.write(f"Priority: {task.priority}")
				with col4:
					st.write(f"Time: {task.preferred_time}")
				st.write(f"Pet: {task.pet_name}")
				st.divider()
		else:
			st.info("No tasks could fit within the time limit.")

		st.write("### Plan Explanation")
		st.info(scheduler.last_explanation)

		if scheduler.last_skipped:
			st.write("### Skipped Tasks")
			for task in scheduler.last_skipped:
				st.write(f"- {task.title} ({task.duration_minutes} min) - {task.pet_name}")
