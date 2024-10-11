from PySide2.QtCore import QObject
DEFAULT_GRADE_SCALE = {
        "A":  4.00,
        "A-": 3.67,
        "B+": 3.33,
        "B":  3.00,
        "B-": 2.67,
        "C+": 2.33,
        "C":  2.00,
        "C-": 1.67,
        "D+": 1.33,
        "D":  1.00,
        "D-": 0.67,
        "E":  0.00,
        "F":  0.00
    }

class GradingSettings(QObject):
    """Class to hold data for grading."""
    def __init__(self, data, parent: QObject | None = ...):
        super().__init__(parent)
        self.data = data
        self.grade_scale = self.data["Grading Scale"]
        if self.grade_scale is None:
            self.grade_scale = DEFAULT_GRADE_SCALE


    def letter_grade_exists(self, letter_grade: str) -> bool:
        """Checks if letter grade is in the Grade Scale

        Args:
            letter_grade (str): The letter grade to check

        Returns:
            bool: If it exists in the grade scale
        """
        return letter_grade in self.grade_scale


    def letter_grade_value(self, letter_grade: str) -> float:
        """Returns the value for GPA tied to a letter grade

        Args:
            letter_grade (str): The index for the value

        Returns:
            float: The value for GPA calculations
        """
        if not self.letter_grade_exists(letter_grade):
            return -1.00
        return self.grade_scale[letter_grade]
