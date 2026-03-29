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
		raise NotImplementedError

	def is_time_fit(self, available_minutes: int) -> bool:
		raise NotImplementedError

	def mark_completed(self) -> None:
		raise NotImplementedError


@dataclass
class Pet:
	name: str
	species: str
	age: int
	owner_name: str = ""
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		raise NotImplementedError

	def edit_task(
		self,
		task_id: str,
		duration_minutes: int | None = None,
		priority: str | None = None,
		title: str | None = None,
		notes: str | None = None,
	) -> bool:
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

	def add_task_to_pet(self, pet_name: str, task: Task) -> bool:
		raise NotImplementedError

	def edit_pet_task(
		self,
		pet_name: str,
		task_id: str,
		duration_minutes: int | None = None,
		priority: str | None = None,
		title: str | None = None,
		notes: str | None = None,
	) -> bool:
		raise NotImplementedError


class Scheduler:
	def __init__(self, available_minutes: int | None = None) -> None:
		self.available_minutes = available_minutes
		self.last_selected: List[Task] = []
		self.last_skipped: List[Task] = []
		self.last_explanation: str = ""

	def generate_daily_plan(self, owner: Owner) -> List[Task]:
		raise NotImplementedError

	def resolve_time_limit(self, owner: Owner) -> int:
		raise NotImplementedError

	def rank_tasks(self, tasks: List[Task]) -> List[Task]:
		raise NotImplementedError

	def filter_by_time(self, tasks: List[Task], limit_minutes: int) -> List[Task]:
		raise NotImplementedError

	def explain_plan(self, selected: List[Task], skipped: List[Task]) -> str:
		raise NotImplementedError
