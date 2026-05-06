"""Tests for the army module."""

import pytest

from army import Army, Unit


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

class TestUnit:
    def test_create_unit(self):
        unit = Unit("Knight", "cavalry", attack=10, defense=8, health=50)
        assert unit.name == "Knight"
        assert unit.unit_type == "cavalry"
        assert unit.attack == 10
        assert unit.defense == 8
        assert unit.health == 50

    def test_unit_repr(self):
        unit = Unit("Archer", "ranged", attack=7, defense=3, health=30)
        r = repr(unit)
        assert "Archer" in r
        assert "ranged" in r

    def test_unit_negative_attack_raises(self):
        with pytest.raises(ValueError):
            Unit("Bad", "infantry", attack=-1, defense=5, health=20)

    def test_unit_negative_defense_raises(self):
        with pytest.raises(ValueError):
            Unit("Bad", "infantry", attack=5, defense=-1, health=20)

    def test_unit_zero_health_raises(self):
        with pytest.raises(ValueError):
            Unit("Ghost", "infantry", attack=5, defense=5, health=0)

    def test_unit_zero_attack_and_defense_allowed(self):
        unit = Unit("Medic", "support", attack=0, defense=0, health=15)
        assert unit.attack == 0
        assert unit.defense == 0


# ---------------------------------------------------------------------------
# Army tests
# ---------------------------------------------------------------------------

class TestArmy:
    def _make_unit(self, name="Soldier", attack=5, defense=5, health=20):
        return Unit(name, "infantry", attack=attack, defense=defense, health=health)

    def test_empty_army(self):
        army = Army("Red Army")
        assert army.name == "Red Army"
        assert army.size == 0
        assert army.total_attack == 0
        assert army.total_defense == 0
        assert army.total_health == 0
        assert army.strength() == 0

    def test_add_unit(self):
        army = Army("Blue Army")
        unit = self._make_unit("Spearman")
        army.add_unit(unit)
        assert army.size == 1
        assert army.units[0] is unit

    def test_add_multiple_units(self):
        army = Army("Green Army")
        for i in range(3):
            army.add_unit(self._make_unit(f"Unit{i}"))
        assert army.size == 3

    def test_units_returns_copy(self):
        army = Army("Test")
        army.add_unit(self._make_unit("A"))
        copy = army.units
        copy.append(self._make_unit("B"))
        assert army.size == 1  # original unchanged

    def test_add_non_unit_raises(self):
        army = Army("Bad Army")
        with pytest.raises(TypeError):
            army.add_unit("not a unit")  # type: ignore[arg-type]

    def test_remove_unit(self):
        army = Army("Alpha")
        unit = self._make_unit("Warrior")
        army.add_unit(unit)
        removed = army.remove_unit("Warrior")
        assert removed is unit
        assert army.size == 0

    def test_remove_unit_not_found_raises(self):
        army = Army("Alpha")
        with pytest.raises(ValueError):
            army.remove_unit("Ghost")

    def test_remove_first_matching_unit(self):
        army = Army("Gamma")
        u1 = self._make_unit("Twin", attack=1)
        u2 = self._make_unit("Twin", attack=2)
        army.add_unit(u1)
        army.add_unit(u2)
        removed = army.remove_unit("Twin")
        assert removed is u1
        assert army.size == 1

    def test_total_stats(self):
        army = Army("Stats")
        army.add_unit(Unit("A", "infantry", attack=10, defense=5, health=30))
        army.add_unit(Unit("B", "cavalry", attack=8, defense=7, health=40))
        assert army.total_attack == 18
        assert army.total_defense == 12
        assert army.total_health == 70
        assert army.strength() == 100

    def test_repr(self):
        army = Army("MyArmy")
        r = repr(army)
        assert "MyArmy" in r
        assert "size=" in r
        assert "strength=" in r
