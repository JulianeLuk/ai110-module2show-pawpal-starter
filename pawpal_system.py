from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime, timedelta


@dataclass
class Task:
	task_id: str
	title: str
	duration_minutes: int
	priority: str
	pet_name: str = ""
	frequency: str = "daily"
	preferred_time: str = "any"
	completed: bool = False
	notes: str = ""

	def is_valid_priority(self) -> bool:
		"""Check if priority is one of 'low', 'medium', or 'high'."""
		return self.priority.strip().lower() in {"low", "medium", "high"}

	def is_time_fit(self, available_minutes: int) -> bool:
		"""Verify task duration fits within available time."""
		return self.duration_minutes > 0 and available_minutes >= self.duration_minutes

	def mark_completed(self) -> Task | None:
		"""Mark the task as completed. If recurring, return a new task for next occurrence."""
		self.completed = True
		
		# Handle recurring tasks
		if self.frequency.lower() in {"daily", "weekly"}:
			days_to_add = 1 if self.frequency.lower() == "daily" else 7
			# Parse preferred_time if it's in HH:MM format
			try:
				next_date = datetime.now() + timedelta(days=days_to_add)
				new_task = Task(
					task_id=f"{self.task_id}_next",
					title=self.title,
					duration_minutes=self.duration_minutes,
					priority=self.priority,
					pet_name=self.pet_name,
					frequency=self.frequency,
					preferred_time=self.preferred_time,
					completed=False,
					notes=self.notes,
				)
				return new_task
			except Exception:
				return None
		
		return None


@dataclass
class Pet:
	name: str
	species: str
	age: int
	owner_name: str = ""
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet."""
		task.pet_name = self.name
		self.tasks.append(task)

	def edit_task(
		self,
		task_id: str,
		duration_minutes: int | None = None,
		priority: str | None = None,
		title: str | None = None,
		notes: str | None = None,
	) -> bool:
		"""Edit a task's properties by ID; return True if found and updated."""
		for task in self.tasks:
			if task.task_id != task_id:
				continue

			if duration_minutes is not None:
				if duration_minutes <= 0:
					return False
				task.duration_minutes = duration_minutes

			if priority is not None:
				normalized_priority = priority.strip().lower()
				if normalized_priority not in {"low", "medium", "high"}:
					return False
				task.priority = normalized_priority

			if title is not None:
				task.title = title

			if notes is not None:
				task.notes = notes

			return True

		return False

	def remove_task(self, task_id: str) -> bool:
		"""Remove a task by ID; return True if found and removed."""
		for index, task in enumerate(self.tasks):
			if task.task_id == task_id:
				del self.tasks[index]
				return True
		return False

	def get_tasks(self) -> List[Task]:
		"""Return a copy of the pet's task list."""
		return list(self.tasks)


class Owner:
	def __init__(
		self,
		name: str,
		time_available_minutes: int,
		preferences: Dict[str, Any] | None = None,
		pets: List[Pet] | None = None,
	) -> None:
		self.name = name
		self.time_available_minutes = time_available_minutes
		self.preferences = preferences if preferences is not None else {}
		self.pets = pets if pets is not None else []

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner; skip if pet name already exists."""
		for existing_pet in self.pets:
			if existing_pet.name == pet.name:
				return
		pet.owner_name = self.name
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> bool:
		"""Remove a pet by name; return True if found and removed."""
		for index, pet in enumerate(self.pets):
			if pet.name == pet_name:
				del self.pets[index]
				return True
		return False

	def update_preferences(self, preferences: Dict[str, Any]) -> None:
		"""Merge new preferences into existing preferences."""
		self.preferences.update(preferences)

	def get_all_tasks(self) -> List[Task]:
		"""Aggregate and return all tasks across all owner's pets."""
		all_tasks: List[Task] = []
		for pet in self.pets:
			all_tasks.extend(pet.get_tasks())
		return all_tasks

	def add_task_to_pet(self, pet_name: str, task: Task) -> bool:
		"""Find a pet by name and add a task to it; return True if pet found."""
		for pet in self.pets:
			if pet.name == pet_name:
				pet.add_task(task)
				return True
		return False

	def edit_pet_task(
		self,
		pet_name: str,
		task_id: str,
		duration_minutes: int | None = None,
		priority: str | None = None,
		title: str | None = None,
		notes: str | None = None,
	) -> bool:
		"""Find a pet by name and edit a task within it; return True if found and edited."""
		for pet in self.pets:
			if pet.name == pet_name:
				return pet.edit_task(
					task_id=task_id,
					duration_minutes=duration_minutes,
					priority=priority,
					title=title,
					notes=notes,
				)
		return False


class Scheduler:
	def __init__(self, available_minutes: int | None = None) -> None:
		self.available_minutes = available_minutes
		self.last_selected: List[Task] = []
		self.last_skipped: List[Task] = []
		self.last_explanation: str = ""

	def generate_daily_plan(self, owner: Owner) -> List[Task]:
		"""Generate and return a daily schedule of selected tasks for the owner."""
		limit_minutes = self.resolve_time_limit(owner)
		all_tasks = owner.get_all_tasks()
		candidate_tasks = [task for task in all_tasks if not task.completed]
		ranked_tasks = self.rank_tasks(candidate_tasks)
		selected_tasks = self.filter_by_time(ranked_tasks, limit_minutes)

		selected_ids = {id(task) for task in selected_tasks}
		skipped_tasks = [task for task in ranked_tasks if id(task) not in selected_ids]

		self.last_selected = selected_tasks
		self.last_skipped = skipped_tasks
		self.last_explanation = self.explain_plan(selected_tasks, skipped_tasks)

		return selected_tasks

	def resolve_time_limit(self, owner: Owner) -> int:
		"""Return the effective time limit: scheduler override or owner's available time."""
		if self.available_minutes is None:
			return max(owner.time_available_minutes, 0)
		return max(self.available_minutes, 0)

	def rank_tasks(self, tasks: List[Task]) -> List[Task]:
		"""Sort tasks by priority (high→low), then duration, then title."""
		priority_rank = {"high": 3, "medium": 2, "low": 1}

		def sort_key(task: Task) -> tuple[int, int, str]:
			priority_score = priority_rank.get(task.priority.strip().lower(), 0)
			return (-priority_score, task.duration_minutes, task.title.lower())

		return sorted(tasks, key=sort_key)

	def filter_by_time(self, tasks: List[Task], limit_minutes: int) -> List[Task]:
		"""Greedily select tasks that fit within the time limit."""
		selected: List[Task] = []
		minutes_used = 0
		for task in tasks:
			if task.duration_minutes <= 0:
				continue
			if minutes_used + task.duration_minutes <= limit_minutes:
				selected.append(task)
				minutes_used += task.duration_minutes
		return selected

	def explain_plan(self, selected: List[Task], skipped: List[Task]) -> str:
		"""Generate a human-readable explanation of the selected and skipped tasks."""
		selected_minutes = sum(task.duration_minutes for task in selected)
		limit_text = (
			f"time limit {self.available_minutes} minutes"
			if self.available_minutes is not None
			else "owner-defined time limit"
		)

		lines = [
			f"Selected {len(selected)} task(s) totaling {selected_minutes} minutes based on priority and {limit_text}.",
		]

		if selected:
			selected_titles = ", ".join(task.title for task in selected)
			lines.append(f"Included: {selected_titles}.")

		if skipped:
			skipped_titles = ", ".join(task.title for task in skipped)
			lines.append(f"Skipped due to time limit: {skipped_titles}.")
		else:
			lines.append("No tasks were skipped.")

		return " ".join(lines)

	def sort_by_time(self, tasks: List[Task]) -> List[Task]:
		"""Sort tasks by their preferred_time in HH:MM format (earliest first)."""
		def parse_time(task: Task) -> str:
			if task.preferred_time == "any" or not task.preferred_time:
				return "23:59"  # "any" times go to end
			try:
				datetime.strptime(task.preferred_time, "%H:%M")
				return task.preferred_time
			except ValueError:
				return "23:59"
		
		return sorted(tasks, key=parse_time)

	def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
		"""Filter tasks by pet name."""
		return [task for task in tasks if task.pet_name.lower() == pet_name.lower()]

	def filter_by_status(self, tasks: List[Task], completed: bool = False) -> List[Task]:
		"""Filter tasks by completion status."""
		return [task for task in tasks if task.completed == completed]

	def detect_conflicts(self, tasks: List[Task]) -> List[str]:
		"""Detect if multiple tasks are scheduled at the same time. Returns list of warning messages."""
		warnings: List[str] = []
		time_groups: Dict[str, List[Task]] = {}
		
		for task in tasks:
			if task.preferred_time == "any" or not task.preferred_time:
				continue
			
			if task.preferred_time not in time_groups:
				time_groups[task.preferred_time] = []
			time_groups[task.preferred_time].append(task)
		
		# Find conflicts
		for time_slot, conflicting_tasks in time_groups.items():
			if len(conflicting_tasks) > 1:
				task_names = ", ".join(
					f"{t.title} ({t.pet_name})" for t in conflicting_tasks
				)
				warnings.append(
					f"⚠️  CONFLICT at {time_slot}: {task_names}"
				)
		
		return warnings
