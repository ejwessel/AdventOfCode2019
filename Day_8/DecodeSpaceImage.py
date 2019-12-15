from PIL import Image

def parseImageFile(file_input, x, y):
    with open(file_input) as data:
        for line in data:
            return parseImage(line, x, y)

def parseImage(data_content, x, y):
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

def decodeImages(image_layers):
    final_image = []
    row_size = len(image_layers[0])
    col_size = len(image_layers[0][0])
    for row in range(row_size):
        for col in range(col_size):
            # best pixel initially is transparent
            best_pixel = '2'
            for layer in image_layers:
                if int(best_pixel) < int('2'):
                    # if best_pixel has been set then we've found the top pixel
                    break
                elif int(layer[row][col]) < int(best_pixel):
                    best_pixel = layer[row][col]
            # add the best pixel
            final_image.append(best_pixel)
    return final_image


if __name__ == "__main__":

    #Part 1
    output = parseImage("123456789012", 3, 2)
    image1_freq = getNumFreq(output[0])
    image2_freq = getNumFreq(output[1])
    assert image1_freq == {'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1}
    assert image2_freq == {'7': 1, '8': 1, '9': 1, '0': 1, '1': 1, '2': 1}

    output = parseImage("113416700012", 3, 2)
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

    image_layers = parseImage("0222112222120000", 2, 2)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '0110'

    image_layers = parseImage("012", 1, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '0'

    image_layers = parseImage("2201", 1, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '0'

    image_layers = parseImage("0120", 1, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '0'

    image_layers = parseImage("2120", 1, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '1'

    image_layers = parseImage("2210", 1, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '1'

    image_layers = parseImage("2220", 1, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '0'

    image_layers = parseImage("222210", 3, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '210'

    image_layers = parseImage("222210201", 3, 1)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '210'

    image_layers = parseImageFile("input.txt", 25, 6)
    decoded_image = decodeImages(image_layers)
    final_image = ''.join(decoded_image)
    assert final_image == '111101001001100100101000010000101001001010010100001110011000100101111010000100001010011110100101000010000101001001010010100001000010010100101001011110'

    # use an image library
    cmap = {'0': (255, 255, 255),
            '1': (0, 0, 0)}
    data = [cmap[letter] for letter in final_image]
    img = Image.new('RGB', (25, len(final_image) // 6), "white")
    img.putdata(data)
    img.show()

    # display the final image on the screen
    # the bits are not the answer
    final_image = final_image.replace('0', ' ')
    final_image = final_image.replace('1', '#')
    size = len(final_image)
    for row in range(0, size, 25):
        print(' '.join(final_image[row:row + 25]))
