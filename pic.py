from pathlib import Path
from PIL import Image
import math

PIXEL_IMAGE_SIZE = 32
use_image_flg = True
output_image_flg = False

def get_img_avrg(image: Image): #画像のR, G, B毎の平均値を求める
    data = list(image.getdata())
    r, g, b = 0, 0, 0
    for pxl in data:
        r += pxl[0]
        g += pxl[1]
        b += pxl[2]

    r /= len(data)
    g /= len(data)
    b /= len(data)
    return int(r), int(g), int(b)
    

def resize_square(image: Image, size:int, flg:bool): #画像を縮小、正方形に加工
    w, h = image.size
    if flg == True:
        if w > h:
            image = image.crop((int((w-h)/2), 0, int((w-h)/2+h), h))
        else:
            image = image.crop((0, int((h-w)/2), w, int((h-w)/2+w)))

        image = image.resize((size, size))
    else:
        if w > h:
            image = image.resize((size, int((h*size)/w)))
        else:
            image = image.resize((int((w*size)/h), size))
    return image



def make_use_image_list(input_dir:str): #指定されたフォルダから画像を取得、そのパスをlistで返す
    types = ("jpg", "png", "jpeg")
    use_image_list_path = []
    for ext in types:
        use_image_list_unst = list(Path(input_dir).glob(f"*.{ext}"))
        use_image_list_path += use_image_list_unst
    
    return list(use_image_list_path)

def nearPoint(r, g, b, points):   #最も近い点（＝似た画像）を検索
    result = [r, g, b]
    stdval = 196608
    for point in points:
        distance = ((point[0] - r)** 2 + (point[1] - g) ** 2 + (point[2] - b) ** 2)
        if stdval > distance:
            stdval = distance
            result[0] = int(point[0])
            result[1] = int(point[1])
            result[2] = int(point[2])
    return tuple(result)
        


if __name__ == "__main__":

    imsize = 64
    #入力用の関数    
    imtext = input("読み込みたい画像をドロップしてください")
    img_2 = Image.open(f"{imtext}")   #アウトプット用の画像

    imsize_text = input("出力画像のクオリティを選んで下さい：高 = H, 中 = M , 低 = L")
    if imsize_text == "H" or imsize_text == "h" or imsize_text == "ｈ":
        imsize = 256
    if imsize_text == "M" or imsize_text == "m" or imsize_text == "ｍ":
        imsize = 128
    if imsize_text == "L" or imsize_text == "l" or imsize_text == "ｌ":
        imsize = 64
    img_2 = resize_square(img_2, imsize, output_image_flg)   #アウトプット用の画像の処理
    # img_2.show()
    # print(get_img_avrg(img))

    input_dir = input("モザイクアートに使用したい写真のフォルダのパスを入力")
    output_dir = input("モザイクアートを保存したいフォルダのパスを入力")

    use_image_list_path =[]
    use_image_list_path = make_use_image_list(input_dir)   #ブロック画像のパスをリストに入れた

    use_image_dict_RGB_path = {():""} #{("R", "G", "B"):"path"}
    use_image_list_RGB = []   #RGB平均値のリスト

    for img in range(len(use_image_list_path)):   #ブロック画像についての処理
        use_image = Image.open(f"{use_image_list_path[img]}")
        use_image = resize_square(use_image, PIXEL_IMAGE_SIZE, use_image_flg)  #指定されたフォルダのブロック画像を全て加工

        c = get_img_avrg(use_image)

        use_image_list_RGB.append(c)
        use_image_dict_RGB_path[c] = (use_image_list_path[img])   #RGBの平均値と画像の辞書型

        print(use_image_list_RGB[img])
        print(use_image_dict_RGB_path[use_image_list_RGB[img]])

    output_img_data = list(img_2.getdata())
    
    #テスト用
    # test = nearPoint(output_img_data[0][0], output_img_data[0][1], output_img_data[0][2], use_image_list_RGB)

    # print(test)
    # print(f"{use_image_dict_RGB_path[test]}")
    # print(f"{use_image_dict_RGB_path[output_img_data[0][0], output_img_data[0][1], output_img_data[0][2]]}")

    pix = []   #左上から右下にかけて順に代入していく画像を格納
    n = 0
    (w, h) = img_2.size
    print(f"output_img_size, {(w, h)}")
    output_image = Image.new("RGB", (w*PIXEL_IMAGE_SIZE, h*PIXEL_IMAGE_SIZE))   #元の画像の縦横サイズ*代入する画像の縦横サイズ


    for i in output_img_data:   #各ピクセルに最も近い値を持つ画像を求める
        rgb = nearPoint(output_img_data[n][0], output_img_data[n][1], output_img_data[n][2], use_image_list_RGB)
        pix.append(f"{use_image_dict_RGB_path[rgb]}")
        n += 1
    for y in range(h):
        for x in range(w):
            use_image_final = Image.open(pix[y*w+x])
            use_image_final = resize_square(use_image_final, PIXEL_IMAGE_SIZE, use_image_flg)
            output_image.paste(use_image_final, (PIXEL_IMAGE_SIZE*x, PIXEL_IMAGE_SIZE*y))

    
    output_image.show()
    saveflg = input("保存しますか？y/n")
    if saveflg == "y" or saveflg == "Y" or saveflg == "ｙ" or saveflg == "Ｙ":
        output_image.save(f"{output_dir}/output_image.png")