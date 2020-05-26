'''
This module is designed to provide a reader for Toby documentation
It supports both man page style markup and text.
To add man pages, just ensure that they end in a '.1'
To add any other kind of text, then leave off an extenstion
'''
import os
import sys


def reader(target):
    '''
    This reader can handle both man pages and regular txt files
    Simply put a '.1' extension on man pages and leave extensions
    off of regular text files
    '''

    target = target.replace(' ', '_')
    #if target is 'topics', just show list of possible targets
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if target in ['topics', 'list']:
        print("Help Topics:")
        for fname in os.listdir(dir_path):
            if os.path.isfile(dir_path + '/' + fname) and '.py' not in fname:
                fname = fname.replace('_', ' ')
                fname = fname.replace('.1', '')
                print('  ' + fname)
        print("\n")
        return

    #set target file and path and ensure file exists
    fname = dir_path + '/' + target
    if os.path.isfile(fname + '.1'):
        os.system("man " + dir_path + "/" + target + '.1')
    elif os.path.isfile(fname):
        editor = None
        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
        if editor == 'vim':
            os.system("vim -M " + dir_path + "/" + target)
        elif editor == 'emacs':
            os.system("emacs " + dir_path + "/" + target + " --eval '(setq buffer-read-only t)'")
        else:
            os.system("vim -M " + dir_path + "/" + target)
    else:
        target = target.replace('_', ' ')
        print("No help available for " + target)
        sys.exit(1)
