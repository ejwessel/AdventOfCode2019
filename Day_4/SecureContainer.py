
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