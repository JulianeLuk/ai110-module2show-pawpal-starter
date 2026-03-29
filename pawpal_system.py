from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


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
		return self.priority.strip().lower() in {"low", "medium", "high"}

	def is_time_fit(self, available_minutes: int) -> bool:
		return self.duration_minutes > 0 and available_minutes >= self.duration_minutes

	def mark_completed(self) -> None:
		self.completed = True


@dataclass
class Pet:
	name: str
	species: str
	age: int
	owner_name: str = ""
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
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
		for index, task in enumerate(self.tasks):
			if task.task_id == task_id:
				del self.tasks[index]
				return True
		return False

	def get_tasks(self) -> List[Task]:
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
		for existing_pet in self.pets:
			if existing_pet.name == pet.name:
				return
		pet.owner_name = self.name
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> bool:
		for index, pet in enumerate(self.pets):
			if pet.name == pet_name:
				del self.pets[index]
				return True
		return False

	def update_preferences(self, preferences: Dict[str, Any]) -> None:
		self.preferences.update(preferences)

	def get_all_tasks(self) -> List[Task]:
		all_tasks: List[Task] = []
		for pet in self.pets:
			all_tasks.extend(pet.get_tasks())
		return all_tasks

	def add_task_to_pet(self, pet_name: str, task: Task) -> bool:
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
		if self.available_minutes is None:
			return max(owner.time_available_minutes, 0)
		return max(self.available_minutes, 0)

	def rank_tasks(self, tasks: List[Task]) -> List[Task]:
		priority_rank = {"high": 3, "medium": 2, "low": 1}

		def sort_key(task: Task) -> tuple[int, int, str]:
			priority_score = priority_rank.get(task.priority.strip().lower(), 0)
			return (-priority_score, task.duration_minutes, task.title.lower())

		return sorted(tasks, key=sort_key)

	def filter_by_time(self, tasks: List[Task], limit_minutes: int) -> List[Task]:
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
