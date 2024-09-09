import click
import matplotlib.image as mpimg
import cv2
import numpy as np
import os

from image_modification import *

@click.command()
@click.option('--file_path', required= True, type=click.Path(exists=True), help='Input image path')
@click.option('--output_dir_path', required= True, type=click.Path(exists=True), help='Output image directory path')


def image_creation(file_path, output_dir_path):
    
    image = mpimg.imread(file_path)
    
    img_name = "MASP_" + file_path.split("\\")[-1].split(".")[0].split("_")[-2]
    
    output_path = output_dir_path + "\\" + img_name
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    src_points = np.float32([[0, 0], 
                            [0, image.shape[0]], 
                            [image.shape[1], 0], 
                            [image.shape[1], image.shape[0]]])

    dst_points = []

    for pair in src_points:
        l = []
        for i in range(len(pair)):
            print(pair[i])
            l.append(reshape(pair[i], image.shape[(i+1)//2]))
        dst_points.append(l)
        
    dst_points = np.float32(dst_points)

    all_points = [src_points, dst_points]

    all_dst_points = []

    for i in range(2):
        li = [all_points[i][0], None, None, None]
        for j in range(2):
            li[1] = all_points[j][1]
            for k in range(2):
                li[2] = all_points[k][2]
                for l in range(2):
                    li[3] = all_points[l][3]
                    all_dst_points.append(np.float32(li))
                    
    for i in range(len(all_dst_points)):

        # Get the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(src_points, all_dst_points[i])

        for j in range(8):
            
            # Perform the perspective warp
            image_ = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))
            image_ = rotate_image(image_, j * 45)
            
            matrix_shape = (image.shape[0], image.shape[1], 3)
            fundo = np.random.randint(256, size=matrix_shape) 
            condition = image_ == [0,0,0]
            image_[condition] = fundo[condition]
            
            
            image_rgb = cv2.cvtColor(image_, cv2.COLOR_BGR2RGB)

            # Save the image using OpenCV
            cv2.imwrite(output_path + f'/{img_name}_{i}_{j}.jpg', image_rgb)
            
            image_gray = cv2.cvtColor(image_, cv2.COLOR_BGR2GRAY)

            # Save the image using OpenCV
            cv2.imwrite(output_path + f'/{img_name}_{i}_{j}_gray.jpg', image_gray)
    
    return

if __name__ == "__main__":
    image_creation()