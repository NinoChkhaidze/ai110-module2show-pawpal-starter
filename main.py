from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup: two tasks intentionally share overlapping start times ---
pet = Pet(age=3)
pet.add_task(Task(title="Feeding",      duration_minutes=10, priority="high",   start_time="08:00"))
pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   start_time="08:05"))  # overlaps Feeding
pet.add_task(Task(title="Playtime",     duration_minutes=20, priority="medium", start_time="09:00"))
pet.add_task(Task(title="Grooming",     duration_minutes=40, priority="low",    start_time="09:30"))

owner = Owner(name="Jordan", available_start=480, available_end=600, pet=pet)

# --- Schedule (start_times already set, scheduler won't overwrite them) ---
scheduler = Scheduler(owner)
scheduler.generate_schedule()

print("=" * 50)
print(f"  PawPal+ | Today's Schedule ({date.today()})")
print("=" * 50)
print(scheduler.explain_plan())

# --- Conflict detection ---
print()
warnings = scheduler.detect_conflicts()
if warnings:
    print("⚠ Conflict warnings:")
    for w in warnings:
        print(f"  {w}")
else:
    print("No conflicts detected.")

print("=" * 50)
