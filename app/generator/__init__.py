import base64
import uuid
from os import remove
from os.path import isfile

from MyQR import myqr


def utf16to8(input_txt: str) -> str:
    out = []
    for idx in range(len(input_txt)):
        ch = ord(input_txt[idx])
        if 0x0001 <= ch <= 0x007f:
            out.append(input_txt[idx])
        elif ch > 0x07ff:
            out.append(chr(0xE0 | (ch >> 12 & 0x0F)))
            out.append(chr(0x80 | (ch >> 6 & 0x3F)))
            out.append(chr(0x80 | (ch >> 0 & 0x3F)))
        else:
            out.append(chr(0xC0 | (ch >> 6) & 0x1f))
            out.append(chr(0x80 | (ch >> 0) & 0x3f))

    return ''.join(out)


class Generator(object):
    @staticmethod
    def gen_normal_qrcode(text: str) -> str:
        target_filename = Generator._get_rnd_png_filename()
        version, level, qr_name = myqr.run(utf16to8(text), save_name=target_filename)
        result_str = None
        file = None
        try:
            file = open(qr_name, 'rb')
            result_str = base64.b64encode(file.read())
        except Exception as e:
            print(e)
        finally:
            if file is not None:
                file.close()
                remove(qr_name)
            if isfile(target_filename):
                remove(target_filename)

        return str(result_str, 'utf-8')

    @staticmethod
    def gen_picture_qrcode(text: str, pic_file_path, colorized=True) -> str:
        target_filename = Generator._get_rnd_png_filename()
        version, level, qr_name = myqr.run(utf16to8(text), picture=pic_file_path, colorized=colorized, save_name=target_filename)
        result_str = None
        file = None
        try:
            file = open(qr_name, 'rb')
            result_str = base64.b64encode(file.read())
        except Exception as e:
            print(e)
        finally:
            if file is not None:
                file.close()
                remove(qr_name)
            if isfile(pic_file_path):
                remove(pic_file_path)
            if isfile(target_filename):
                remove(target_filename)

        return str(result_str, 'utf-8')

    @staticmethod
    def gen_gif_qrcode(text: str, pic_file_path, colorized=True) -> str:
        target_filename = Generator._get_rnd_gif_filename()
        print(target_filename)
        result_str = None
        file = None

        try:
            version, level, qr_name = myqr.run(utf16to8(text), picture=pic_file_path, colorized=colorized,
                                               save_name=target_filename)
            file = open(qr_name, 'rb')
            result_str = base64.b64encode(file.read())
        except Exception as e:
            print(e)
        finally:
            if file is not None:
                file.close()
                remove(target_filename)
            if isfile(pic_file_path):
                remove(pic_file_path)
            if isfile(target_filename):
                remove(target_filename)

        return str(result_str, 'utf-8')

    @staticmethod
    def _get_rnd_png_filename():
        return str(uuid.uuid4()) + '.png'

    @staticmethod
    def _get_rnd_gif_filename():
        return str(uuid.uuid4()) + '.gif'
