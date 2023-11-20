import cv2
import os
import time
from PIL import Image

print('''
NOTE: Make sure the input image is in the same directory as the executable/python file! 
      
Choose the Appropriate option(1 2 3) from below:
      
1.Encode text in an image (without password)
2.Decode image and extract text (without password)
3.Do both (Encode/Decode with password)
      
''')

user_inp = int(input('>'))


def text_to_binary(text):
    binary_result = ''.join(format(ord(char), '08b') for char in text)
    return binary_result


def hide_text(image_input, secret_text, output_image):
    image = Image.open(image_input)
    binary_secret_text = text_to_binary(secret_text)
    binary_secret_text += '1111111111111110'

    data_index = 0
    pixels = list(image.getdata())

    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):
            if data_index < len(binary_secret_text):
                pixel[j] = pixel[j] & ~1 | int(binary_secret_text[data_index])
                data_index += 1
            else:
                break

        pixels[i] = tuple(pixel)

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(pixels)
    new_image.save(output_image)


def extract_text(image_input):
    image = Image.open(image_input)
    binary_secret_text = ''
    pixels = list(image.getdata())

    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):
            binary_secret_text += str(pixel[j] & 1)

    index = binary_secret_text.find('1111111111111110')
    secret_text_binary = binary_secret_text[:index]
    secret_text = ''.join([chr(int(secret_text_binary[i:i+8], 2))
                          for i in range(0, len(secret_text_binary), 8)])

    return secret_text


# Encode only
if user_inp == 1:
    try:
        print('Enter full image name with extension to encode: ')
        image_input = input(r'>')
        print('Similarly enter the filename to be saved after encoding image: ')
        output_image = input(r'>')
        secret_text = str(input('Enter the text message you want to hide: '))
        hide_text(image_input, secret_text, output_image)
        print('Done encoding image! Opening image...')
        time.sleep(2)
        os.system("start "+output_image)
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")


# Decode only
if user_inp == 2:
    try:
        print('Enter full Encoded image name with extension in current directory: ')
        output_image = input(r'>')
        extracted_text = extract_text(output_image)
        print("Success! Extracted Text: ", extracted_text)
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")


# Both encoding and decoding
if user_inp == 3:
    d = {}
    c = {}
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)
    m = 0
    n = 0
    z = 0

    print("Enter the image name with extension: ")
    img_path = str(input())
    print()
    img = cv2.imread(img_path)

    # Encoding a text in an image:
    msg = input("Enter secret message: ")
    password = input("Set a passcode for decryption: ")
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    cv2.imwrite("encrypted.png", img)
    print()
    print("SUCCESS! Opening encrpyted image now ")
    print()
    time.sleep(2)
    os.system("start encrypted.png")

    # Decoding an image for extracting text:
    message = ""
    m = 0
    n = 0
    z = 0
    image = str
    pas = input("Enter passcode for Decryption: ")
    if password == pas:
        for i in range(len(msg)):
            message = message + c[img[n, m, z]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3
        print("Success! Decryption message: ", message)

    else:
        print("Wrong password! ")
    time.sleep(10)