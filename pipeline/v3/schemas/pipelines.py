import typing as t
from datetime import datetime

from pipeline.v3.schemas import BaseModel


class PipelineGet(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime

    path: str
    minimum_cache_number: t.Optional[int]
    gpu_memory_min: t.Optional[int]
    environment_id: str


class PipelinePatch(BaseModel):
    minimum_cache_number: t.Optional[int]
    gpu_memory_min: t.Optional[int]
