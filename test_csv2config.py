import csv2config
import pytest


def test_csv_import(tmpdir):
    p = tmpdir.join('test.csv')
    p.write('a,b\n'
            'c,d\n'
            'e,f\n')
    data = csv2config.csv_import(str(p))
    assert len(data) == 2
    assert data == [{'a': 'c', 'b': 'd'}, {'a': 'e', 'b': 'f'}]


def test_render_template(tmpdir):
    context = {
        'hostname': 'testnode',
        'logging_host': '1.1.1.1',
        'ip': '10.10.10.10',
        'mask': '255.255.255.0'
    }
    p = tmpdir.join('template.j2')
    p.write('!\n'
            'logging host {{ logging_host }}\n'
            'hostname {{ hostname }}\n'
            'int eth0\n'
            'ip address {{ ip }} {{ mask }}\n'
            '!')
    data = csv2config.render_template(str(p), [context])
    result = ('!\n'
              'logging host 1.1.1.1\n'
              'hostname testnode\n'
              'int eth0\n'
              'ip address 10.10.10.10 255.255.255.0\n'
              '!')
    assert data[0] == result


def test_write_file(tmpdir):
    text_list = ['hostname test1\n!', 'hostname test2\n!']
    tmpdir.chdir()
    csv2config.write_files(text_list)
    for i, text in list(enumerate(text_list, start=1)):
        f = tmpdir.join('file{:02d}.md'.format(i))
        assert f.read() == text
    assert len(tmpdir.listdir()) == len(text_list)
