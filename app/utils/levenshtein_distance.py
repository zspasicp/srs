
def minimum_edit_distance(first_string: str, second_string: str) -> int:
    distances = range(len(first_string) + 1)
    for index2,char2 in enumerate(second_string):
        newDistances = [index2+1]
        for index1,char1 in enumerate(first_string):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]


def similarity(longer_string: str, shorter_string: str) -> float:
    if(len(longer_string) < len(shorter_string)):
        longer_string, shorter_string = shorter_string, longer_string
    if(len(longer_string) == 0):
        return 1.0
    return (len(longer_string) - minimum_edit_distance(shorter_string, longer_string)) / float(len(longer_string))


if __name__ == '__main__':
    print(similarity('assa', 'asa'))