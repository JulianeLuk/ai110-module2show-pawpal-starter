from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Task:
	task_id: str
	title: str
	duration_minutes: int
	priority: str
	notes: str = ""

	def is_valid_priority(self) -> bool:
		raise NotImplementedError

	def is_time_fit(self, available_minutes: int) -> bool:
		raise NotImplementedError


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		raise NotImplementedError

	def edit_task(self, task_id: str, duration_minutes: int, priority: str) -> bool:
		raise NotImplementedError

	def remove_task(self, task_id: str) -> bool:
		raise NotImplementedError

	def get_tasks(self) -> List[Task]:
		raise NotImplementedError


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
		raise NotImplementedError

	def remove_pet(self, pet_name: str) -> bool:
		raise NotImplementedError

	def update_preferences(self, preferences: Dict[str, Any]) -> None:
		raise NotImplementedError

	def get_all_tasks(self) -> List[Task]:
		raise NotImplementedError


class Scheduler:
	def __init__(self, available_minutes: int) -> None:
		self.available_minutes = available_minutes

	def generate_daily_plan(self, owner: Owner) -> List[Task]:
		raise NotImplementedError

	def rank_tasks(self, tasks: List[Task]) -> List[Task]:
		raise NotImplementedError

	def filter_by_time(self, tasks: List[Task], limit_minutes: int) -> List[Task]:
		raise NotImplementedError

	def explain_plan(self, selected: List[Task], skipped: List[Task]) -> str:
		raise NotImplementedError
