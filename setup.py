from setuptools import setup, find_packages

setup(
    name='whatsapp-chat-reader',
    version='0.1.0',
    description='A Python project designed to read exported WhatsApp chat text files.',
    author='Yannick Sandermann',
    author_email='ysandermann@gmail.com',
    url='https://github.com/YanniSani/whatsapp-chat-reader.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        're',
        'enum',
        'typing'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)
