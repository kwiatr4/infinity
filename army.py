"""Army module for Infinity.

Provides Unit and Army classes to build and manage armies.
"""


class Unit:
    """Represents a single military unit."""

    def __init__(self, name: str, unit_type: str, attack: int, defense: int, health: int):
        if attack < 0 or defense < 0 or health <= 0:
            raise ValueError("attack and defense must be >= 0, health must be > 0")
        self.name = name
        self.unit_type = unit_type
        self.attack = attack
        self.defense = defense
        self.health = health

    def __repr__(self) -> str:
        return (
            f"Unit(name={self.name!r}, type={self.unit_type!r}, "
            f"attack={self.attack}, defense={self.defense}, health={self.health})"
        )


class Army:
    """Represents an army composed of multiple units."""

    def __init__(self, name: str):
        self.name = name
        self._units: list[Unit] = []

    def add_unit(self, unit: Unit) -> None:
        """Add a unit to the army."""
        if not isinstance(unit, Unit):
            raise TypeError("Only Unit instances can be added to an Army")
        self._units.append(unit)

    def remove_unit(self, unit_name: str) -> Unit:
        """Remove and return the first unit with the given name.

        Raises ValueError if no unit with that name exists.
        """
        for i, unit in enumerate(self._units):
            if unit.name == unit_name:
                return self._units.pop(i)
        raise ValueError(f"No unit named {unit_name!r} found in army {self.name!r}")

    @property
    def units(self) -> list[Unit]:
        """Return a copy of the unit list."""
        return list(self._units)

    @property
    def size(self) -> int:
        """Total number of units in the army."""
        return len(self._units)

    @property
    def total_attack(self) -> int:
        """Sum of attack values across all units."""
        return sum(u.attack for u in self._units)

    @property
    def total_defense(self) -> int:
        """Sum of defense values across all units."""
        return sum(u.defense for u in self._units)

    @property
    def total_health(self) -> int:
        """Sum of health values across all units."""
        return sum(u.health for u in self._units)

    def strength(self) -> int:
        """Overall strength score: total_attack + total_defense + total_health."""
        return self.total_attack + self.total_defense + self.total_health

    def __repr__(self) -> str:
        return f"Army(name={self.name!r}, size={self.size}, strength={self.strength()})"
