#!/usr/bin/python

# Constructs python code containing common APIs
# example:  ./build_hltapi_common_lib_step2.py > hltapi_common.py

common_functions = {} 

file_obj = open("HLTAPI_method_comparison.tab")
for line in file_obj:
    line = line.rstrip()
    function, parameter, common = line.split('\t')
    if common == 'both':
        if function in common_functions:
            common_functions[function].append(parameter)
        else:
            parameters = []
            parameters.append(parameter)
            common_functions[function] = parameters

for function in common_functions:
    print('\ndef j_' + function + '(rt_handle,' + ','.join(common_functions[function]) + '):')
    print('    """')
    print('    :param rt_handle:       RT object')
    for parameter in common_functions[function]:
        print('    :param ' + parameter)
    print('    :return response from rt_handle.invoke(<parameters>)')
    print('    """')

    print('\n    args = dict()')
    for parameter in common_functions[function]:
        print('    args[\'' + parameter + '\'] = ' + parameter)

    print('    return rt_handle.invoke(\'' + function + '\', **args)')
     
        
