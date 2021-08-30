echo off
:run
cls
start /b 
py -c "import source.ligature_kerning as lk; lk.generate_volt_outputs()"