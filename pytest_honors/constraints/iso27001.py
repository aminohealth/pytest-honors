import enum


@enum.unique
class ISO27001Controls(enum.Enum):
    """Enumeration of ISO 27001 controls.

    Using the definitions from
    http://gender.govmu.org/English/Documents/activities/gender%20infsys/AnnexIX1302.pdf
    """

    A_7_2_2 = "Information labelling and handling"
    A_15_2_1 = "Compliance with security policies and standards"
