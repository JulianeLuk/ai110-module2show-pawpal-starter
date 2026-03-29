import pytest

from pawpal_system import Pet, Task, Owner, Scheduler


class TestTaskCompletion:
	"""Test Task completion behavior."""

	def test_mark_completed_changes_status(self) -> None:
		"""Verify that calling mark_completed() changes task.completed from False to True."""
		task = Task(
			task_id="T1",
			title="Morning Walk",
			duration_minutes=30,
			priority="high",
		)

		assert task.completed is False, "Task should start as incomplete"

		task.mark_completed()

		assert task.completed is True, "Task should be marked as completed after mark_completed()"


class TestTaskAddition:
	"""Test adding tasks to pets."""

	def test_add_task_to_pet_increases_count(self) -> None:
		"""Verify that adding a task to a Pet increases that pet's task count."""
		pet = Pet(name="Mochi", species="dog", age=4)

		assert len(pet.tasks) == 0, "Pet should start with no tasks"

		task = Task(
			task_id="T1",
			title="Evening Feed",
			duration_minutes=15,
			priority="high",
		)
		pet.add_task(task)

		assert len(pet.tasks) == 1, "Pet should have 1 task after adding one"

		task2 = Task(
			task_id="T2",
			title="Play Session",
			duration_minutes=20,
			priority="medium",
		)
		pet.add_task(task2)

		assert len(pet.tasks) == 2, "Pet should have 2 tasks after adding two"


class TestSortingByTime:
	"""Test sorting tasks by preferred_time in HH:MM format."""

	def test_sort_by_time_chronological_order(self) -> None:
		"""Verify that sort_by_time() returns tasks in earliest-to-latest order."""
		scheduler = Scheduler()
		
		task_afternoon = Task(
			task_id="T1",
			title="Play Session",
			duration_minutes=20,
			priority="medium",
			preferred_time="14:00",
		)
		task_morning = Task(
			task_id="T2",
			title="Morning Walk",
			duration_minutes=30,
			priority="high",
			preferred_time="08:00",
		)
		task_evening = Task(
			task_id="T3",
			title="Evening Feed",
			duration_minutes=15,
			priority="high",
			preferred_time="18:30",
		)
		
		tasks = [task_afternoon, task_morning, task_evening]
		sorted_tasks = scheduler.sort_by_time(tasks)
		
		assert sorted_tasks[0].preferred_time == "08:00", "First task should be at 08:00"
		assert sorted_tasks[1].preferred_time == "14:00", "Second task should be at 14:00"
		assert sorted_tasks[2].preferred_time == "18:30", "Third task should be at 18:30"

	def test_sort_by_time_with_flexible_times(self) -> None:
		"""Verify that 'any' time tasks are placed at the end."""
		scheduler = Scheduler()
		
		task_fixed = Task(
			task_id="T1",
			title="Feed",
			duration_minutes=15,
			priority="high",
			preferred_time="09:00",
		)
		task_flexible = Task(
			task_id="T2",
			title="Play",
			duration_minutes=20,
			priority="low",
			preferred_time="any",
		)
		
		tasks = [task_flexible, task_fixed]
		sorted_tasks = scheduler.sort_by_time(tasks)
		
		assert sorted_tasks[0].preferred_time == "09:00", "Fixed time should come first"
		assert sorted_tasks[1].preferred_time == "any", "Flexible time should come last"

	def test_sort_by_time_empty_list(self) -> None:
		"""Verify that sort_by_time() handles empty task list gracefully."""
		scheduler = Scheduler()
		sorted_tasks = scheduler.sort_by_time([])
		
		assert sorted_tasks == [], "Empty list should return empty list"


class TestRecurringTasks:
	"""Test automatic recurring task creation."""

	def test_mark_completed_daily_creates_next_occurrence(self) -> None:
		"""Verify that marking a daily task complete creates a new task for tomorrow."""
		task = Task(
			task_id="T1",
			title="Morning Feed",
			duration_minutes=15,
			priority="high",
			frequency="daily",
			preferred_time="08:00",
		)
		
		new_task = task.mark_completed()
		
		assert task.completed is True, "Original task should be marked complete"
		assert new_task is not None, "Daily task should return a new task"
		assert new_task.task_id == "T1_next", "New task ID should be '_next' version"
		assert new_task.title == "Morning Feed", "New task should have same title"
		assert new_task.frequency == "daily", "New task should have same frequency"
		assert new_task.completed is False, "New task should start as incomplete"

	def test_mark_completed_weekly_creates_next_occurrence(self) -> None:
		"""Verify that marking a weekly task complete creates a new task for next week."""
		task = Task(
			task_id="T5",
			title="Grooming",
			duration_minutes=40,
			priority="low",
			frequency="weekly",
			preferred_time="20:00",
		)
		
		new_task = task.mark_completed()
		
		assert new_task is not None, "Weekly task should return a new task"
		assert new_task.frequency == "weekly", "New task should have same frequency"
		assert new_task.completed is False, "New task should start as incomplete"

	def test_mark_completed_one_time_no_recurrence(self) -> None:
		"""Verify that one-time tasks don't create new occurrences."""
		task = Task(
			task_id="T3",
			title="Vet Appointment",
			duration_minutes=60,
			priority="high",
			frequency="once",
		)
		
		new_task = task.mark_completed()
		
		assert new_task is None, "One-time tasks should not create new occurrence"
		assert task.completed is True, "Task should be marked complete"


class TestConflictDetection:
	"""Test scheduling conflict detection."""

	def test_detect_conflicts_same_time(self) -> None:
		"""Verify that detect_conflicts() identifies tasks at the same time."""
		scheduler = Scheduler()
		
		task1 = Task(
			task_id="T1",
			title="Dog Training",
			duration_minutes=30,
			priority="high",
			pet_name="Buddy",
			preferred_time="10:00",
		)
		task2 = Task(
			task_id="T2",
			title="Cat Play",
			duration_minutes=20,
			priority="high",
			pet_name="Whiskers",
			preferred_time="10:00",
		)
		
		conflicts = scheduler.detect_conflicts([task1, task2])
		
		assert len(conflicts) == 1, "Should detect one conflict"
		assert "10:00" in conflicts[0], "Conflict message should mention time"
		assert "Dog Training" in conflicts[0], "Conflict message should mention first task"
		assert "Cat Play" in conflicts[0], "Conflict message should mention second task"

	def test_detect_conflicts_three_tasks_same_time(self) -> None:
		"""Verify that detect_conflicts() handles three tasks at same time."""
		scheduler = Scheduler()
		
		tasks = [
			Task(
				task_id="T1",
				title="Task A",
				duration_minutes=20,
				priority="high",
				pet_name="Pet1",
				preferred_time="15:00",
			),
			Task(
				task_id="T2",
				title="Task B",
				duration_minutes=20,
				priority="high",
				pet_name="Pet2",
				preferred_time="15:00",
			),
			Task(
				task_id="T3",
				title="Task C",
				duration_minutes=20,
				priority="high",
				pet_name="Pet3",
				preferred_time="15:00",
			),
		]
		
		conflicts = scheduler.detect_conflicts(tasks)
		
		assert len(conflicts) == 1, "Should detect one conflict slot with three tasks"
		assert conflicts[0].count(",") >= 2, "Conflict message should list all three tasks"

	def test_detect_conflicts_no_conflict(self) -> None:
		"""Verify that detect_conflicts() returns empty when no conflicts exist."""
		scheduler = Scheduler()
		
		task1 = Task(
			task_id="T1",
			title="Morning",
			duration_minutes=30,
			priority="high",
			preferred_time="08:00",
		)
		task2 = Task(
			task_id="T2",
			title="Afternoon",
			duration_minutes=20,
			priority="medium",
			preferred_time="14:00",
		)
		
		conflicts = scheduler.detect_conflicts([task1, task2])
		
		assert conflicts == [], "Should return empty list when no conflicts"

	def test_detect_conflicts_ignores_flexible_times(self) -> None:
		"""Verify that tasks with 'any' time are ignored by conflict detection."""
		scheduler = Scheduler()
		
		task1 = Task(
			task_id="T1",
			title="Fixed Time",
			duration_minutes=30,
			priority="high",
			preferred_time="10:00",
		)
		task2 = Task(
			task_id="T2",
			title="Flexible Time",
			duration_minutes=20,
			priority="medium",
			preferred_time="any",
		)
		
		conflicts = scheduler.detect_conflicts([task1, task2])
		
		assert conflicts == [], "Tasks with 'any' time should not trigger conflicts"

	def test_detect_conflicts_empty_list(self) -> None:
		"""Verify that empty task list returns no conflicts."""
		scheduler = Scheduler()
		conflicts = scheduler.detect_conflicts([])
		
		assert conflicts == [], "Empty list should return no conflicts"


class TestFilteringByPet:
	"""Test filtering tasks by pet name."""

	def test_filter_by_pet_returns_correct_tasks(self) -> None:
		"""Verify that filter_by_pet() returns only tasks for specified pet."""
		scheduler = Scheduler()
		
		mochi_task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			pet_name="Mochi",
		)
		luna_task = Task(
			task_id="T2",
			title="Play",
			duration_minutes=20,
			priority="medium",
			pet_name="Luna",
		)
		
		tasks = [mochi_task, luna_task]
		mochi_filtered = scheduler.filter_by_pet(tasks, "Mochi")
		
		assert len(mochi_filtered) == 1, "Should return 1 task for Mochi"
		assert mochi_filtered[0].pet_name == "Mochi", "Returned task should be for Mochi"

	def test_filter_by_pet_case_insensitive(self) -> None:
		"""Verify that filter_by_pet() is case-insensitive."""
		scheduler = Scheduler()
		
		task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			pet_name="Mochi",
		)
		
		filtered = scheduler.filter_by_pet([task], "mochi")
		
		assert len(filtered) == 1, "Should find task with lowercase pet name"

	def test_filter_by_pet_no_tasks(self) -> None:
		"""Verify that filter_by_pet() returns empty list when pet has no tasks."""
		scheduler = Scheduler()
		
		task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			pet_name="Mochi",
		)
		
		filtered = scheduler.filter_by_pet([task], "Luna")
		
		assert filtered == [], "Should return empty list for non-existent pet"


class TestFilteringByStatus:
	"""Test filtering tasks by completion status."""

	def test_filter_by_status_incomplete(self) -> None:
		"""Verify that filter_by_status(completed=False) returns only incomplete tasks."""
		scheduler = Scheduler()
		
		incomplete_task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			completed=False,
		)
		complete_task = Task(
			task_id="T2",
			title="Feed",
			duration_minutes=15,
			priority="high",
			completed=True,
		)
		
		filtered = scheduler.filter_by_status([incomplete_task, complete_task], completed=False)
		
		assert len(filtered) == 1, "Should return 1 incomplete task"
		assert filtered[0].task_id == "T1", "Should return the incomplete task"

	def test_filter_by_status_complete(self) -> None:
		"""Verify that filter_by_status(completed=True) returns only complete tasks."""
		scheduler = Scheduler()
		
		incomplete_task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			completed=False,
		)
		complete_task = Task(
			task_id="T2",
			title="Feed",
			duration_minutes=15,
			priority="high",
			completed=True,
		)
		
		filtered = scheduler.filter_by_status([incomplete_task, complete_task], completed=True)
		
		assert len(filtered) == 1, "Should return 1 complete task"
		assert filtered[0].task_id == "T2", "Should return the completed task"

	def test_filter_by_status_empty_result(self) -> None:
		"""Verify that filter_by_status() returns empty when no matches found."""
		scheduler = Scheduler()
		
		task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			completed=False,
		)
		
		filtered = scheduler.filter_by_status([task], completed=True)
		
		assert filtered == [], "Should return empty list when no complete tasks"


class TestPriorityRanking:
	"""Test task ranking by priority."""

	def test_rank_tasks_by_priority(self) -> None:
		"""Verify that rank_tasks() prioritizes high > medium > low."""
		scheduler = Scheduler()
		
		low_task = Task(
			task_id="T1",
			title="Lazy",
			duration_minutes=10,
			priority="low",
		)
		high_task = Task(
			task_id="T2",
			title="Urgent",
			duration_minutes=20,
			priority="high",
		)
		medium_task = Task(
			task_id="T3",
			title="Normal",
			duration_minutes=15,
			priority="medium",
		)
		
		ranked = scheduler.rank_tasks([low_task, high_task, medium_task])
		
		assert ranked[0].priority == "high", "High priority should be first"
		assert ranked[1].priority == "medium", "Medium priority should be second"
		assert ranked[2].priority == "low", "Low priority should be last"

	def test_rank_tasks_same_priority_by_duration(self) -> None:
		"""Verify that tasks with same priority are ranked by duration (shorter first)."""
		scheduler = Scheduler()
		
		long_task = Task(
			task_id="T1",
			title="Long",
			duration_minutes=30,
			priority="high",
		)
		short_task = Task(
			task_id="T2",
			title="Short",
			duration_minutes=10,
			priority="high",
		)
		
		ranked = scheduler.rank_tasks([long_task, short_task])
		
		assert ranked[0].duration_minutes == 10, "Shorter task should rank first"
		assert ranked[1].duration_minutes == 30, "Longer task should rank second"


class TestDailyPlanGeneration:
	"""Test full daily schedule generation."""

	def test_generate_daily_plan_respects_time_limit(self) -> None:
		"""Verify that generate_daily_plan() respects the owner's available time."""
		owner = Owner(name="Jordan", time_available_minutes=50)
		
		dog = Pet(name="Mochi", species="dog", age=4)
		owner.add_pet(dog)
		
		# Add tasks totaling 70 minutes
		owner.add_task_to_pet(
			"Mochi",
			Task(
				task_id="T1",
				title="Walk",
				duration_minutes=30,
				priority="high",
			),
		)
		owner.add_task_to_pet(
			"Mochi",
			Task(
				task_id="T2",
				title="Play",
				duration_minutes=20,
				priority="medium",
			),
		)
		owner.add_task_to_pet(
			"Mochi",
			Task(
				task_id="T3",
				title="Training",
				duration_minutes=20,
				priority="low",
			),
		)
		
		scheduler = Scheduler()
		plan = scheduler.generate_daily_plan(owner)
		
		total_minutes = sum(task.duration_minutes for task in plan)
		assert total_minutes <= 50, "Plan should fit within 50-minute limit"

	def test_generate_daily_plan_empty_owner(self) -> None:
		"""Verify that plan for owner with no tasks returns empty list."""
		owner = Owner(name="Jane", time_available_minutes=60)
		scheduler = Scheduler()
		
		plan = scheduler.generate_daily_plan(owner)
		
		assert plan == [], "Owner with no pets should have empty plan"

	def test_generate_daily_plan_excludes_completed_tasks(self) -> None:
		"""Verify that completed tasks are excluded from the plan."""
		owner = Owner(name="Jordan", time_available_minutes=100)
		dog = Pet(name="Mochi", species="dog", age=4)
		owner.add_pet(dog)
		
		completed_task = Task(
			task_id="T1",
			title="Done",
			duration_minutes=20,
			priority="high",
			completed=True,
		)
		incomplete_task = Task(
			task_id="T2",
			title="Todo",
			duration_minutes=20,
			priority="high",
			completed=False,
		)
		
		owner.add_task_to_pet("Mochi", completed_task)
		owner.add_task_to_pet("Mochi", incomplete_task)
		
		scheduler = Scheduler()
		plan = scheduler.generate_daily_plan(owner)
		
		assert len(plan) == 1, "Plan should only include incomplete tasks"
		assert plan[0].task_id == "T2", "Plan should include the incomplete task"


class TestEdgeCases:
	"""Test edge cases and error handling."""

	def test_invalid_time_format_handled(self) -> None:
		"""Verify that invalid time formats are handled gracefully."""
		scheduler = Scheduler()
		
		task = Task(
			task_id="T1",
			title="Walk",
			duration_minutes=30,
			priority="high",
			preferred_time="25:99",  # Invalid time
		)
		
		sorted_tasks = scheduler.sort_by_time([task])
		
		# Should not crash, and task should be treated as late time
		assert len(sorted_tasks) == 1, "Should handle invalid time gracefully"

	def test_task_with_zero_duration_skipped(self) -> None:
		"""Verify that tasks with zero or negative duration are skipped."""
		scheduler = Scheduler()
		
		valid_task = Task(
			task_id="T1",
			title="Valid",
			duration_minutes=20,
			priority="high",
		)
		invalid_task = Task(
			task_id="T2",
			title="Invalid",
			duration_minutes=0,
			priority="high",
		)
		
		selected = scheduler.filter_by_time([valid_task, invalid_task], 30)
		
		assert len(selected) == 1, "Zero-duration task should be skipped"
		assert selected[0].task_id == "T1", "Valid task should be selected"

	def test_large_task_list_performance(self) -> None:
		"""Verify that scheduler handles large task lists."""
		scheduler = Scheduler()
		
		# Create 100 tasks
		tasks = [
			Task(
				task_id=f"T{i}",
				title=f"Task {i}",
				duration_minutes=10,
				priority="high" if i % 2 == 0 else "low",
				preferred_time=f"{8 + (i % 12):02d}:00",
			)
			for i in range(100)
		]
		
		# Should complete without error
		sorted_tasks = scheduler.sort_by_time(tasks)
		filtered = scheduler.filter_by_pet(tasks, "Mochi")
		conflicts = scheduler.detect_conflicts(tasks)
		
		assert len(sorted_tasks) == 100, "Should handle all tasks"
		assert isinstance(filtered, list), "Should return list"
		assert isinstance(conflicts, list), "Should return warnings list"
