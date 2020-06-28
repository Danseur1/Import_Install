#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:53:29 2020

@author: cws2
@Time-stamp: <2020-06-01 15:17:44 cws2>
"""

'''  New ideas:
    Ref: https://stackoverflow.com/questions/12332975/installing-python-module-within-code
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


install_and_import('transliterate')
---------------------

Ref: https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/

---------------------

'''

import sys
import subprocess

## Here add unusual install commands, use list if more than one command line is needed.

PipSpecialCases = { }

PipSpecialCases[ 'p2j'] = 'pip install git+https://github.com/remykarem/python2jupyter#egg=p2j'
PipSpecialCases[ 'pypulse'] = 'python -m pip install git+https://github.com/mtlam/PyPulse#egg=PyPulse'
PipSpecialCases[ 'saba'] = ['conda install -c sherpa sherpa', 'pip install saba']

PipSpecialCases[ 'pscTest'] = [ 'echo This is a test.', 'echo test', 'echo test.']

## PipInstallDict not currently used
PipInstallDict = { }
PipInstallDict[ 'pip'] = 'python -m pip install -U pip'
PipInstallDict[ 'scipy'] = 'python -m pip install --user scipy'
PipInstallDict[ 'matplotlib'] = 'python -m pip install --user matplotlib'
PipInstallDict[ 'ipython'] = 'python -m pip install --user ipython'
PipInstallDict[ 'jupyter'] = 'python -m pip install --user jupyter'
PipInstallDict[ 'pandas'] = 'python -m pip install --user pandas'
PipInstallDict[ 'sympy'] = 'python -m pip install --user sympy'
PipInstallDict[ 'nose'] = 'python -m pip install --user nose'
PipInstallDict[ 'numdifftools'] = 'python -m pip install --user numdifftools'
PipInstallDict[ 'pymc3'] = 'python -m pip install --user pymc3'
PipInstallDict[ 'statsmodels'] = 'python -m pip install --user statsmodels'
PipInstallDict[ 'astropy'] = 'python -m pip install --user astropy'
PipInstallDict[ 'seaborn'] = 'pip install seaborn'
PipInstallDict[ 'emcee'] = [ 'python -m pip install -U pip',
                             'pip install -U setuptools setuptools_scm pep517',
			     'pip install -U emcee']
PipInstallDict[ 'ptest'] = [ 'conda update conda', 'python -m pip install -U pip']

#-- special case:
PipInstallDict[ 'scipy+'] = 'python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose'


## CondaInstallDict is not currently used
CondaInstallDict = { }
CondaInstallDict[ 'pip'] = 'conda install pip'
CondaInstallDict[ 'sympy'] = 'conda install sympy'
CondaInstallDict[ 'astropy'] = 'conda install astropy'
CondaInstallDict[ 'matplotlib'] = 'conda install matplotlib'
CondaInstallDict[ 'pymc3'] = 'conda install -c conda-forge pymc3'
CondaInstallDict[ 'seaborn'] = 'conda install seaborn '
CondaInstallDict[ 'emcee'] = [ 'conda update conda',
                               'conda install -c conda-forge emcee']
CondaInstallDict[ 'ctest'] = [ 'conda update conda', 'python -m pip install -U pip']

## python -m pip install --upgrade pip
## conda update -n root conda
## conda update --all

## for linux:
##    apt-get -qq install python-cartopy python3-cartopy
##  See: https://colab.research.google.com/notebooks/snippets/importing_libraries.ipynb#scrollTo=Zq68DSY2rP2W

## Later: support install from git or multiple lines (mini-scripts).

## Ref: https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/
    
# def hasCmd( ckstr):
#     '''Check if cmd is installed by running 'ckstr' in shell.
#     Returns True if ckstr executed without error in shell,
#             False otherwise.
#     Typically used to see if 'conda' or 'emacs' is installed on system.
#     '''
#     from subprocess import PIPE, run
#     import sys
    
#     ## check if conda available
#     try: 
#         cmd = ckstr.split()
#         try:
#             result = run( cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True) 
#         except Exception:
#             return False
        
#         if verbose:
#             print( 'Command returned:\n{}'.format( result.stdout))
#         if result.returncode < 0: 
#             print("Child was terminated by signal", -result.returncode, file=sys.stderr) 
#             return False
#         else: 
#             if verbose:
#                 print("Child returned", result.returncode, file=sys.stderr) 
#             return True
#     except OSError as e: 
#         print("Execution failed:", e, file=sys.stderr) 
#         return False

    
# def runit( it):
#     '''run string or run elements of list sequencially.'''
#     from subprocess import run
    
#     if not isinstance( it, list):
#        run( it)
#     else:
#        for s in it:
#             run( s)      



verboseInstall = True ## turn on/off extra output

def call( cmd):
    '''Modeled after call function in NANOGrav Sprinng 2020 workshop.
    call() just executes the command in the shell and displays output,
    while runCatch( cmd) tries to catch all errors and output and only returns
    True of False to indicate success or failure.'''
    subprocess.call( cmd, shell=True)

def runCatch( it):
    '''Run string(s) from commandline.
    Returns True if no error was produced and False if an error was produced.'''
    
    if isinstance( it, list):
        cmdList = it
    else:
        cmdList = [ it]

    success = True  ## is set to False if any command fails.
    for cmd_i in cmdList:
        if verboseInstall:
            print( 'Trying to execute:\n{}'.format( cmd_i))
        try:
            cmds = cmd_i.split()
            returned = subprocess.Popen( cmds, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, universal_newlines=True)
            output, errors = returned.communicate()
            returncode = returned.returncode
            if verboseInstall:
                print(' Command line returned code {}.'.format( returncode))
                if len( errors) > 0:
                    print( "  stderr is:\n")
                    print( errors, '\n')
            if returncode == 0:
                success = True
            else:
                success = False
                            
        except Exception as e:
            if verboseInstall:
                print( e)
                success = False
    return success


# def runCatch0( it):
#     '''Run string from commandline.
#     Returns True if no error was produced and False if an error was produced.'''
    
#     if verboseInstall:
#         print( 'Trying to execute:\n{}'.format( it))
#     try:
#         cmds = it.split()
#         returned = subprocess.run( cmds, capture_output=True)
#         if verboseInstall:
#             print(' Command line returned code {}.'.format( returned.returncode))
#             if len( returned.stderr) > 0:
#                 print( "  stderr is:\n")
#                 print( returned.stderr, '\n')
#         if returned.returncode == 0:
#             return True
#         else:
#             return False
#     except Exception as e:
#         if verboseInstall:
#             print( e)
#         return False
    
# ## testing runCatch
# print( 'ls:\n', runCatch( 'ls'))
# print( 'pwd:\n', runCatch( 'pwd'))
# print( 'ssscc:\n', runCatch( 'ssscc'))  
# print( 'ls --fred:\n', runCatch( 'ls --fred'))
# print( 'ls -h:\n', runCatch( 'ls -h'))
# ## end runCatch testing 

def hasConda():
    '''returns True if running in Conda (if package conda is available).'''
    try:
        __import__( 'conda')
        return True
    except ImportError: 
        return False

def locatePythonPrefix():
    '''setup pyton executable path and condaprefix if conda is used.
    sets 'pythonExe' to path of python executable and 
    sets 'condaPrefix' to the prefix path or None if conda is not used.'''
    pythonExe = sys.executable
    if hasConda():
        condaPrefix = sys.prefix
    else:
        condaPrefix = None
    return pythonExe, condaPrefix

## testing locatePythonPrefix
##print( 'DBug locatePythonPrefix:', locatePythonPrefix())
    
# def tryLookupInstall( pkgname):
#     '''Try to install 'pkgname' using conda or pip.'''
#     if not hasConda():
#         if pkgname in PipInstallDict:
#             dictionary = PipInstallDict
#         else:
#             raise RuntimeError( '{} package install info is missing'.
#                                format( pkgname))
#     else:
#         if pkgname in CondaInstallDict:
#             dictionary = CondaInstallDict
#         elif pkgname in PipInstallDict:
#             dictionary = PipInstallDict
#         else:
#             raise RuntimeError( '{} package install info is missing'.
#                                format( pkgname))
#     try:
#       runit( dictionary[ pkgname] )
#     except OSError as inserr:
#       print( 'At 3')
#       print( 'Exception on trying to install {}'.format( pkgname))
#       print( 'Exception:', inserr)
#       raise inserr

## updating seems dangerous so it is disabled.
# def updatecp():
#     '''Try to update conda and pip'''
#     pythonExe, condaPrefix = locatePythonPrefix() ## get python executable, and conda prefix
#     if condaPrefix != None:
#         ## python -m pip install --upgrade pip
#         ## conda update -n root conda
#         ## conda update --all

#         ck = runCatch( 'conda update --yes -n root conda')
#         if not ck:
#             print( 'Problems with conda update.')
#         ck = runCatch( 'conda update --all --yes')
#         if not ck:
#             print( 'Problems with conda update --all.')

#     else:
#         ck = runCatch( pythonExe + ' -m pip install --update pip')
#         if not ck:
#             print( 'Problems with pip update.')
#     return ck

# ##print( 'DBug: update conda - pip, result: {}'.format( updatecp()))



##   Fix These:
## - Need to be able to specify the install name and the package name separately
##   example package: pint, install name: pint_pulsar

    
def import_install( pkgname, installname=None):
    '''Tries to import package in string in pkgname.
    If import fails, tries to install pkgname and then import.
    
    Warning, only use the base package.  For example:
       matplotlib = import_install( 'matplotlib')
       plt = matplotlib.pyplot
     should have similar result to
       import matplotlib as plt
     If the repository nume is different from the package name,
     specify that name as the second argument.  Ex:
         import_install( 'pint', 'pint_pulsar')
        '''
    if installname == None:
        installfromname = pkgname
    else:
        installfromname = installname
    
    try:
        pkg = __import__( pkgname)
        ##print( 'At 4')
        if verboseInstall:
            print( ' {} imported.'.format( pkgname))
        return pkg
    except ( ImportError, ModuleNotFoundError ) as exc:
        
        ## import failed, so now try to install
        pythonExe, condaPrefix = locatePythonPrefix() ## get python executable, and conda prefix

    ## first check if package is known special case
        if installfromname in PipSpecialCases:
            ck = runCatch( PipSpecialCases[ installfromname])
            if verboseInstall:
                print( 'runCatch returned {}'.format( ck))
            if ck:
                pkg = __import__( pkgname)
                if verboseInstall:
                    print( ' {} imported.'.format( pkgname))
                return pkg
            ## if special install fails, try other ways.

	## try installing from conda repository if conda is available
        if ( condaPrefix != None) and runCatch( 'conda install --yes --prefix ' +\
                                    condaPrefix + ' ' + installfromname):
            pkg = __import__( pkgname)
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            return pkg

	## try installing from conda-forge repository
        elif ( condaPrefix != None) and runCatch( 'conda install --yes --prefix ' +\
                                    condaPrefix + ' -c conda-forge ' + installfromname):
            pkg = __import__( pkgname)
            ##print( 'At 6')
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            return pkg

        ## try installing with pip
        elif runCatch( pythonExe + ' -m pip install ' + installfromname):
            pkg = __import__( pkgname)
            ##print( 'At 7')
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            return pkg
	
	## try installing with pip to user directory
        elif runCatch( pythonExe + ' -m pip install --user ' + installfromname):
            pkg = __import__( pkgname)
            ##print( 'At 7')
            if verboseInstall:
                print( ' {} imported.'.format( pkgname))
            return pkg
        
        else:   
            ##print( 'At 8')
            if verboseInstall:
                print( ' --> Problems importing or installing {}!'.format( pkgname))
            raise exc




## general import / install + import function
## Ref: https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/

# def import_install_( pkgname, installcmd=None, altinstallcmd=None):
#     '''Trys to import package specified in string in pkgname,
#     if import fails, uses installcmd as commandline statement(s) to try
#     to install the package and then trys again to import it.
#     If nether works, or if installcmd is None (default), then
#     attempts to install using 'usual' installs (conda and or pip).  If now of the
#     usual installs work, then raises and exception.
#     Returns pointer to imported package or raises exception if import/install
#     fails.
    
#     Usage:
#        matplotlib = import_install( 'matplotlib')
#        plt = matplotlib.pyplot
#      should have similar result to
#        import matplotlib as plt
#        '''

#     try:
#         pkg = __import__( pkgname)
#         print( 'DBug, {} imported.'.format( pkgname))
#         return pkg
    
#     except ImportError:
#         if installcmd != None:
#             print( 'DBug, Trying to install {} with cmd: {}.'.format( pkgname, installcmd))
#         if installcmd==None:  ## not specified, then try lookup of install info
#             print( 'Trying to install {} from built-in info.'.format( pkgname))
#             tryLookupInstall( pkgname)
#         else:
#             try:
#               subprocess.call( installcmd.split())
#             except OSError as inserr:
#               ##print ('{} does not exist'.format( installcmd))
#               print( 'Exception on trying to install {}'.format( pkgname))
#               print( 'Exception:', inserr)
    
#               ## try 2nd install command if not None
#               if altinstallcmd==None:
#                 raise inserr
#               else:
#                 try:
#                   subprocess.call( altinstallcmd.split())
#                 except OSError as inserr:
#                   ##print ('{} does not exist'.format( altinstallcmd))
#                   print( 'Exception on trying to install {} with alternate method.'.format( pkgname))
#                   print( 'Exception:', inserr)
#                   raise inserr
#         pkg = __import__( pkgname)
#         print( '{} imported after install.'.format( pkgname))

#     except Exception as e:
#         if verboseInstall:
#             print( ' --> Problems importing or installing {}!\n{}'.format( pkgname, e.message))
#             print( '     Exception: {}'.format( sys.exc_value))
#         raise e


   
if __name__ == "__main__":
    

    np = import_install( 'numpy')
    matplotlib = import_install( 'matplotlib')
    plt = matplotlib.pyplot
    ndt = import_install( 'numdifftools')
    pm3 = import_install( 'pymc3')
    statsmodels = import_install( 'statsmodels')
    astropy = import_install( 'astropy')
    pint = import_install( 'pint', 'pint-pulsar')
    np = import_install( 'numpy')
    emcee = import_install( 'emcee')
    easygui = import_install( 'easygui')
    passwordmeter = import_install( 'passwordmeter')
    zxcvbn = import_install( 'zxcvbn')
    pypulse = import_install( 'pypulse')
    wxpython = import_install( 'wx', 'wxpython')

    saba = import_install( 'saba')
    
    oops = import_install( 'pscTest')
    oops = import_install( 'fredricka')
        
 
