def parser_the_great():
    xmlfile = open('xmlagain', 'r', encoding='UTF-8')
    ymlfile = open('yamlfriday.yml', 'w+', encoding='UTF-8')
    xmllines = xmlfile.readlines()
    tab_counter = 0
    for line in xmllines:
        cur_line = line
        if 'xml version' in cur_line:
            continue

        while len(cur_line) != 0:
            if ' ' in cur_line[:1]:
                cur_line = cur_line[1:]

            elif ('\n' or '\t') in cur_line[:1]:
                cur_line = cur_line[1:]

            elif '</' in cur_line[:2]:
                tab_counter -= 1
                end = cur_line.find('>')
                cur_line = cur_line[end + 1:]

            elif cur_line[0] == '<':
                tab_counter += 1
                end = cur_line.find('>')
                if not ('</' in cur_line):
                    ymlfile.write(tab_counter * '   ' + cur_line[1:end] + ':' + '\n')
                else:
                    ymlfile.write(tab_counter * '   ' + cur_line[1:end] + ':')

                cur_line = cur_line[end + 1:]
            elif ('\n' or '\t' or ' ') in cur_line[:1]:
                cur_line = cur_line[1:]
            else:
                if '<' in cur_line:
                    end = cur_line.find('<')
                    ymlfile.write(' ' + "'" + cur_line[:end] + "'" + "\n")
                    cur_line = cur_line[end:]
    xmlfile.close()
    ymlfile.close()
    with open('yamlfriday.yml', 'r') as file:
        greg = file.readlines()
        for i in range(len(greg)):
            for j in range(i + 1, len(greg) - 1):
                if greg[i] == greg[j]:
                    g = greg[i]
                    gf = g.find(':')
                    g = g[:gf]
                    while g[:1] == ' ':
                        g = g[1:]
                    greg[j] = greg[j].replace(g, g + '1')
        file.close()
    with open('yamlfriday.yml', 'w') as save_changes:
        save_changes.writelines(greg)
        save_changes.close()


def using_libraries():
    import xmlplain
    xmlin = open('xmlagain', 'r', encoding='UTF-8')
    root = xmlplain.xml_to_obj(xmlin, strip_space=True, fold_dict=True)
    yamlout = open('libyaml', 'w', encoding='UTF-8')
    xmlplain.obj_to_yaml(root, yamlout)


def usingRE():
    import re
    xmlfile = open('xmlagain', 'r', encoding='UTF-8')
    ymlfile = open('trymere', 'w', encoding='UTF-8')
    xmllines = xmlfile.readlines()
    tab_counter = 0
    for line in xmllines:
        greg = line
        if 'xml version' in greg:
            continue
        head_counter = 0
        open_key_sample = '<\w+>'
        result_sample = '>.*<'
        close_key_sample = '</\w+>'
        open_check = re.findall(open_key_sample, greg)
        result_check = re.findall(result_sample, greg)
        close_check = re.findall(close_key_sample, greg)
        if (len(open_check) != 0) and (len(close_check) == 0):
            open_check[0] = open_check[0].strip('>')
            open_check[0] = open_check[0].strip('<')
            list = ''.join(open_check) + ':'
            tab_counter += 1
            head_counter += 1
            if head_counter >= 1:
                ymlfile.write(tab_counter * ' ' + '-' + ' ' + list + '\n')
            else:
                ymlfile.write(tab_counter * ' ' + list + '\n')
        elif (len(open_check) != 0) and (len(close_check) != 0):
            open_check[0] = open_check[0].strip('>')
            open_check[0] = open_check[0].strip('<')
            result_check[0] = result_check[0].strip('>')
            result_check[len(result_check) - 1] = result_check[len(result_check) - 1].strip('<')
            open_list = ''.join(open_check)
            result_list = ' '.join(result_check)
            ymlfile.write(tab_counter * '  ' + open_list + ':' + ' ' + '"' + result_list + '"' + '\n')
        elif (len(open_check) == 0) and (len(close_check) != 0):
            tab_counter -= 1

import time

time_wl = time.time()
for i in range(10):
    parser_the_great()
time_wl = time_wl - time.time()

time_l = time.time()
for j in range(10):
    using_libraries()
time_l = time_l - time.time()

time_re = time.time()
for k in range(10):
    usingRE()
time_re = time_re - time.time()

print('Время исполнения без библиотек:', abs(time_wl))
print('Время исполнения с библиотеками:', abs(time_l))
print('Время исполнения с регулярными выражениями:', abs(time_re))
