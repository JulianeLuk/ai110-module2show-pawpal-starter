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


def main() -> None:
	owner = build_demo_owner()
	scheduler = Scheduler()
	print_schedule(owner, scheduler)


if __name__ == "__main__":
	main()
