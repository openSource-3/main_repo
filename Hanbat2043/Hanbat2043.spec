# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Hanbat2043.py'],
             pathex=[],
             binaries=[],
             datas=[('image_file/', 'image_file/'),  # 이미지 폴더
                            ('sound_file/', 'sound_file/'),  # 소리 폴더
                            ('public/', 'public/'),         # 다른 리소스 폴더
                            ('ending_part/', 'ending_part/'),
                            ('event_story/', 'event_story/'),
                            ('group_task/', 'group_task/'),
                            ('reaction/', 'reaction/'),
                            ('routine/', 'routine/'),
                            ('ChangwonDangamAsac-Bold_0712.ttf', '.'),  # ttf 파일 추가
                            ('GowunBatang-Bold.ttf', '.'),  # ttf 파일 추가
                            ('GowunBatang-Regular.ttf', '.'),  # ttf 파일 추가
                            ('H2GPRM.TTF', '.'),  # ttf 파일 추가
                            ('progress_icon.png', '.'),  # 이미지 파일 추가
                            ('main_menu.kv', '.'),  # kv 파일 추가
                            ('ending_screen.kv', '.'),  # kv 파일 추가
                            ('malgunbd.ttf', '.'),
                            ('C:/SWproject/Hanbat2043/NanumGothic.ttf', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Hanbat2043',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
icon='Hanbat2043.ico' )