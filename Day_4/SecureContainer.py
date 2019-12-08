if __name__ == "__main__":

    valid_count = 0
    for num in range(156218, 652527):

        # Rule - Increasing Check
        num_str = str(num)
        valid = True
        min_str = num_str[0]
        for i in range(1, len(num_str)):
            # if encountering a num that is less than the seen min then stop
            if int(num_str[i]) < int(min_str):
                valid = False
                break
            min_str = num_str[i]

        # Rule - Duplicate
        duplicates = False
        if valid:
            for i in range(0, len(num_str) - 1):
                if num_str[i] == num_str[i + 1]:
                    duplicates = True
                    break

        # check if rules hold
        if valid and duplicates:
            print(num)
            valid_count += 1

    print(valid_count)