# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

## 1. add a pet - the owner registers a pet, its name and what species it is
## 2. add a care task - add a task to a pet, like 
## "feed, 30 minutes, high priority"

## 3. generate today's schedule - the owner sets how many hours they have available, and the code will generate the to do list for the day based on the tasks their priorities and how much time it takes

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Three changes were made after reviewing the initial skeleton:

1. **`available_start` and `available_end` changed from 'str' to 'int' - Originally stored as strings like "08:00", but the Scheduler needs to do arithmetic to get a time budget. Storing them as minutes since midnight makes that it easier.

2. **`Scheduler` gained `scheduled_tasks` and `skipped_tasks` lists** — `explain_plan()` needs to know which tasks were chosen and which were left out


Owner:
attribute: name, available_start, available_end
methods: add_task(), get_all_tasks()

task:
attribute: title, duration, priority, is_complete
method: mark_complete

scheduler:
method: generate_scheduler, explain_reasoning()

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler uses the followingg algorithm: it sorts tasks by priority (in case the priority is the same then sorted by duration) and schedules each one as long as it fits in the remaining time budget

This tradeoff is reasonable for a pet care app because the priority ordering already reflects what matters most to the owner, and the greedy approach is fast, predictable, and easy to explain — the owner can see exactly why each task was included or skipped.

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
