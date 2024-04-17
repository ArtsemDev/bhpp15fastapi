from typing import Annotated

from fastapi import Path

CategoryID = Annotated[
    int,
    Path(
        alias="id",
        title="Category ID",
        description="Category unique identifier",
        examples=[42]
    )
]
