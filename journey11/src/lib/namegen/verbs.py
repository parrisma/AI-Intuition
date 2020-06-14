import numpy as np


class Verbs:
    _verbs = ["abashing",
              "abating",
              "abiding",
              "absorbing",
              "accepting",
              "accompanying",
              "aching",
              "achieving",
              "acquiring",
              "acting",
              "adding",
              "addressing",
              "adjusting",
              "admiring",
              "admitting",
              "advising",
              "affording",
              "agreeing",
              "alighting",
              "allowing",
              "animating",
              "announcing",
              "answering",
              "apologizing",
              "appearing",
              "applauding",
              "applying",
              "approaching",
              "approving",
              "arising",
              "arranging",
              "asking",
              "asserting",
              "assorting",
              "astonishing",
              "attending",
              "attracting",
              "awaking",
              "batting",
              "being",
              "beautifying",
              "befalling",
              "beginning",
              "behaving",
              "beholding",
              "believing",
              "belonging",
              "beseeching",
              "betting",
              "bidding",
              "binding",
              "blossoming",
              "blurring",
              "boasting",
              "bowing",
              "boxing",
              "braying",
              "bringing",
              "broadcasting",
              "buzzing",
              "calling",
              "canvassing",
              "carrying",
              "cashing",
              "catching",
              "causing",
              "celebrating",
              "challenging",
              "changing",
              "charging",
              "chasing",
              "chatting",
              "checking",
              "cheering",
              "choosing",
              "classifying",
              "cleaning",
              "clicking",
              "clinging",
              "collapsing",
              "collecting",
              "colouring",
              "commenting",
              "comparing",
              "compelling",
              "competing",
              "complaining",
              "completing",
              "conducting",
              "confiscating",
              "confusing",
              "congratulating",
              "connecting",
              "conserving",
              "considering",
              "consigning",
              "consisting",
              "consoling",
              "constituting",
              "constructing",
              "construing",
              "consulting",
              "containing",
              "contemning",
              "contending",
              "contesting",
              "continuing",
              "contrasting",
              "contributing",
              "contriving",
              "convening",
              "converging",
              "conversing",
              "converting",
              "conveying",
              "convincing",
              "cooling",
              "cooperating",
              "coping",
              "copying",
              "correcting",
              "corresponding",
              "costing",
              "coughing",
              "counting",
              "creating",
              "crossing",
              "crowding",
              "curving",
              "cycling",
              "damping",
              "dancing",
              "daring",
              "dashing",
              "dazzling",
              "deciding",
              "declaring",
              "decorating",
              "dedicating",
              "delaying",
              "depending",
              "deriving",
              "describing",
              "detecting",
              "determining",
              "developing",
              "differing",
              "dining",
              "directing",
              "disappearing",
              "discovering",
              "discussing",
              "diving",
              "donating",
              "downloading",
              "drawing",
              "dreaming",
              "driving",
              "drying",
              "educating",
              "empowering",
              "encouraging",
              "entangling",
              "endorsing",
              "enjoying",
              "enlightening",
              "entering",
              "envying",
              "escaping",
              "exchanging",
              "exclaiming",
              "expecting",
              "explaining",
              "expressing",
              "extending",
              "facing",
              "feeding",
              "ferrying",
              "fetching",
              "finding",
              "fishing",
              "fitting",
              "fizzing",
              "fleeing",
              "floating",
              "flying",
              "following",
              "forecasting",
              "foretelling",
              "forgiving",
              "forming",
              "founding",
              "framing",
              "freeing",
              "frightening",
              "fulfilling",
              "gaining",
              "glittering",
              "glowing",
              "googling",
              "greeting",
              "growing",
              "guarding",
              "guessing",
              "guiding",
              "happening",
              "hatching",
              "healing",
              "hearing",
              "helping",
              "hiding",
              "hopping",
              "hoping",
              "humming",
              "hurrying",
              "hushing",
              "hypnotizing",
              "idealizing",
              "identifying",
              "idolizing",
              "illuminating",
              "illustrating",
              "imagining",
              "imitating",
              "imparting",
              "impeding",
              "impelling",
              "imploring",
              "implying",
              "importing",
              "impressing",
              "imprinting",
              "improving",
              "including",
              "increasing",
              "inculcating",
              "indenting",
              "indicating",
              "indulging",
              "inflecting",
              "informing",
              "inheriting",
              "initiating",
              "innovating",
              "inputting",
              "inquiring",
              "inspiring",
              "installing",
              "integrating",
              "introducing",
              "inventing",
              "inviting",
              "joining",
              "jumping",
              "justifying",
              "keeping",
              "kidding",
              "knitting",
              "knowing",
              "lading",
              "landing",
              "lasting",
              "laughing",
              "leading",
              "leaning",
              "leaping",
              "learning",
              "leaving",
              "lifting",
              "lighting",
              "listening",
              "living",
              "looking",
              "magnifying",
              "maintaining",
              "making",
              "managing",
              "marching",
              "marking",
              "matching",
              "meaning",
              "measuring",
              "meeting",
              "migrating",
              "minding",
              "missing",
              "mixing",
              "modifying",
              "motivating",
              "moulting",
              "moving",
              "mowing",
              "multiplying",
              "murmuring",
              "napping",
              "needing",
              "nipping",
              "nodding",
              "noting",
              "noticing",
              "notifying",
              "nourishing",
              "nursing",
              "obeying",
              "obliging",
              "observing",
              "obstructing",
              "obtaining",
              "occupying",
              "occurring",
              "offering",
              "offsetting",
              "omitting",
              "opining",
              "opting",
              "optimizing",
              "organizing",
              "originating",
              "outputting",
              "overflowing",
              "overtaking",
              "painting",
              "patting",
              "patching",
              "pausing",
              "persuading",
              "phoning",
              "placing",
              "planning",
              "pleasing",
              "pointing",
              "pondering",
              "praising",
              "preferring",
              "preparing",
              "presenting",
              "presiding",
              "pressing",
              "pretending",
              "printing",
              "proceeding",
              "producing",
              "progressing",
              "promising",
              "proposing",
              "protecting",
              "proving",
              "providing",
              "qualifying",
              "racing",
              "raining",
              "rattling",
              "reaching",
              "reading",
              "realizing",
              "rebuilding",
              "recalling",
              "receiving",
              "reciting",
              "recognizing",
              "recollecting",
              "recurring",
              "referring",
              "reflecting",
              "regarding",
              "relating",
              "relaxing",
              "remaining",
              "renewing",
              "repeating",
              "replacing",
              "replying",
              "reporting",
              "requesting",
              "reselling",
              "resembling",
              "resetting",
              "resisting",
              "resolving",
              "respecting",
              "resting",
              "returning",
              "reviewing",
              "rewinding",
              "ringing",
              "ruling",
              "running",
              "rushing",
              "sailing",
              "saluting",
              "salvaging",
              "salving",
              "saturating",
              "sauntering",
              "saving",
              "savoring",
              "saying",
              "scanning",
              "scrawling",
              "scrubbing",
              "searching",
              "seating",
              "seeing",
              "seeking",
              "seeming",
              "selecting",
              "sending",
              "setting",
              "sewing",
              "shining",
              "shitting",
              "shivering",
              "shocking",
              "showing",
              "sighting",
              "signalling",
              "singing",
              "sipping",
              "sitting",
              "skiing",
              "skidding",
              "sleeping",
              "sliding",
              "slipping",
              "smiling",
              "sneezing",
              "sniffing",
              "soaring",
              "solving",
              "sorting",
              "sowing",
              "sparkling",
              "speaking",
              "spelling",
              "spending",
              "spinning",
              "splitting",
              "spraying",
              "spreading",
              "springing",
              "sprouting",
              "standing",
              "staring",
              "starting",
              "stating",
              "staying",
              "stealing",
              "steeping",
              "stemming",
              "stepping",
              "sticking",
              "stirring",
              "stitching",
              "storing",
              "straining",
              "straying",
              "striding",
              "striving",
              "studying",
              "succeeding",
              "suggesting",
              "supplying",
              "supporting",
              "surging",
              "surmising",
              "surpassing",
              "surrounding",
              "surveying",
              "surviving",
              "swaying",
              "sweeping",
              "swimming",
              "swinging",
              "taking",
              "teaching",
              "teeing",
              "telling",
              "tending",
              "testing",
              "thanking",
              "thinking",
              "thriving",
              "training",
              "travelling",
              "treasuring",
              "treating",
              "triumphing",
              "trusting",
              "trying",
              "typing",
              "understanding",
              "urging",
              "uttering",
              "valuing",
              "vanishing",
              "verifying",
              "vying",
              "viewing",
              "waking",
              "walking",
              "wandering",
              "warning",
              "watching",
              "waving",
              "welcoming",
              "wending",
              "whispering",
              "winning",
              "wishing",
              "working",
              "writing",
              "yawning",
              "zooming"]
    _verbs_length = len(_verbs)

    @staticmethod
    def random_verb() -> str:
        return Verbs._verbs[np.random.randint(Verbs._verbs_length, size=1)[0]]
