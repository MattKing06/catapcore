"""
catapcore Machine Area Module

This module defines a base classes specifying the machine area of an object.

Classes:
    - :class:`~catapcore.common.constants.machine.area.MachineArea`: Machine area name.
"""

from pydantic import BaseModel, ConfigDict

__all__ = ["MachineArea"]


class MachineArea(BaseModel):
    """
    Base class for setting the machine area of an object (see :mod:`~catapcore.common.constants.areas`).
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
    name: str
    """Machine area name"""


def _string_to_machine_area(area: str = None) -> MachineArea:
    """
    Convert string to :class:`~catapcore.common.machine.area.MachineArea` type.

    :param area: Name of area as string
    :type area: str

    :returns: String as :class:`~catapcore.common.machine.area.MachineArea`
    """
    if area is None:
        raise ValueError("Please provide a string to convert to a machine area.")
    if isinstance(area, str):
        return MachineArea(name=area)
    if isinstance(area, MachineArea):
        return area
