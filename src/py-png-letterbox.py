import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import cv2
import numpy as np
from PIL import Image

MIN_WIDTH = 0
R = 0
G = 0
B = 0


# 画像のオーバーレイ関数
def overlayImage(src, overlay, location):

    # 背景をPIL形式に変換
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    pil_src = Image.fromarray(src)
    pil_src = pil_src.convert('RGBA')

    # オーバーレイをPIL形式に変換
    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
    pil_overlay = Image.fromarray(overlay)
    pil_overlay = pil_overlay.convert('RGBA')

    # 画像を合成
    pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
    pil_tmp.paste(pil_overlay, location, pil_overlay)
    result_image = Image.alpha_composite(pil_src, pil_tmp)

    # OpenCV形式に変換
    return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)


def execute_file(path):
  # 画像の読み込み
  src_img = cv2.imread(path)

  # 高さと幅の取得
  height = src_img.shape[0]
  width = src_img.shape[1]

  # 最低幅以上の画像にはレターボックス画像を作成しない
  if MIN_WIDTH <= width:
    return


  # ##### 以下はレターボックスを作成する処理 #####

  # 幅が最低幅、高さが元画像と同じのまっくろ画像を生成
  blank_img = np.zeros((height, MIN_WIDTH, 3))
  # ここに
  for h in range(0, height):
    for w in range(0, MIN_WIDTH):
      blank_img[h, w] = [B, G, R]

  # 一旦ファイルに保存してcv画像として再読み込み
  blank_img_path = 'blank.png'
  cv2.imwrite(blank_img_path, blank_img)
  blank_img = cv2.imread(blank_img_path)
  os.remove(blank_img_path)

  # 重ね合わせた画像
  overlay_image = overlayImage(blank_img, src_img, (int(MIN_WIDTH / 2 - width / 2), 0))

  # 保存先
  dirname = os.path.dirname(path)
  basename = os.path.basename(path)
  splitext = os.path.splitext(basename)
  path_without_ext = splitext[0]
  ext = splitext[1]
  cv2.imwrite(f'{dirname}\\{path_without_ext}_letterbox{ext}', overlay_image)


def execute_dir(dir, exts):
  for item in os.listdir(dir):
    path = f'{dir}\\{item}'
    if os.path.isdir(path):
        execute_dir(path, exts)
    else:
      for ext in exts:
        if(item.endswith(ext)):
          try:
            execute_file(path)
          except Exception as err:
            print(str(err))


def select_dir():
  tkinter.messagebox.showinfo('py-img-letterbox', '対象フォルダを選択してください。')
  selected_dir = tkinter.filedialog.askdirectory()
  return selected_dir


if __name__ == '__main__':
  try:
    selected_dir = select_dir()
    if selected_dir != '':

      MIN_WIDTH = int(input('最小幅を入力してください:'))
      R = int(input('R(赤)を入力してください:'))
      G = int(input('G(緑)を入力してください:'))
      B = int(input('B(青)を入力してください:'))
      execute_dir(selected_dir, ['.png', '.jpg', '.jpeg'])
  except Exception as err:
    print(str(err))
