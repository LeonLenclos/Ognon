"""Fichier d'installation d'Ognon"""

from cx_Freeze import setup, Executable


options = {"build_exe": {"excludes": ['Tcl']}}

setup(
    name="Ognon",
    version="0.1",
    description="Ognon est un logiciel d'animation 2d",
    options=options,
    executables=[Executable("ognon/ognon.py", base=None)]
)
