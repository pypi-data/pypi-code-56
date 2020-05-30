from typing import Optional

from pydantic.dataclasses import dataclass

from .boolean_annotation import BooleanAnnotation
from .comment_annotation import CommentAnnotation
from .double_annotation import DoubleAnnotation
from .file_annotation import FileAnnotation
from .list_annotation import ListAnnotation
from .long_annotation import LongAnnotation
from .map_annotation import MapAnnotation
from .tag_annotation import TagAnnotation
from .term_annotation import TermAnnotation
from .timestamp_annotation import TimestampAnnotation


@dataclass
class StructuredAnnotations:
    boolean_annotation: Optional[BooleanAnnotation] = None
    comment_annotation: Optional[CommentAnnotation] = None
    double_annotation: Optional[DoubleAnnotation] = None
    file_annotation: Optional[FileAnnotation] = None
    list_annotation: Optional[ListAnnotation] = None
    long_annotation: Optional[LongAnnotation] = None
    map_annotation: Optional[MapAnnotation] = None
    tag_annotation: Optional[TagAnnotation] = None
    term_annotation: Optional[TermAnnotation] = None
    timestamp_annotation: Optional[TimestampAnnotation] = None
    xml_annotation: Optional[str] = None
