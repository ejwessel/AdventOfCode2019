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

if __name__ == "__main__":

    output = parseImage(123456789012, 3, 2)
    print(output)

    output = parseImageFile("input.txt", 25, 6)
    print(output)
