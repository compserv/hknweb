from typing import Dict

from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Weighting:
    @staticmethod
    def weight(tutor: Tutor, slot: Slot) -> float:
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

    @staticmethod
    def weight(tutor: Tutor, slot: Slot) -> float:
        retval: float = 0.00;

        # Add the time preference
        retval += Butler.TIME_PREF_TOW[tutor.slot_prefs[slot.slot_id]]

        # Add the office preference
        retval += tutor.office_prefs[slot.slot_id]

        for s in tutor.slots:
            if s.day == slot.day:
                if s.adjacent(slot):
                    retval += Butler.SAME_DAY_ADJACENCY[tutor.adjacent_pref]
                else:
                    retval -= 1000
            else:
                retval += Butler.DIFFERENT_DAY_ADJACENCY[tutor.adjacent_pref]

        return retval
