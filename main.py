
from fastapi import FastAPI, HTTPException, status
from schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(
    title="TaskFlow API",
    description="A task management REST API",
    version="1.0.0"
)

tasks: list[TaskResponse] = []
next_id = 1


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def home():
    return {"message": "Welcome to TaskFlow API"}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):
    global next_id

    if not task.title.strip():
        raise HTTPException(
            status_code=422,
            detail="Task title cannot be blank"
        )

    new_task = TaskResponse(
        id=next_id,
        **task.model_dump()
    )

    tasks.append(new_task)
    next_id += 1

    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update: TaskUpdate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            changes = update.model_dump(exclude_unset=True)

            if "title" in changes:
                if changes["title"] is None or not changes["title"].strip():
                    raise HTTPException(
                        status_code=422,
                        detail="Task title cannot be blank"
                    )

            if "completed" in changes and changes["completed"] is None:
                raise HTTPException(
                    status_code=422,
                    detail="Completed must be true or false"
                )

            updated_task = task.model_copy(update=changes)

            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
