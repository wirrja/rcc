cisco = {
    'read_login': b'Username: ',
    'read_pass': b'Password',
    'root_cli': b'en\n',
    'nobreaks': b'terminal length 0\n',
    'show_conf': b'show run\n',
    'quit': b'exit\n',
    'waitfor': b'>'
}
huawei = {
    'read_login': b'Username:',
    'read_pass': b'Password:',
    'root_cli': None,
    'nobreaks': b'screen-length 0 temporary\n',
    'show_conf': b'dis cur\n',
    'quit': b'exit\n',
    'waitfor': b'>'
}
juniper = {
    'read_login': b'login:',
    'read_pass': b'Password:',
    'root_cli': None,
    'nobreaks': None,
    'show_conf': b'show configuration | no-more\n',
    'quit': b'quit\n',
    'waitfor': b'>'
}

