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

The scheduler considers task priority (high/medium/low) and the owner's available time window. Priority came first because a pet care app needs to guarantee the most important tasks always get scheduled before lower-priority ones like grooming. Time budget came second to handle real-world limits — not every task fits in a day.

**b. Tradeoffs**

The scheduler uses the followingg algorithm: it sorts tasks by priority (in case the priority is the same then sorted by duration) and schedules each one as long as it fits in the remaining time budget

This tradeoff is reasonable for a pet care app because the priority ordering already reflects what matters most to the owner, and the greedy approach is fast, predictable, and easy to explain — the owner can see exactly why each task was included or skipped.

---

## 3. AI Collaboration

**a. How you used AI**

Claude gave suggestions based on my actual code. I used it to spot missing methods, draft test cases, and understand unfamiliar code like `itertools.combinations` before adding it. 

**b. Judgment and verification**

Copilot suggested storing available hours as strings like `"08:00"`. I didn't go with that because the scheduler needs to do arithmetic - adding durations, checking time budgets - and strings would make that messy.

**c. Separate chat sessions per phase**

Starting a new chat for each phase kept things focused. 

---

## 4. Testing and Verification

**a. What you tested**

I tested sorting, recurrence, and conflict detection (overlapping tasks get flagged, sequential ones don't). These mattered most because they're the three behaviors the owner actually relies on.
**b. Confidence**

4 out of 5. The core logic is covered and I trust it works as designed. 
---

## 5. Reflection

**a. What went well**

The conflict detection came together cleanly. Using `itertools.combinations` to check every pair of tasks was simple and easy to test — I was happy with how little code it took to do something that feels complex.

**b. What you would improve**

I'd redesign the UI to let owners mark tasks complete directly in the app.

**c. Key takeaway**

AI is most useful when you give it something concrete and direct to react to. I learned to ask specific questions like "what's missing from this class?".
