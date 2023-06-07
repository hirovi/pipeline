import typing as t
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class RunState(int, Enum):
    created: int = 0
    routing: int = 1
    resource_accepted: int = 2
    # this includes creating a virtual environment and installing
    # packages
    creating_environment: int = 3
    # starting subrprocess running worker in custom environment
    starting_worker: int = 4
    downloading_graph: int = 5
    caching_graph: int = 6
    running: int = 7
    resource_returning: int = 8
    api_received: int = 9

    in_queue: int = 16
    denied: int = 11
    resource_rejected: int = 14
    resource_died: int = 15
    retrying: int = 13

    completed: int = 10
    failed: int = 12
    rate_limited: int = 17
    lost: int = 18
    no_environment_installed: int = 19

    unknown: int = 20

    @classmethod
    def __get_validators__(cls):
        cls.lookup = {v: k.value for v, k in cls.__members__.items()}
        cls.value_lookup = {k.value: v for v, k in cls.__members__.items()}
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            v = int(v)
        except Exception:
            ...

        if isinstance(v, str):
            return cls.lookup[v]
        elif isinstance(v, int):
            return getattr(cls, cls.value_lookup[v])
        else:
            raise ValueError(f"Invalid value: {v}")


class RunError(Enum):
    input_error = 1
    unroutable = 2
    graph_error = 3
    runtime_error = 4


class RunFileType(Enum):
    input = "input"
    output = "output"


class RunFile(BaseModel):
    id: int
    run_id: int
    io_type: RunFileType
    path: str

    class Config:
        # use_enum_values = True
        orm_mode = True


class Run(BaseModel):
    id: int

    pipeline_id: int
    environment_id: int
    environment_hash: str

    state: RunState
    error: t.Optional[RunError]

    result: t.Optional[t.Any]

    files: t.Optional[t.List[RunFile]]

    created_at: datetime

    class Config:
        # use_enum_values = True
        orm_mode = True


class RunStateTransition(BaseModel):
    run_id: int
    new_state: RunState
    time: datetime