"""Cross-platform image file-paths"""

from pathlib import Path


images_prefix = ('assets', 'images')
path = Path().joinpath(*images_prefix)


add_img_path = path / 'add_icon.png'
close_img_path = path / 'close_icon.png'
delete_img_path = path / 'delete_icon.png'
update_img_path = path / 'update_icon.png'

