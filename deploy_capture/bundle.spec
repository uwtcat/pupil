# -*- mode: python -*-


import platform

if platform.system() == 'Darwin':
    from version import dpkg_deb_version

    a = Analysis(['../pupil_src/capture/main.py'],
                 pathex=['../pupil_src/shared_modules/'],
                 hiddenimports=['pyglui.pyfontstash.fontstash','pyglui.cygl.shader','pyglui.cygl.utils'],
                 hookspath=None,
                 runtime_hooks=None)
    pyz = PYZ(a.pure)
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='pupil_capture',
              debug=False,
              strip=None,
              upx=False,
              console=False)

    #exclude system lib.
    libSystem = [bn for bn in a.binaries if 'libSystem.dylib' in bn]
    coll = COLLECT(exe,
                   a.binaries - libSystem,
                   a.zipfiles,
                   a.datas,
                   [('methods.so', '../pupil_src/shared_modules/c_methods/methods.so','BINARY')],
                   [('uvcc.so', '../pupil_src/shared_modules/uvc_capture/mac_video/uvcc.so','BINARY')],
                   [('libglfw3.dylib', '/usr/local/Cellar/glfw3/3.0.2/lib/libglfw3.dylib','BINARY')],
                   [('OpenSans-Regular.ttf','/usr/local/lib/python2.7/site-packages/pyglui/OpenSans-Regular.ttf','DATA')],
                   [('Roboto-Regular.ttf','/usr/local/lib/python2.7/site-packages/pyglui/Roboto-Regular.ttf','DATA')],
                   strip=None,
                   upx=True,
                   name='Pupil Capture')

    app = BUNDLE(coll,
                 name='Pupil Capture.app',
                 icon='pupil-capture.icns',
                 version = str(dpkg_deb_version()))


elif platform.system() == 'Linux':
    a = Analysis(['../pupil_src/capture/main.py'],
                 pathex=['../pupil_src/shared_modules/'],
                 hiddenimports=['pyglui.pyfontstash.fontstash','pyglui.cygl.shader','pyglui.cygl.utils'],
                 hookspath=None,
                 runtime_hooks=None)
    pyz = PYZ(a.pure)
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='pupil_capture',
              debug=False,
              strip=False,
              upx=True,
              console=True)

    coll = COLLECT(exe,
                   [b for b in a.binaries if not "libX" in b[0] and not "libxcb" in b[0]], # any libX file should be taken from distro else not protable between Ubuntu 12.04 and 14.04
                   a.zipfiles,
                   a.datas,
                   [('methods.so', '../pupil_src/shared_modules/c_methods/methods.so','BINARY')],
                   [('libglfw.so', '/usr/local/lib/libglfw.so','BINARY')],
                   [('libGLEW.so', '/usr/lib/x86_64-linux-gnu/libGLEW.so','BINARY')],
                   [('OpenSans-Regular.ttf','/usr/local/lib/python2.7/dist-packages/pyglui/OpenSans-Regular.ttf','DATA')],
                   [('Roboto-Regular.ttf','/usr/local/lib/python2.7/dist-packages/pyglui/Roboto-Regular.ttf','DATA')],
                   strip=True,
                   upx=True,
                   name='pupil_capture')

