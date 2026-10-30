
from fastapi import FastAPI, HTTPException, status
from schemas import TaskCreate, TaskResponse

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