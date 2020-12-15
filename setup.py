from cx_Freeze import setup, Executable

executables = [Executable('interface.py')]

setup(name='Video Analysis',
      version='2.0.0',
      description='Video objects recognize app',
      executables=executables)