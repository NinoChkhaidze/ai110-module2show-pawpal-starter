from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
pet = Pet(age=3)
pet.add_task(Task(title="Morning walk",    duration_minutes=30, priority="high"))
pet.add_task(Task(title="Feeding",         duration_minutes=10, priority="high"))
pet.add_task(Task(title="Playtime",        duration_minutes=20, priority="medium"))
pet.add_task(Task(title="Grooming",        duration_minutes=40, priority="low"))
pet.add_task(Task(title="Vet check-in",   duration_minutes=60, priority="medium"))

# Owner available 8:00 AM (480) to 9:30 AM (570) — 90 min budget to show skipping
owner = Owner(name="Jordan", available_start=480, available_end=570, pet=pet)

# --- Schedule ---
scheduler = Scheduler(owner)
scheduler.generate_schedule()

# --- Output ---
print("=" * 40)
print(f"  PawPal+ | Today's Schedule for {owner.name}")
print("=" * 40)
print(scheduler.explain_plan())
print("=" * 40)
