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

def getSmallestZeroFreq(images):
    best_freq = None
    for image in images:
        freq = getNumFreq(image)
        if best_freq is None:
            best_freq = freq
        elif freq['0'] < best_freq['0']:
            best_freq = freq
    return best_freq


if __name__ == "__main__":

    #Part 1
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
    freq = getSmallestZeroFreq(output)
    assert freq == {'1': 15, '2': 130, '0': 5}
    product = freq['1'] * freq['2']
    assert product == 1950

    #Part 2

    # image rules
    # 0 is black
    # 1 is white
    # 2 is transparent
    # ordering of image has precedence
    # 0 + 1 + 2 = 0
    # 2 + 2 + 0 + 1 = 0

    # 0 + 1 + 2 + 0 = 0
    # 2 + 1 + 2 + 0 = 1
    # 2 + 2 + 1 + 0 = 1
    # 2 + 2 + 2 + 0 = 0

    # seems the rule is to find the first instance of a 0 or 1 when going down layers

    # inspect every pixel
    final_image = []
    image_layers = parseImageFile("input.txt", 25, 6)
    print(image_layers)
    row_size = len(image_layers[0])
    col_size = len(image_layers[0][0])
    for row in row_size:
        for col in col_size:
            best_pixel = 3
            for layer in len(image_layers):

                # go through the layers
                # get first number smaller than 2
                # if best pixel has been identified break out of for loop
                if best_pixel is 3:
                    best_pixel = image_layers[row][col]





