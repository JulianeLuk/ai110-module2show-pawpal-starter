classDiagram
    class Owner {
        +String name
        +int time_available_minutes
        +Map preferences
        +List~Pet~ pets
        +add_pet(pet: Pet) void
        +remove_pet(pet_name: String) bool
        +update_preferences(preferences: Map) void
        +get_all_tasks() List~Task~
    }

    class Pet {
        +String name
        +String species
        +int age
        +List~Task~ tasks
        +add_task(task: Task) void
        +edit_task(task_id: String, duration_minutes: int, priority: String) bool
        +remove_task(task_id: String) bool
        +get_tasks() List~Task~
    }

    class Task {
        +String task_id
        +String title
        +int duration_minutes
        +String priority
        +String notes
        +is_valid_priority() bool
        +is_time_fit(available_minutes: int) bool
    }

    class Scheduler {
        +int available_minutes
        +generate_daily_plan(owner: Owner) List~Task~
        +rank_tasks(tasks: List~Task~) List~Task~
        +filter_by_time(tasks: List~Task~, limit_minutes: int) List~Task~
        +explain_plan(selected: List~Task~, skipped: List~Task~) String
    }

    Owner "1" o-- "0..*" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Scheduler ..> Owner : reads owner info
    Scheduler ..> Task : schedules
