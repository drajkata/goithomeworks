from setuptools import find_namespace_packages, setup

setup(
    name='clean_folder',
      version='1',
      description='Homework2',
      url='https://github.com/drajkata/goithomeworks/blob/main/Homework1/homework1.py', #adres, gdzie można zostawić kod źródłowy
      author='Katarzyna Drajok',
      author_email='katarzyna.drajok@gmail.com',
      license='MIT',
      packages = find_namespace_packages(), # zestaw pakietów, które są uwzględnione w instalacji
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean']}
)