from typing import Dict

from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Weighting:
    @classmethod
    def weight(cls, tutor: Tutor, slot: Slot) -> float:
        """
        Parameters
        ----------
        tutor: Tutor
            Tutor to be matched, may already be partially assigned.
        slot: Slot
            Slot to be matched, may already have some tutors.

        Returns
        -------
        weight: float
            -1 if Tutor is already assigned to a simultaneous slot a nonnegative value otherwise

        """
        raise NotImplementedError()


class Butler(Weighting):
    TIME_PREF_TOW: Dict[int, float] = {
        0: -100000,  # unavailable
        1: 6,        # ambivalent
        2: 0.01,     # prefer
    }

    SAME_DAY_ADJACENCY: Dict[int, float] = {
        1: 5,       # Prefers adjacent
        0: -2,      # Indifferent
        -1: -3,     # Prefers not adjacent
    }

    DIFFERENT_DAY_ADJACENCY: Dict[int, float] = {
        1: -2,      # Prefers adjacent
        0: 0,       # Indifferent
        -1: 3,      # Prefers not adjacent
    }

    @classmethod
    def weight(cls, tutor: Tutor, slot: Slot) -> float:
        retval: float = 0.00;

        # Add the time preference
        retval += cls.TIME_PREF_TOW[tutor.slot_prefs[slot.slot_id]]

        # Add the office preference
        retval += tutor.office_prefs[slot.slot_id]

        for s in tutor.slots:
            if s.day == slot.day:
                if s.adjacent(slot):
                    retval += cls.SAME_DAY_ADJACENCY[tutor.adjacent_pref]
                else:
                    retval -= 1000
            else:
                retval += cls.DIFFERENT_DAY_ADJACENCY[tutor.adjacent_pref]

        return retval


class Gardener(Weighting):
    TIME_PREF_TOW: Dict[int, float] = {
        0: -1000,   # unavailable
        1: 20,      # ambivalent
        2: 40,      # prefer
    }

    ADJACENCY: Dict[int, float] = {
        0: 5,   # No preference
        1: 10,  # Prefer adjacent
    }

    @classmethod
    def weight(cls, tutor: Tutor, slot: Slot) -> float:
        retval: float = 0.0

        if tutor.adjacent_pref == 0:
            retval += cls.ADJACENCY[tutor.adjacent_pref]
        elif tutor.adjacent_pref == 1:
            has_adj = sum(slot.adjacent(s) for s in tutor.slots)
            retval += has_adj * cls.ADJACENCY[tutor.adjacent_pref]

        retval += cls.TIME_PREF_TOW[tutor.slot_prefs[slot.slot_id]]

        return retval


class OldGardener(Gardener):
    TIME_PREF_TOW: Dict[int, float] = {
        0: -1000,   # unavailable
        1: 10,      # ambivalent
        2: 20,      # prefer
    }
