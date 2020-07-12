import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import cv2
import numpy as np
from PIL import Image

MIN_WIDTH = 0
MIN_HEIGHT = 0
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

  # 最低幅以上かつ最低高さ以上の大きさの画像はレターボックス画像を作成しない
  if MIN_HEIGHT <= height and MIN_WIDTH <= width:
    return

  lb_height = MIN_HEIGHT if height < MIN_HEIGHT else height
  lb_width = MIN_WIDTH if width < MIN_WIDTH else width

  # ##### 以下はレターボックスを作成する処理 #####

  # レターボックスサイズの単色画像を生成
  blank_img = np.zeros((lb_height, lb_width, 3))
  # ここに
  for h in range(0, lb_height):
    for w in range(0, lb_width):
      blank_img[h, w] = [B, G, R]

  # 一旦ファイルに保存してcv画像として再読み込み
  blank_img_path = 'blank.png'
  cv2.imwrite(blank_img_path, blank_img)
  blank_img = cv2.imread(blank_img_path)
  os.remove(blank_img_path)

  # 重ね合わせた画像
  x_pos = int(MIN_WIDTH / 2 - width / 2) if width < MIN_WIDTH else 0
  y_pos = int(MIN_HEIGHT / 2 - height / 2) if height < MIN_HEIGHT else 0
  overlay_image = overlayImage(
      blank_img, src_img, (x_pos, y_pos))

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


def input_RGB(R_or_G_or_B):
  color = 0
  try:
    color = int(input(f'{R_or_G_or_B}を入力してください(0~255):'))
    if 0 <= color and color < 255:
      return (True, color)
  except:
    pass
  print('0~255の範囲で入力してください。')
  return (False, color)


def ask_RGB(R_or_G_or_B):
  while True:
    R = input_RGB(R_or_G_or_B)
    if R[0]:
      break
  return R[1]


def input_nonnegative_integer(text):
  i = 0
  try:
    i = int(input(text))
    if 0 < i:
      return (True, i)
  except:
    pass
  print('0より大きい数字で入力してください。')
  return (False, i)


def ask_nonnegative_integer(text):
  while True:
    result = input_nonnegative_integer(text)
    if result[0]:
      break
  return result[1]



if __name__ == '__main__':
  try:
    selected_dir = select_dir()
    if selected_dir != '':
      MIN_WIDTH = ask_nonnegative_integer('最小幅を入力してください:')
      MIN_HEIGHT = ask_nonnegative_integer('最小高さを入力してください:')
      R = ask_RGB('R(赤)')
      G = ask_RGB('G(緑)')
      B = ask_RGB('B(青)')
      execute_dir(selected_dir, ['.png', '.jpg', '.jpeg'])
      print('完了しました。')
  except Exception as err:
    print('エラーが発生しました。')
    print(str(err))
  input('何かキーを押してください..')
