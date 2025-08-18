from typing import Dict, Any, Optional
from uuid import uuid4
from threading import Lock

class TaskManager:
  def __init__(self):
    self.tasks: Dict[str, Dict[str, Any]] = {}
    self.lock = Lock()

  def create(self) -> str:
    """Create a new task with optional step names."""
    task_id = str(uuid4())
    
    with self.lock:
      self.tasks[task_id] = {
        "status": "pending", # pending, running, running:STEP, done, error, cancelled
        "current_step": None,
        "progress": 0.0,
        "cancelled": False,
        "result": None,
        "error": None,
      }

    return task_id

  def start(self, task_id: str):
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["status"] = "running"

  def start_step(self, task_id: str, step_name: str):
    """Mark a step as running."""
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["current_step"] = step_name
        self.tasks[task_id]["status"] = f"running:{step_name}"
        self.tasks[task_id]["progress"] = 0.0

  def update_progress(self, task_id: str, progress: float):
    """Update task progress (0.0 - 1.0) for current step."""
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["progress"] = min(max(progress, 0.0), 1.0)

  def complete_step(self, task_id: str):
    """Mark the current step as completed."""
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["progress"] = 1.0
        self.tasks[task_id]["current_step"] = None

  def update_result(self, task_id: str, result: Any):
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["result"] = result
        self.tasks[task_id]["status"] = "done"

  def update_error(self, task_id: str, error: str):
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["error"] = error
        self.tasks[task_id]["status"] = "error"

  def cancel(self, task_id: str) -> bool:
    with self.lock:
      if task_id in self.tasks:
        self.tasks[task_id]["cancelled"] = True
        self.tasks[task_id]["status"] = "cancelled"

        return True

    return False

  def is_cancelled(self, task_id: str) -> bool:
    with self.lock:
      return self.tasks.get(task_id, {}).get("cancelled", False)

  def get(self, task_id: str) -> Optional[Dict[str, Any]]:
    with self.lock:
      return self.tasks.get(task_id)

  def delete(self, task_id: str):
    with self.lock:
      if task_id in self.tasks:
        del self.tasks[task_id]
