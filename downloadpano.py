import requests
import cv2

import os

def download(url, filename):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the content of the response (the image binary data)
            image_data = response.content
            
            # Specify the local file path where you want to save the image
            local_file_path = filename
            
            # Open a local file in binary write mode and write the image data
            with open(local_file_path, "wb") as image_file:
                image_file.write(image_data)
            
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def stitch(n):
    # Load the four input images
    image1 = cv2.imread(str(n) + "_0_0.jpg")
    image2 = cv2.imread(str(n) + "_0_1.jpg")
    image3 = cv2.imread(str(n) + "_1_0.jpg")
    image4 = cv2.imread(str(n) + "_1_1.jpg")

    height, width, channels = image1.shape

    # Create an empty canvas for the stitched image
    result_image = cv2.resize(image1, (2 * width, 2 * height))

    # Stitch the images together
    result_image[0:height, 0:width] = image1
    result_image[0:height, width:] = image2
    result_image[height:, 0:width] = image3
    result_image[height:, width:] = image4

    # Save the stitched image to a file
    cv2.imwrite(str(n) + '.jpg', result_image)


# URL of the image you want to download
image_url = "https://museusdigitais.pe.gov.br/wp-content/uploads/static-html-to-wp/data/9be6f15638bb21be3d4dd7f607a8c806/p360tourdata/dsc_3944_panorama2_475/"

for x in range(0,6):
    for a in range(0,2):
        for b in range(0,2):
            temp = image_url + str(x) + "/0/" + str(a) + "_" + str(b) + ".jpg" 
            print(temp)
            download(temp, str(x)+"_"+str(a)+"_"+str(b)+".jpg")
    stitch(x)
    #for a in range(0,2):
    #    for b in range(0,2):
    #        os.remove(str(x)+"_"+str(a)+"_"+str(b)+".jpg")