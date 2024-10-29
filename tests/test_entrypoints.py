import os

def test_module_entrypoint():
    '''
    Test can package be run as a module wihout any errors
    '''
    owd = os.getcwd()
    os.chdir('./src/wghelper/')
    exit_status = os.system('python3 . --help')
    os.chdir(owd)
    assert exit_status == 0


def test_console_entrypoint():
    '''
    Test can package be run from command line entrypoint wihout any errors
    '''
    owd = os.getcwd()
    os.chdir('./src/wghelper/')
    exit_status = os.system('python3 command_line.py --help')
    os.chdir(owd)
    assert exit_status == 0