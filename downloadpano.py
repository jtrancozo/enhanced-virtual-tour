import requests
import cv2
import numpy as np
import os

from PIL import Image
import py360convert

IMG_DIRECTORY = "source/download_images/"
TOUR_DATA_URL = "https://museusdigitais.pe.gov.br/wp-content/uploads/static-html-to-wp/data/9be6f15638bb21be3d4dd7f607a8c806/p360tourdata/"
#PANO_DIRECTORY = "dsc_3944_panorama2_475"
#pano = '3944'

# URL of the image you want to download
# image_url = "https://museusdigitais.pe.gov.br/wp-content/uploads/static-html-to-wp/data/9be6f15638bb21be3d4dd7f607a8c806/p360tourdata/dsc_3944_panorama2_475/"


if not os.path.exists("source/download_images/"): 
    os.makedirs("source/download_images/")

if not os.path.exists("source/pano"): 
    os.makedirs("source/pano/")     


def download(url, filename, pano):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        pano_dir = f"{IMG_DIRECTORY}{pano}"
        local_file_path = f"{pano_dir}/{filename}"
        
        # Check if the request was successful (status code 200)
        #print(local_file_path)

        if (os.path.isfile(local_file_path)):
            #print("Imagem já existe.")
            return

        if response.status_code == 200:
            # Get the content of the response (the image binary data)
            image_data = response.content
            
            # Specify the local file path where you want to save the image

            if not os.path.exists(pano_dir):
                os.makedirs(pano_dir)

            #local_file_path = f"{pano_dir}/{filename}"
            
            # Open a local file in binary write mode and write the image data
            with open(local_file_path, "wb") as image_file:
                image_file.write(image_data)
            
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def toCubeMap (pano):
    # Load the four input images
    pano_dir = f"{IMG_DIRECTORY}{pano}"

    if not os.path.exists(pano_dir):
        os.makedirs(pano_dir)

    image_path = pano_dir + '/'
    file_name = image_path + "cubemap.png"

    left = cv2.imread(image_path + "0.jpg")
    front = cv2.imread(image_path + "1.jpg")
    right = cv2.imread(image_path + "2.jpg")
    back = cv2.imread(image_path + "3.jpg")
    top = cv2.imread(image_path + "4.jpg")
    bottom = cv2.imread(image_path + "5.jpg")

    height, width, channels = left.shape
    side = height

    #print(height, width, channels)

    # Create an empty canvas for the stitched image
    #blank_canvas = np.zeros((1,1,4), np.uint8)
    blank_canvas = np.zeros((1,1,3), np.uint8)
    result_image = cv2.resize(blank_canvas, (4 * width, 3 * height))

    # # Stitch the images together
    # array onde define Y e X, dando as coordenandas do eixo vertical e horizontal [y0: y1, x0:x1]
    result_image[0: side, side: 2 * side] = top
    result_image[side: 2*side, 0: side] = back
    result_image[side: 2*side, side: 2* side] = left
    result_image[side: 2*side, 2*side : 3* side] = front
    result_image[side: 2*side:, 3*side: 4* side] = right
    result_image[2*side: 3*side, side: 2*side] = bottom
    

    # dice = concat_vh([
    #     [],
    #     [],
    #     []
    # ])

    # cubemap = cv2.vconcat([cv2.hconcat(list_h) for list_h in dice])

    # Save the stitched image to a file
    cv2.imwrite(file_name , result_image)


def stitch(n, pano):
    pano_dir = f"{IMG_DIRECTORY}{pano}"

    if not os.path.exists(pano_dir):
        os.makedirs(pano_dir)

    # Load the four input images
    file_path = f"{pano_dir}/{n}"
    output_name = f"{file_path}.jpg"

    image1 = cv2.imread(file_path + "_0_0.jpg")
    image2 = cv2.imread(file_path + "_0_1.jpg")
    image3 = cv2.imread(file_path + "_1_0.jpg")
    image4 = cv2.imread(file_path + "_1_1.jpg")

    height, width, channels = image1.shape

    # Create an empty canvas for the stitched image
    result_image = cv2.resize(image1, (2 * width, 2 * height))

    # Stitch the images together
    result_image[0:height, 0:width] = image1
    result_image[0:height, width:] = image2
    result_image[height:, 0:width] = image3
    result_image[height:, width:] = image4

    # Save the stitched image to a file
    cv2.imwrite(output_name, result_image)

def toEquirectangular(panoName):
    height = 2048
    width = 4096
    mode = 'bilinear'
    image_path = f"source/download_images/{panoName}/cubemap.png"
    output_image = f"source/pano/{panoName}.jpg"

    # Read image
    image = np.array(Image.open(image_path))
    if len(image.shape) == 2:
        image = image[..., None]

    print("Criando imagem Equiretangular... " + panoName)   

    out = py360convert.c2e(image, h=height, w=width, mode=mode)

    # Output image
    Image.fromarray(out.astype(np.uint8)).save(output_image)


def makepano(panoName, pano_directory):
        
    if not (os.path.isfile(f"{pano_directory}{panoName}/cubemap.png")):
        for x in range(0,6):
            for a in range(0,2):
                for b in range(0,2):
                    temp = TOUR_DATA_URL + pano_directory + "/" + str(x) + "/0/" + str(a) + "_" + str(b) + ".jpg" 
                    #print(temp)
                    download(temp, str(x)+"_"+str(a)+"_"+str(b)+".jpg", panoName)
            stitch(x, panoName)
        
        try:
            toCubeMap(panoName)
        except:
            print("Erro ao criar o cubemap")

    #try:
    toEquirectangular(panoName)
    #except:
    #    print("Erro ao criar a imagem EquiRetangular")    

#"""
#for a in range(0,2):
#    for b in range(0,2):
#        os.remove(str(x)+"_"+str(a)+"_"+str(b)+".jpg")
# """    

##
# py360convert
#
# convert360 --convert c2e --i source/download_images/3944/cubemap.png --o equirect.png --w 4096 --h 2048 
#
