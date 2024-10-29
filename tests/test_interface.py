import os

def test_sbsolve_command():
    '''
    Test if sbsolve command can be called without any errors
    '''
    owd = os.getcwd()
    os.chdir('./src/wghelper/')
    exit_status = os.system("python3 command_line.py -s 'A BCDE'")
    os.chdir(owd)
    assert exit_status == 0

def test_sbhelper_command():
    '''
    Test if sbhelper command can be called without any errors
    '''
    owd = os.getcwd()
    os.chdir('./src/wghelper/')
    exit_status = os.system("python3 command_line.py -sh 'AB 5'")
    os.chdir(owd)
    assert exit_status == 0