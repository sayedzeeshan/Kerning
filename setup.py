from setuptools import setup, find_packages

setup(
  name = 'ligature_kerning',
  packages = find_packages(),
  version = '0.1.0',
  license='MIT',
  description = 'Nasteeq ligatures kerning for OpenType (TruType) Fonts',
  author = 'Sayed Zeeshan Asghar',
  author_email = 'sayedzeeshan@gmail.com',
  url = 'https://github.com/sayedzeeshan/Kerning',
  keywords = [
    'nastaliq',
    'kerning',
    'auto-kerning',
    'opentype',
    'fonts'
  ],
  install_requires=[
    'numpy >= 1.0',
    'matplotlib >= 1.0',
    'opencv-python >= 4.5.2.0'
  ],
  classifiers=[
    'Development Status :: 3 - Beta',
    'Intended Audience :: Users',
    'Topic :: Fonts :: Kerning',
    'License :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
