import os, sys, stat, shutil, getopt, time
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '4.5.2-dev'

toby_attributes = {"__version__": VERSION, "__installation_date__": time.asctime()}

with open(os.path.realpath(__file__).replace('setup.py', 'lib/jnpr/toby/__init__.py'), 'w') as init_file:
    [init_file.write("%s = '%s'\n" % (key, value)) for key,value in toby_attributes.items()]


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        install.run(self)

        # Copy Toby files to proper destination
        srcdir = self.install_lib + 'jnpr/toby/bin/'
        dstdir = '/usr/local/bin/'
        try:
            shutil.copytree("/volume/labtools/lib/Selenium/resources/firefoxprofile", self.install_lib + "/SeleniumLibrary/resources/firefoxprofile" )
        except OSError:
            pass
        try:
            for filename in os.listdir(srcdir):
                print(srcdir + filename)
                if (os.path.isfile(srcdir + filename)) and '__' not in filename :
                    try:
                        # This creates a symbolic link of toby in /usr/local/bin
                        os.remove(dstdir + filename)
                    except OSError:
                        pass
                    try:
                        shutil.copyfile( srcdir + filename, dstdir + filename)
                        #os.symlink(srcdir + filename, dstdir + filename)
                        os.chmod(dstdir + filename, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                    except OSError:
                        pass
        except OSError:
            pass


# parse requirements
req_lines = [line.strip() for line in open(
    'requirements.txt').readlines()]
install_reqs = list(filter(None, req_lines))


setup(
    name="Toby",
    namespace_packages=['jnpr'],
    version=VERSION,
    author="Sanjay kolar",
    author_email="toby-git@juniper.net",
    description=("Junos Python Framework to write test scripts"),
    license="Apache 2.0",
    keywords="Junos networking automation pyhton framework",
    url="https://git.juniper.net/toby-git/toby",
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    package_data={
        'jnpr.toby.hldcl.perl.lib': ['*.*'],
        'jnpr.toby.bin': ['*'],
        'jnpr.toby.hldcl.perl.lib.JT': ['*.pm'],
        'jnpr.toby.frameworkDefaults': ['*.yaml'],
        'jnpr.toby.hldcl.juniper': ['*.yaml'],
        'jnpr.toby.docs': ['*'],
        'jnpr.toby.engines.events': ['*.yaml'],
        'jnpr.toby.utils': ['*.xsl'],
        'jnpr.toby.init.attrib_init': ['*.yaml'],
        '':['*.robot']
    },
    install_requires=install_reqs,
    cmdclass={
        'install': CustomInstallCommand,
    },
    dependency_links=[
        'https://github.com/Juniper/py-junos-eznc#egg=junos_eznc-1.4.0.dev0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Text Processing :: Markup :: XML'
    ],
)
