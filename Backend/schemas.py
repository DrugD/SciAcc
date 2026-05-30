"""Pydantic response models for the FastAPI backend."""
from __future__ import annotations
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


DimCode = Literal["D", "M", "E", "V"]
BoundaryPosition = Literal["边界内问题", "边界迁移问题", "边界外问题"]


class PushDimensions(BaseModel):
    primary: list[DimCode]
    secondary: list[DimCode] = Field(default_factory=list)
    summary: str = ""
    multi_dim_link: str = ""


class PaperEntry(BaseModel):
    paper_id: str
    order: int
    year: int
    title: str
    venue: str
    boundary_position: Optional[BoundaryPosition] = None
    pdf_path: Optional[str] = None
    question_path: Optional[str] = None
    work_path: Optional[str] = None
    push_dimensions: Optional[PushDimensions] = None


class PapersIndex(BaseModel):
    schema_version: str = "1.0"
    papers: list[PaperEntry]


class TreeNode(BaseModel):
    label: str
    code: Optional[str] = None
    hint: Optional[str] = None
    year: Optional[int] = None
    papers_introduced: Optional[list[str]] = None
    children: Optional[list["TreeNode"]] = None


TreeNode.model_rebuild()


class BoundaryTree(BaseModel):
    D: TreeNode
    M: TreeNode
    E: TreeNode
    V: TreeNode


class DeltaOp(BaseModel):
    dim: DimCode
    path: list[str]
    item: str
    op: Literal["add", "split", "sibling-of"]
    sibling_of: Optional[str] = None
    papers: list[str] = Field(default_factory=list)


# deltas.json is { "<year>": [DeltaOp, ...] }
class DeltasFile(BaseModel):
    deltas: dict[str, list[DeltaOp]]


class TaskState(BaseModel):
    task_id: str
    paper_id: str
    status: Literal["pending", "extracting", "analyzing", "merging", "done", "failed"]
    step: str = ""
    started_at: str
    updated_at: str
    error: Optional[str] = None
    result: Optional[dict[str, Any]] = None


class UploadResponse(BaseModel):
    task_id: str
    paper_id: str
    status: str = "pending"


class PaperDetail(BaseModel):
    paper_id: str
    title: str
    venue: str
    year: int
    boundary_position: Optional[BoundaryPosition] = None
    push_dimensions: Optional[PushDimensions] = None
    question: dict[str, Any]
    work: dict[str, Any]
