from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
	owner = Owner(name="Jordan", time_available_minutes=95)

	dog = Pet(name="Mochi", species="dog", age=4)
	cat = Pet(name="Luna", species="cat", age=2)

	owner.add_pet(dog)
	owner.add_pet(cat)

	owner.add_task_to_pet(
		"Mochi",
		Task(
			task_id="T1",
			title="Morning Walk",
			duration_minutes=30,
			priority="high",
			preferred_time="08:00",
			frequency="daily",
		),
	)
	owner.add_task_to_pet(
		"Mochi",
		Task(
			task_id="T2",
			title="Evening Feed",
			duration_minutes=15,
			priority="high",
			preferred_time="18:30",
			frequency="daily",
		),
	)
	owner.add_task_to_pet(
		"Luna",
		Task(
			task_id="T3",
			title="Play Session",
			duration_minutes=20,
			priority="medium",
			preferred_time="14:00",
			frequency="daily",
		),
	)
	owner.add_task_to_pet(
		"Luna",
		Task(
			task_id="T4",
			title="Grooming",
			duration_minutes=40,
			priority="low",
			preferred_time="20:00",
			frequency="weekly",
		),
	)

	return owner


def print_schedule(owner: Owner, scheduler: Scheduler) -> None:
	schedule = scheduler.generate_daily_plan(owner)

	print("Today's Schedule")
	print("=" * 16)
	if not schedule:
		print("No tasks scheduled today.")
		return

	for index, task in enumerate(schedule, start=1):
		print(
			f"{index}. {task.title} ({task.pet_name}) - "
			f"{task.duration_minutes} min - priority: {task.priority} - "
			f"time: {task.preferred_time}"
		)

	print("\nPlan Explanation:")
	print(scheduler.last_explanation)


def test_sorting_and_filtering(owner: Owner, scheduler: Scheduler) -> None:
	"""Demonstrate sorting tasks by time and filtering by pet/status."""
	print("\n" + "="*50)
	print("FEATURE 1: SORTING AND FILTERING")
	print("="*50)
	
	all_tasks = owner.get_all_tasks()
	
	# Demo 1: Sorting by time
	print("\n📋 Tasks sorted by time (earliest first):")
	sorted_tasks = scheduler.sort_by_time(all_tasks)
	for task in sorted_tasks:
		print(f"  {task.preferred_time} - {task.title} ({task.pet_name})")
	
	# Demo 2: Filter by pet
	print("\n🐕 Tasks for 'Mochi' only:")
	mochi_tasks = scheduler.filter_by_pet(all_tasks, "Mochi")
	for task in mochi_tasks:
		print(f"  {task.title} at {task.preferred_time}")
	
	# Demo 3: Filter by status
	print("\n✅ Incomplete tasks:")
	incomplete = scheduler.filter_by_status(all_tasks, completed=False)
	for task in incomplete:
		print(f"  {task.title} ({task.pet_name})")


def test_recurring_tasks(owner: Owner) -> None:
	"""Demonstrate automatic recurring task creation."""
	print("\n" + "="*50)
	print("FEATURE 2: RECURRING TASKS")
	print("="*50)
	
	# Get a daily task
	all_tasks = owner.get_all_tasks()
	daily_task = next((t for t in all_tasks if t.frequency == "daily"), None)
	
	if daily_task:
		print(f"\n📅 Original task: {daily_task.title}")
		print(f"   ID: {daily_task.task_id}, Completed: {daily_task.completed}")
		
		# Mark it complete (should create next occurrence)
		new_task = daily_task.mark_completed()
		print(f"   ✓ Marked complete!")
		
		if new_task:
			print(f"\n📅 New task created for next occurrence:")
			print(f"   ID: {new_task.task_id}")
			print(f"   Title: {new_task.title}")
			print(f"   Completed: {new_task.completed}")
			print(f"   (Due tomorrow via timedelta calculation)")
		else:
			print("   No recurring task created.")


def test_conflict_detection(owner: Owner, scheduler: Scheduler) -> None:
	"""Demonstrate conflict detection for overlapping task times."""
	print("\n" + "="*50)
	print("FEATURE 3: CONFLICT DETECTION")
	print("="*50)
	
	# Create a test owner with conflicting tasks
	test_owner = Owner(name="TestUser", time_available_minutes=100)
	dog = Pet(name="Buddy", species="dog", age=3)
	cat = Pet(name="Whiskers", species="cat", age=1)
	
	test_owner.add_pet(dog)
	test_owner.add_pet(cat)
	
	# Add conflicting tasks at same time
	test_owner.add_task_to_pet(
		"Buddy",
		Task(
			task_id="C1",
			title="Dog Training",
			duration_minutes=30,
			priority="high",
			preferred_time="10:00",
		),
	)
	test_owner.add_task_to_pet(
		"Whiskers",
		Task(
			task_id="C2",
			title="Cat Play",
			duration_minutes=20,
			priority="high",
			preferred_time="10:00",
		),
	)
	test_owner.add_task_to_pet(
		"Buddy",
		Task(
			task_id="C3",
			title="Dog Feed",
			duration_minutes=15,
			priority="high",
			preferred_time="10:00",
		),
	)
	
	all_test_tasks = test_owner.get_all_tasks()
	print("\n⏰ Tasks scheduled:")
	for task in all_test_tasks:
		print(f"  {task.preferred_time} - {task.title} ({task.pet_name})")
	
	conflicts = scheduler.detect_conflicts(all_test_tasks)
	if conflicts:
		print("\n🚨 Detected conflicts:")
		for warning in conflicts:
			print(f"  {warning}")
	else:
		print("\n✅ No conflicts detected!")


def main() -> None:
	owner = build_demo_owner()
	scheduler = Scheduler()
	
	# Original schedule
	print_schedule(owner, scheduler)
	
	# New feature demos
	test_sorting_and_filtering(owner, scheduler)
	test_recurring_tasks(owner)
	test_conflict_detection(owner, scheduler)


if __name__ == "__main__":
	main()
