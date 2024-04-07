import hou

with open('/Users/yeko/Desktop/netflix_TD/Final_project/libs/hou_lib/tree_group.py', 'r') as f:
    tree_group = f.read()

t_btn = hou.ButtonParmTemplate(
    name='group_tree', label='Select Your Name',
    script_callback=tree_group,
    script_callback_language=hou.scriptLanguage.Python
)

node = kwargs['node']
print(f'created {node.name()}')

# hide original render button
ptg = node.parmTemplateGroup()
ptg.hide('execute', True)

# setup custom render button
r_btn = hou.ButtonParmTemplate(
    name='custom_execute', label='Render USD', join_with_next=True,
    script_callback="""
import pathlib
import re
from libs.hou_lib import db_up

lop_dir = pathlib.Path(hou.pwd().parm('lopoutput').eval())

ext = lop_dir.suffixes[0]
s_dir = lop_dir.parent
src_dir = None

if lop_dir.exists():
    fname = str(lop_dir.name)
    num = int(fname.split('_v')[-1].split('.')[0]) + 1
    depart = fname.split('_v')[0]
    re_src_dir = pathlib.Path(s_dir/f"{depart}_v{num:03}{ext}")
    src_dir = re_src_dir
    print('src:', src_dir)
elif lop_dir.exists() == False:
    src_dir = lop_dir
    print('src:', src_dir)
    
fin_name = re.sub(r'_v\d+', '', src_dir.name)
cpath = src_dir.as_posix()
db_up.update_files(fin_name, cpath)
hou.pwd().parm('execute').pressButton()
""",
    script_callback_language=hou.scriptLanguage.Python
)


# setup reference note
note = hou.StringParmTemplate(
    name='refnote', label='Reference Note', num_components=1,
    default_value=('ex)add lines on its body',)
)

# setup username
uname = hou.StringParmTemplate(
    name='username', label='Your Name', num_components=1,
    default_value=('ex)jason',)
)

node.parm('lopoutput').set(f'$HIP/geo/test_v001.usd')

# script for post render
postrender_expr = """
import pathlib
import os
import re

final_path = pathlib.Path.home() / 'workspace' / 'final'
if not final_path.exists():
    os.mkdir(final_path.as_posix())
    
src_dir = pathlib.Path(hou.parm('lopoutput').eval())
ext = src_dir.suffixes[0]
print('src:', src_dir)
s_dir = src_dir.parent

if src_dir.exists():
    fname = str(src_dir.name)
    num = int(fname.split('_v')[-1].split('.')[0]) + 1
    depart = fname.split('_v')[0]
    re_src_dir = pathlib.Path(s_dir/f"{depart}_v{num:03}{ext}")

print('s:', s_dir)
if not s_dir.exists():
    os.mkdir(s_dir)
    
fin_name = pathlib.Path(re.sub(r'_v\d+', '', src_dir.name))

fin_dir = pathlib.Path(final_path) / fin_name
if not fin_dir.exists():
    os.symlink(src_dir.as_posix(), fin_dir.as_posix())
    print('link created succ')
else:
    print('succ')
"""

node.parm('postrender').set(postrender_expr)
node.parm('lpostrender').set('python')

ptg.insertBefore((0,), r_btn)
ptg.insertAfter('lopoutput', note)
ptg.insertBefore('lopoutput', uname)
ptg.insertAfter((8,), t_btn)

# set all
node.setParmTemplateGroup(ptg)
