import pytest

from pawpal_system import Pet, Task


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
