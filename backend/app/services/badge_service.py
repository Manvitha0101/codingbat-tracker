def calculate_badges(students):
    # Sort by total solved to find top performers
    sorted_students = sorted(students, key=lambda x: x.total_solved, reverse=True)
    count = len(sorted_students)

    for i, student in enumerate(sorted_students):
        if student.total_solved == 0:
            student.badge = "Beginner"
        elif i < count * 0.10: # Top 10%
            student.badge = "Top Performer"
        elif student.total_solved > 30:
            student.badge = "Consistent Learner"
        else:
            student.badge = "Rising Star"
    return sorted_students