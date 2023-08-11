def letter_grade(score):
    """
    Calculate a letter grade from the number score.

    :param score: The numerical score to be converted.
    :type score: float

    :return: The corresponding letter grade.
    :rtype: str
    """
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    return grade

def avg_score(scores):
    """
    Calculates the average score from a list of scores.

    :param scores: A list of numerical scores.
    :type scores: list[float]

    :return: The calculated average score.
    :rtype: float
    """
    total = 0
    for score in scores:
        total += score
    avg = total / len(scores)
    return avg