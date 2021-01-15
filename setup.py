from setuptools import setup

setup(name='extraction',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['extraction'],
      include_package_data=True,
      package_data={'extraction': ['utils\*', 'Data\*', 'standford\*'], '': ['*.txt']},
      zip_safe=False)
