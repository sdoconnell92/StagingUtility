# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\sean\\WorthSaving\\repos\\StagingUtility\\nsp_staging_utility\\guiapp.py'],
             pathex=['C:\\Users\\sean\\WorthSaving\\repos\\StagingUtility\\su_venv\\Scripts'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='guiapp',
          debug=False,
          strip=False,
          upx=True,
          console=False )
