import pathlib
import re

src_dir = pathlib.Path('$HIP/shot/DPP/EP01/Animation/test_animation_v001.usdnc')
print(src_dir.parent)
ext = src_dir.suffixes[0]
# if exists
aa = str(src_dir.name)
print(aa)

number = int(aa.split('_v')[-1].split('.')[0]) + 1
depart = aa.split('_v')[0]

print(ext)
print('depart', depart)

s_dir = pathlib.Path('/'.join(src_dir.as_posix().split('/')[:-1]))
o = pathlib.Path(s_dir/f"{depart}_v{number:03}{ext}")
# test_animation_v
# .usdnc


print(src_dir)
print(o)

