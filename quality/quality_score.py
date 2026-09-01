def calculate_quality_score(
    total_records,
    duplicate_count=0,
    null_count=0,
    invalid_count=0
):

    if total_records == 0:

        return 0

    total_issues = (
        duplicate_count
        + null_count
        + invalid_count
    )

    score = (
        (total_records - total_issues)
        / total_records
    ) * 100

    score = max(0, score)

    return round(score, 2)