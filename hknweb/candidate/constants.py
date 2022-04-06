class ATTR:
    CAND_CSV = "cand_csv"
    CANDIDATE = "candidate"
    COLOR = "color"
    CONFIRMED = "confirmed"
    CSV_ENDING = ".csv"
    EMAIL = "Email"
    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    NEXT = "next"
    NUM_BITBYTES = "num_bitbytes"
    NUM_CONFIRMED = "num_confirmed"
    NUM_PENDING = "num_pending"
    NUM_REJECTED = "num_rejected"
    POST = "POST"
    STATUS = "status"
    TITLE = "title"
    UNCONFIRMED = "unconfirmed"
    UTF8 = "utf-8"
    UTF8SIG = "utf-8-sig"


DOMAINS = [
    "@berkeley.edu",
    "@hkn.eecs.berkeley.edu",
]


class CandidateDTO:
    def __init__(self, candidate_attributes: dict):
        self.email = candidate_attributes.get(ATTR.EMAIL, None)
        self.first_name = candidate_attributes.get(ATTR.FIRST_NAME, None)
        self.last_name = candidate_attributes.get(ATTR.LAST_NAME, None)
        self.username = self.email
        if self.email is not None:
            for d in DOMAINS:
                if self.email.endswith(d):
                    self.username = self.email.replace(d, "")
                    break
        self.validate()

    def validate(self):
        assert self.email, "Candidate email must not be empty"
        assert any(
            self.email.endswith(d) for d in DOMAINS
        ), "Candidate email must be an @berkeley.edu or @hkn.eecs.berkeley.edu email"
        assert self.first_name, "Candidate first name must not be empty"
        assert self.last_name, "Candidate last name must not be empty"
        assert self.username, "Candidate username must not be empty"


DEFAULT_RANDOM_PASSWORD_LENGTH = 20


# Default hard-coded event types for candidate semester
# NOTE: these strings are also hard-coded in candidate/index.html
class EVENT_NAMES:
    MANDATORY = "Mandatory"
    BITBYTE = "bitbyte"
    HANGOUT = "officer_hangout"
    CHALLENGE = "officer_challenge"
    EITHER = "either"
    INTERACTIVITIES = "interactivities"


REQUIREMENT_TITLES_TEMPLATE = "{} ({} required, {} remaining)"
