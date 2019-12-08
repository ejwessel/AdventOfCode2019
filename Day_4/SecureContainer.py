
def check_increasing(num_str):
    valid = True
    min_str = num_str[0]
    for i in range(1, len(num_str)):
        # if encountering a num that is less than the seen min then stop
        if int(num_str[i]) < int(min_str):
            valid = False
            break
        min_str = num_str[i]
    return valid


def check_duplicates(num_str):
    duplicates = False
    for i in range(0, len(num_str) - 1):
        if num_str[i] == num_str[i + 1]:
            duplicates = True
            break
    return duplicates


def check_duplicates_freq(num_str):
    num_freq = {}
    for i in range(0, len(num_str)):
        if num_str[i] not in num_freq:
            num_freq[num_str[i]] = 1
        else:
            num_freq[num_str[i]] += 1

    for num in num_freq.values():
        # skip if freq is 1
        if num == 1:
            continue
        # # skip if freq is even, meaning it's not of 2 pair
        # if num % 2 == 0:
        #     return True
        if num == 2:
            return True
    return False


if __name__ == "__main__":
    valid_count = 0
    for num in range(156218, 652527):
        num_str = str(num)
        if not check_increasing(num_str):
            continue
        if not check_duplicates(num_str):
            continue

        # We made it here so the number must be valid
        valid_count += 1

    # Check the answer
    print(valid_count)
    assert valid_count == 1694

    # Part 2 ================

    result = check_duplicates_freq("156666")
    assert result == False
    result = check_duplicates_freq("123444")
    assert result == False
    result = check_duplicates_freq("111122")
    assert result == True
    reult = check_duplicates_freq("112233")
    assert result == True
    result = check_duplicates_freq("122244")
    assert result == True

    valid_count = 0
    for num in range(156218, 652527):
        num_str = str(num)
        if not check_increasing(num_str):
            continue
        if not check_duplicates(num_str):
            continue
        if not check_duplicates_freq(num_str):
            continue
        # We made it here so the number must be valid
        valid_count += 1

    # Check the answer
    print(valid_count)
    assert valid_count == 1148
