# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The purpose of the Pawpal application is to help with pet care management. This application assists the user with scheduling all necessary care items for their pets, including medications, grooming, feeding, and more. The app should produce a daily plan that clearly lists what needs to be done that day with priorities, while also allowing the user to add, edit, or remove tasks. Overall, the application is designed to make managing multiple pets easier and less stressful by keeping everything organized in one place.

- What classes did you include, and what responsibilities did you assign to each?

The UML diagram includes four main classes: Owner, Pet, Task, and Scheduler. The Owner class manages the user’s information, preferences, and the list of pets, and it provides methods to add or remove pets as well as retrieve all tasks across pets. The Pet class stores information about each pet, including their name, species, age, and list of tasks, and it handles adding, editing, removing, and retrieving tasks. The Task class represents an individual task with attributes like title, duration, priority, and notes, and it includes methods to validate priority and check if the task fits within available time. The Scheduler class is responsible for generating a daily plan based on the owner’s available time, ranking tasks by priority, filtering tasks that fit within the time limit, and explaining the daily plan including tasks that were skipped.

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
One major change I made was adding the completed attribute and the mark_completed() method to the Task class. I did this so each task can track whether it’s done, which makes it easier for the Scheduler to generate an accurate daily plan and for the owner to see what still needs attention without manually checking each task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler considers several constraints when generating a daily plan. First, it looks at the owner’s available time as a hard limit so tasks don’t exceed what can realistically be done in a day. It also takes into account task priority (high, medium, low), task duration, and completion status, only scheduling tasks that haven’t been marked completed. Each task is associated with a specific pet, so the plan clearly organizes care by pet. I also include preferred times as hints for when a task should ideally happen, and frequency to handle one-time versus recurring tasks. I decided these constraints mattered most because they directly affect whether the plan is practical and helpful because owners need to know what must be done, when, and for which pet, without overbooking their day.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff my scheduler makes is that it uses a greedy approach, picking the highest-priority tasks that fit one at a time until time runs out. That means sometimes a longer high-priority task might get skipped so I can fit in a couple of shorter ones instead. I think this tradeoff makes sense because it keeps the plan simple and easy to follow, makes sure essential care like feeding or meds comes first, and stops the owner from overcommitting. For daily planning, it’s better to have a schedule you can actually finish than trying to squeeze everything in perfectly.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
