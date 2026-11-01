
from fastapi import FastAPI, HTTPException, status
from schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(
    title="TaskFlow API",
    description="A task management REST API",
    version="1.0.0"
)

tasks: dict[int, TaskResponse] = {}
next_id = 1


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def home():
    return {"message": "Welcome to TaskFlow API"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    global next_id

    if not task.title.strip():
        raise HTTPException(status_code=422, detail="Title cannot be blank")

    new_task = TaskResponse(
        id=next_id,
        **task.model_dump()
    )

    tasks[next_id] = new_task
    next_id += 1

    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    changes = update.model_dump(exclude_unset=True)

    if "title" in changes:
        if changes["title"] is None or not changes["title"].strip():
            raise HTTPException(status_code=422, detail="Title cannot be blank")

    if "completed" in changes and changes["completed"] is None:
        raise HTTPException(status_code=422, detail="Completed must be a boolean")

    tasks[task_id] = tasks[task_id].model_copy(update=changes)

    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[task_id]
