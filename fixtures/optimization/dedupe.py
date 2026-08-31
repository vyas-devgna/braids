def dedupe(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
