def parseImageFile(file_input, x, y):
    with open(file_input) as data:
        for line in data:
            return parseImage(line, x, y)

def parseImage(data_content, x, y):
    data_content = str(data_content)
    image_layers = []

    while len(data_content) > 0:
        image = []
        for i in range(y):
            data = data_content[:x]
            data_content = data_content[x:]
            image.append(data)
        image_layers.append(image)

    return image_layers

def getNumFreq(image):
    num_freq = {}
    for row in image:
        for pixel in range(len(row)):
            if row[pixel] not in num_freq:
                num_freq[row[pixel]] = 0
            num_freq[row[pixel]] += 1
    return num_freq


if __name__ == "__main__":

    output = parseImage(123456789012, 3, 2)
    image1_freq = getNumFreq(output[0])
    image2_freq = getNumFreq(output[1])
    assert image1_freq == {'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1}
    assert image2_freq == {'7': 1, '8': 1, '9': 1, '0': 1, '1': 1, '2': 1}

    output = parseImage(113416700012, 3, 2)
    image1_freq = getNumFreq(output[0])
    image2_freq = getNumFreq(output[1])
    assert image1_freq == {'1': 3, '3': 1, '4': 1, '6': 1}
    assert image2_freq == {'7': 1, '0': 3, '1': 1, '2': 1}


    output = parseImageFile("input.txt", 25, 6)
    best_freq = None
    for image in output:
       freq = getNumFreq(image)
       if best_freq is None:
           best_freq = freq
       elif freq['0'] < best_freq['0']:
           best_freq = freq

    product = best_freq['1'] * best_freq['2']
    print(product)

