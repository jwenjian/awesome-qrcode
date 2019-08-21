import base64
import uuid
from os import remove
from os.path import isfile

from MyQR import myqr


class Generator(object):
    @staticmethod
    def gen_normal_qrcode(text: str) -> str:
        target_filename = Generator._get_rnd_png_filename()
        version, level, qr_name = myqr.run(text, save_name=target_filename)
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
        version, level, qr_name = myqr.run(text, picture=pic_file_path, colorized=colorized, save_name=target_filename)
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
            version, level, qr_name = myqr.run(text, picture=pic_file_path, colorized=colorized,
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
