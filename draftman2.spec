# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['draftman2.py'],
             pathex=['/home/att/git/draftman2'],
             binaries=[('draftman2_run', '.')],
             datas=[
              ('draftman2.glade', '.'),
              ('icon/draftman2.png', 'icon'),
              ('icon/draftman2_sm.png', 'icon'),
              ('icon/file.svg', 'icon'),
              ('icon/directory.svg', 'icon'),
              ('icon/trash.svg', 'icon'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

#a.datas += Tree('./Draftman2 Tutorial', prefix='Draftman2 Tutorial')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='draftman2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='draftman2')
