from datetime import datetime
from typing import List

from pydantic import BaseModel


class AvailableTimeSlots(BaseModel):
    """
    Example usage:

    ```
        from datetime import datetime

        slots = AvailableTimeSlots.parse_obj(
            [
                datetime(2021, 1, 1, 10, 0),
                datetime(2021, 1, 1, 11, 0),
            ]
        )
    ```
    """

    __root__: List[datetime]
