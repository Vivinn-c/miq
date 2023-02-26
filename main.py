from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pilmoji import Pilmoji
import textwrap

BASE_GRADATION_IMAGE = Image.open('base-gd.png')
BASE_WHITE_IMAGE = Image.open('base.png')

ICON = 'icon.png'

MPLUS_FONT_16 = ImageFont.truetype('fonts/MPLUSRounded1c-Regular.ttf', size=16)

def draw_text(im, ofs, string, font='fonts/MPLUSRounded1c-Regular.ttf', size=16, color=(0,0,0,255), split_len=None, padding=4, auto_expand=False, emojis: list = [], disable_dot_wrap=False):
    
    draw = ImageDraw.Draw(im)
    fontObj = ImageFont.truetype(font, size=size)

    # 改行、句読点(。、.,)で分割した後にさらにワードラップを行う
    pure_lines = []
    pos = 0
    l = ''

    if not disable_dot_wrap:
        for char in string:
            if char == '\n':
                pure_lines.append(l)
                l = ''
                pos += 1
            elif char == '、' or char == ',':
                pure_lines.append(l + ('、' if char == '、' else ','))
                l = ''
                pos += 1
            elif char == '。' or char == '.':
                pure_lines.append(l + ('。' if char == '。' else '.'))
                l = ''
                pos += 1
            else:
                l += char
                pos += 1

        if l:
            pure_lines.append(l)
    else:
        pure_lines = string.split('\n')

    lines = []

    for line in pure_lines:
        lines.extend(textwrap.wrap(line, width=split_len))
    
    dy = 0

    draw_lines = []


    # 計算
    for line in lines:
        tsize = fontObj.getsize(line)

        ofs_y = ofs[1] + dy
        t_height = tsize[1]

        x = int(ofs[0] - (tsize[0]/2))
        draw_lines.append((x, ofs_y, line))
        ofs_y += t_height + padding
        dy += t_height + padding
    
    # 描画
    adj_y = -30 * (len(draw_lines)-1)
    for dl in draw_lines:
        with Pilmoji(im) as p:
            p.text((dl[0], (adj_y + dl[1])), dl[2], font=fontObj, fill=color, emojis=emojis, emoji_position_offset=(-4, 4))

    real_y = ofs[1] + adj_y + dy

    return (0, dy, real_y)

content = "これってなんですかね？知らないんですけどwwww でも結局はあれだよね"
# 引用する
img = BASE_WHITE_IMAGE.copy()

icon = Image.open(ICON)
icon = icon.resize((720, 720), Image.ANTIALIAS)
icon = icon.convert('L')
icon_filtered = ImageEnhance.Brightness(icon)

img.paste(icon_filtered.enhance(0.7), (0,0))

# 黒グラデ合成
img.paste(BASE_GRADATION_IMAGE, (0,0), BASE_GRADATION_IMAGE)

# テキスト合成
tx = ImageDraw.Draw(img)

base_x = 890

# 文章描画
tsize_t = draw_text(img, (base_x, 270), content, size=45, color=(255,255,255,255), split_len=16, auto_expand=True)

# 名前描画
uname = 'Taka005#6668'
name_y = tsize_t[2] + 40
tsize_name = draw_text(img, (base_x, name_y), uname, size=25, color=(255,255,255,255), split_len=25, disable_dot_wrap=True)

# ID描画
id = '000000000000'
id_y = name_y + tsize_name[1] + 4
tsize_id = draw_text(img, (base_x, id_y), f'({id})', size=18, color=(180,180,180,255), split_len=45, disable_dot_wrap=True)

# クレジット
tx.text((1125, 694), 'TakasumiBOT#7189', font=MPLUS_FONT_16, fill=(120,120,120,255))

img.save('quote.png', quality=95)