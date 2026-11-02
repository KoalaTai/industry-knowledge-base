"""World / Build registry used by the generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List

from .voxel import Voxel

Builder = Callable[[Voxel], None]


@dataclass
class Build:
    id: str                    # function path segment, e.g. "giza"
    name: str                  # display name
    description: str           # one or two sentences shown in chat
    builder: Builder           # fills a fresh Voxel with ground at y=0
    scale: str = ""            # e.g. "1 block = 2.5 m"


@dataclass
class World:
    id: str                    # namespace folder, e.g. "egypt"
    name: str                  # "Ptolemaic Egypt"
    game: str                  # "Assassin's Creed Origins (2017)"
    era: str                   # "49-43 BCE"
    description: str
    builds: List[Build] = field(default_factory=list)
    franchise: str = "Assassin's Creed"

    def build(self, b: Build) -> "World":
        self.builds.append(b)
        return self


def all_worlds() -> List[World]:
    """Import every world module and return them in franchise / play order."""
    from .worlds import (holy_land, italy, constantinople, colonial_america,
                         caribbean, paris, chronicles, london, egypt, greece,
                         viking, baghdad, japan, hexe, atla, korra, seven_havens)
    return [m.WORLD for m in (holy_land, italy, constantinople, colonial_america,
                              caribbean, paris, chronicles, london, egypt, greece,
                              viking, baghdad, japan, hexe,
                              atla, korra, seven_havens)]
