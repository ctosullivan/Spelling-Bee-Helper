import os

def test_sbsolve_command():
    '''
    Test if sbsolve command can be called without any errors
    #TODO - update test when command accepts correct format
    '''
    owd = os.getcwd()
    os.chdir('./src/wghelper/')
    exit_status = os.system("python3 command_line.py -s 'test'")
    os.chdir(owd)
    assert exit_status == 0