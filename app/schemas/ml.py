from typing import Any, List, Tuple

from pydantic import BaseModel, confloat

# Request


# Response
class Layer(BaseModel):
    name: str
    class_name: str
    params: int
    output_shape: Tuple[Any, ...]


class ModelPrediction(BaseModel):
    class_name: str
    confidence: confloat(ge=0, le=1.0)


class ModelSummaryResponse(BaseModel):
    name: str
    total_params: int
    trainable_params: int
    non_trainable_params: int
    layers: List[Layer]
