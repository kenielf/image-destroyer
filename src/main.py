from PIL import Image
from math import floor
import dearpygui.dearpygui as gui
from typing import Union


class DefaultLowQuality:
    OPTIMIZE = True
    QUALITY = 15
    RESIZE_PARAM = 0.63


def low_image(path: str, resize_factor: float, quality: int, optimize: Union[bool]) -> None:
    """
    Redimensiona uma imagem localizada no caminho especificado por `path` para uma nova resolução,
    calculada como o produto da dimensão original e o fator de redimensionamento `resize_factor`.
    Utiliza a interpolação bilinear para suavizar a imagem. A imagem redimensionada é salva como
    'image_saida.jpg' com as opções de otimização e qualidade especificadas pelos argumentos `optimize`
    e `quality`, respectivamente.

    Parameters
    ----------
    path : str
        Caminho para o arquivo de imagem a ser redimensionado.
    resize_factor : float
        Fator de redimensionamento a ser aplicado na imagem.
    quality : int
        Nível de qualidade da imagem salva, na escala de 0 a 100.
    optimize : bool
        Se deve aplicar otimização na imagem salva.

    Returns
    -------
    None

    Examples
    --------
    >>> low_image('imagem.jpg', 20, 80, True)
    """
    image = Image.open(path)
    new_resolution = floor(image.size[0] * resize_factor), floor(image.size[1] * resize_factor)
    image = image.resize(new_resolution, Image.BILINEAR)
    image.save("image_saida.jpg", optimize=optimize, quality=quality)


path_image: str = ""


def load_image(_, app_data):
    global path_image
    path_image = app_data["file_path_name"]


def process_image():
    if gui.get_value("check_default"):
        low_image(
            path_image,
            DefaultLowQuality.RESIZE_PARAM,
            DefaultLowQuality.QUALITY,
            DefaultLowQuality.OPTIMIZE,
        )
    else:
        low_image(
            path_image,
            gui.get_value("txt_fator_escala"),
            gui.get_value("slider_quality"),
            DefaultLowQuality.OPTIMIZE,
        )


def init_gui() -> None:
    gui.create_context()
    gui.create_viewport()
    gui.setup_dearpygui()
    with gui.window(label="Low quality image", no_close=True, width=800, height=200):
        with gui.file_dialog(
            directory_selector=False,
            show=False,
            callback=load_image,
            tag="file_dialog_image",
            width=700,
            height=400,
        ):
            gui.add_file_extension(".jpg")
            gui.add_file_extension(".jpeg")
            gui.add_file_extension(".png")
        gui.add_text("App para reduzir qualidade de imagens")
        gui.add_button(label="Importar imagem", callback=lambda: gui.show_item("file_dialog_image"))
        gui.add_input_float(
            label="Fator em % da escala",
            tag="txt_fator_escala",
            min_value=0.10,
            max_value=0.90,
        )
        gui.add_slider_int(label="Fator em % de qualidade", min_value=5, tag="slider_quality")
        gui.add_checkbox(label="Usar valores padrao", tag="check_default")
        gui.add_button(label="Processar", callback=process_image)
    gui.show_viewport()
    gui.start_dearpygui()
    gui.destroy_context()


def main():
    init_gui()


if __name__ == "__main__":
    main()
