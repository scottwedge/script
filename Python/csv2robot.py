import csv
import sys
import os
import re
from shutil import copytree, ignore_patterns, copy
import xmltodict
from collections import OrderedDict
import shutil


def gen_dict(filename='', conf=False):
    case_num = 0
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if row[0] == 'Path' and row[1] == 'QAID':
                    continue
                case_num += 1
                gen_dir(dst_dir='/home/zcyang/tmp/testlink/conf', row=row, conf=True)
            print case_num
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


def gen_dir(dst_dir='/temp/testlink', row=list(), conf=True):
    path = dst_dir
    dirhie = row[0].strip('/').split('/')
    if conf is True:
        conf_dir = '%s/%s' % (dst_dir, 'conf')
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        for dir in dirhie:
            conf_dir = '%s/%s' % (conf_dir, dir)
    for name in dirhie[0:-1]:
        path = '%s/%s' % (path, name)
        print path,name
        if not os.path.exists(path):
            os.mkdir(path)
            open('%s/__init__.robot' % path, 'a').close() 
    dirhie[-1] = dirhie[-1].replace(':','_')
    if not os.path.exists('%s/%s.robot' % (path, dirhie[-1])):
        casefile = open('%s/%s.robot' % (path, dirhie[-1]), 'a')
        for string in ('*** Settings ***', 'Documentation\tScript Writer: '):
            casefile.write('%s\n' % string)
        map(lambda x: casefile.write('\t...\t\t%s\n' % x),
            ('Feature Name:',
             'Feature Description:',
             'Module Dev:',
             'Feature Dev:',
             'GUI Dev:',
             'Funtion Test:',
             'System Test:',
             'Auto Test:',
             'Version:',
             'Feature ID: '))
        for string in ('Suite Setup\t\tTest Suite Initial',
                       'Suite Teardown\t\tTest Suite TearDown',
                       'Resource\t\t_Resource_Files/common.robot',
                       '*** Test Cases ***'):
            casefile.write('%s\n' % string)
        casefile.close()

    rcasefile = open('%s/%s.robot' % (path, dirhie[-1]))
    content = rcasefile.read()
    casefile = open('%s/%s.robot' % (path, dirhie[-1]), 'a')
    # print row[1],row[1].isalnum(),content
    if row[1].isalnum() and not re.search(r'\b%s\n'%row[-1],content):
    # if row[1].isalnum() and '%s\n' % row[1] not in content:
        doc = row[2].split('\n')
        steps = map(lambda x: '\t...\t%s\n' % (x), doc[1:])
        for kw in ('    [Documentation]\t%s%s\n' % ('Summary: ', doc[0]), '%s\n' % row[1]):
            steps.insert(0, kw)
        steps.extend('    ...    Script Writer: \n')
        steps.extend('\n')
        #steps.extend('    [Tags]\t%s\tv5.3\n\n' % row[4],)
        case_content = ''.join(steps)
        if '\n*** Keywords ***' in content:
            wcasefile = open('%s/%s.robot' % (path, dirhie[-1]), 'w')
            kw_pos = content.find('*** Keywords ***')
            new_content = '%s%s%s' % (
                content[:kw_pos], case_content, content[kw_pos:])
            wcasefile.write(new_content)
            wcasefile.close()
        else: 
            casefile.write(case_content)
            casefile.close()
    rcasefile.close()


def copy_setting(src='', dst='', force=False):
    dst_dir = dst.strip('/').split('/')
    dst_path = dst_dir[0]
    for hie in dst_dir[1:-1]:
        dst_path = '%s/%s' % (dst_path, hie)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
    src_split = src.rsplit('/', 1)
    if dst_dir[-1] == src_split[-1] == 'all':
        copytree(src=src_split[0], dst=dst_path.replace(
            ' ', '_'), ignore=ignore_patterns('.svn'))
        return ''
    dst_filelist = gen_case_list(case_string=dst_dir[-1])
    src_filelist = gen_case_list(case_string=src_split[-1])
    if len(src_filelist) == len(dst_filelist):
        if force is True:
            for i in range(len(dst_filelist)):
                pre_src = src_filelist[i]
                pre_dst = dst_filelist[i]
                for subfix in range(10):
                    subname = '%s/%s-%d.robot' % (src_split[0], pre_src, subfix)
                    # print subname
                    if not os.path.exists(subname):
                        break
                    else:
                        rcontent = open(subname).read()
                        wcontent = open('%s/%s-%d.robot' %
                                        (dst_path, pre_dst, subfix), 'w')
                        wcontent.write(rcontent)
                        wcontent.close()
                src_basefile = '%s/%s.robot' % (src_split[0], src_filelist[i])
                if os.path.exists(src_basefile):
                    rcontent = open(src_basefile).read()
                    wcontent = open(
                        '%s/%s.robot' % (dst_path, dst_filelist[i]), 'w')
                    wcontent.write(rcontent)
                    wcontent.close()
        else:
            for i in range(len(dst_filelist)):
                pre_src = src_filelist[i]
                pre_dst = dst_filelist[i]
                for subfix in range(1, 10):
                    src_subname = '%s/%s-%d.robot' % (
                        src_split[0], pre_src, subfix)
                    dst_subname = '%s/%s-%d.robot' % (dst_path, pre_dst, subfix)
                    if not os.path.exists(src_subname):
                        break
                    if os.path.exists(src_subname) and not os.path.exists(dst_subname):
                        rcontent = open(src_subname).read()
                        wcontent = open(dst_subname, 'w')
                        wcontent.write(rcontent)
                        wcontent.close()
                src_basefile = '%s/%s.robot' % (src_split[0], src_filelist[i])
                if not os.path.exists('%s/%s.robot' % (dst_path, dst_filelist[i])) and os.path.exists(src_basefile):
                    rcontent = open('%s/%s.robot' %
                                    (src_split[0], src_filelist[i])).read()
                    wcontent = open(
                        '%s/%s.robot' % (dst_path, dst_filelist[i]), 'w')
                    wcontent.write(rcontent)
                    wcontent.close()
    else:
        raise ('can not 1 to 1 map for the src and dst file')


def create_dst_dir(dst='', case=False):
    dst_dir = dst.strip('/').split('/')
    dst_path = dst_dir[0]
    dstlist = dst_dir[1:-2] if case is True else dst_dir[1:-1]
    for hie in dstlist:
        dst_path = '%s/%s' % (dst_path, hie)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
    return dst_path


def gen_case_list(case_string=''):  # 1-3,23,25 =>[1,2,3,23,25]
    case_list = []
    for file in case_string.split(','):
        if file.find('-') != -1:
            temp = file.split('-')
            case_list = case_list + \
                [str(i) for i in range(int(temp[0]), int(temp[-1])+1)]
        else:
            case_list.append(file)
    return case_list


def case2dict(casefile=''):
    try:
        content = open(casefile).read()
    except IOError:
        raise "No file %s" % casefile
    module_name = re.findall(r'[\*]{3}[\w\s]+[\*]+', content)
    module = re.split(r'[\*]{3}[\w\s]+[\*]+', content)
    data = dict(zip(module_name, module[1:]))
    data[module_name[1]] = handle_cases(data[module_name[1]])
    # print data[module_name[1]]
    return data


def handle_cases(cases):
    caseid = re.findall(r'\n\d+\n', cases)
    case = re.split(r'\n\d+\n', cases)
    casedict = dict(zip(caseid, case[1:]))
    return casedict


def copy_case(src='', dst=''):
    '''
    1)src=/temp/testlink/a/b/all,dst=H:/a/b/all
    2)src=/temp/testlink/a/b/1,2,5-10,dst=H:/a/c/7,9,10-15
    3)src=/temp/testlink/a/b/1,2,5-10,dst=H:/a/c/

    '''
    srclist = src.rsplit('/', 2)
    dstlist = dst.rsplit('/', 2)
    src_casefile = '%s/%s.robot' % (srclist[0], srclist[1])
    dst_casefile = '%s/%s.robot' % (dstlist[0], dstlist[1])
    dst_path = ''
    if not os.path.exists(dst_casefile):
        dst_path = create_dst_dir(dst=dstlist, case=True)
    if srclist[-1] == dstlist[-1] == 'all':
        copy(src_casefile, dst_casefile)
        return ''
    else:
        pass


def _handle_suite_name(name):
    if re.search(r'[1-4]+$', name):
        return re.sub(r'(?<!40)[1-4]+$', r'', name)
    elif name == 'SLB':
        return '02_SLB'
    elif name=='Log':
        return '14_VDOM'
    elif name=='Firewall':
        return '05_Firewall'
    elif name.find(' '):
        return name.replace(' ', '_')
    else:
        return name


def _handle_suite(data, fd, path_list, level, exclude_dict):
    if isinstance(data, list):
        for d in data:
            if d.get('testcase'):
                if 'name' in d:
                    path_list.append(_handle_suite_name(d.get('name')))
                _handle_case(
                    d.get('testcase'), fd, path_list, level, exclude_dict)
                path_list.pop()
            if d.get('testsuite'):
                if 'name' in d:
                    path_list.append(_handle_suite_name(d.get('name')))
                _handle_suite(
                    d.get('testsuite'), fd, path_list, level, exclude_dict)
                path_list.pop()

    elif isinstance(data, dict):
        if data.get('testcase'):
            if 'name' in data:
                path_list.append(_handle_suite_name(data.get('name')))
            _handle_case(data['testcase'], fd, path_list, level, exclude_dict)
            path_list.pop()
        if data.get('testsuite'):
            if 'name' in data:
                path_list.append(_handle_suite_name(data.get('name')))
            _handle_suite(
                data['testsuite'], fd, path_list, level, exclude_dict)
            path_list.pop()
    else:
        pass


def _write_to_csv(fd, path, data):
    level_map={'1':'low','2':'medium','3':'high'}
    execution_map={'1':'manual','2':'automated'}
    level=level_map.get(data.get('importance'),'high')
    execution_type=execution_map.get(data.get('execution_type'),'1')
    # summary=re.sub(r'\<.*\>',r'',data.get('summary'))
    # print summary
    # print data.get('summary'),data.get('externalid')
    row = path, data.get('externalid').replace(
        'FortiADC-', ''), data.get('name').encode("ascii", "ignore"), '5.3', level,execution_type 
    fd.writerow(row)


def _handle_case(data, fd, path_list, level, exclude_dict):
    path = '/'.join(path_list)
    pathtxt = '%s.robot' % path.replace('\\', '/') 
    level=[str(i) for i in level] 
    # print pathtxt,pathtxt in exclude_dict
    if pathtxt in exclude_dict: 
        if isinstance(data, list):
            for x in data:
                # print x.get('externalid'),x.get('importance')
                #print x.get('importance', None) in level and x.get('externalid', None) not in exclude_dict[pathtxt],'-----'
                if x.get('importance', None) in level and x.get('externalid', None) not in exclude_dict[pathtxt]:
                    _write_to_csv(fd, '/'.join(path_list[1:]), x)
                # if x.get('importance', None) is None:
                #     print x.get('externalid', None),'--x'
        elif isinstance(data, dict):
            # print data.get('externalid'),data.get('importance')
            #print data.get('importance', None) in level and data.get('externalid', None) not in exclude_dict[pathtxt],'000'
            if data.get('importance', None) in level and data.get('externalid', None) not in exclude_dict[pathtxt]:
                _write_to_csv(fd, '/'.join(path_list[1:]), data)
        #     if data.get('importance', None) is None:
        #         print data.get('externalid', None),'--x'
        # else:
            pass
    else:
        if isinstance(data, list):
            for x in data:
                # print x.get('externalid'),x.get('importance')
                #print x.get('importance', None) in level,level,x.get('importance', None)
                if x.get('importance', None) in level:
                    _write_to_csv(fd, '/'.join(path_list[1:]), x)
                # else:
                #     print x.get('externalid', None),'--',x.get('importance', None)
        elif isinstance(data, dict):
            # print data.get('externalid'),data.get('importance')
            #print data.get('importance', None) in level
            if data.get('importance', None) in level:
                _write_to_csv(fd, '/'.join(path_list[1:]), data)
            # else:
            #     print x.get('externalid', None),'--',x.get('importance', None)
        else:
            pass


def xmltocsv(**args):
    src = args.get('src', '/temp/testlink/5.3.xml')
    dst = args.get('dst', src.replace('xml', 'csv'))
    level = args.get('level', ['1','2','3'])  # 0 high, 2 medium, 1 low
    exclude_dict = args.get('exclude_dict', {})
    exclude_prefix = args.get('exclude_prefix', None)
    casedict = xmltodict.parse(
        open(src), dict_constructor=OrderedDict, attr_prefix='')
    with open(dst, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        first_row = 'Path', 'QAID', 'Objective', 'Release', 'Priority'
        writer.writerow(first_row)
        path_list = [] if exclude_prefix is None else [exclude_prefix]
        _handle_suite(casedict, writer, path_list, level, exclude_dict)


def recurse_dirctory_1(dir='/temp/testlink', topdown=False):
    out = '' 
    for prefix, sub_path, filelist in os.walk(dir): 
        prefix = prefix.replace('\\', '/')
        print prefix
        for file in filelist:
            if file != '__init__.robot':
                out = '%s\n%s/%s' % (out, prefix, file)  
        sub_path[:] = [path for path in sub_path if path != '.svn'] 
        if sub_path:
            for path in sub_path:
                tmpout = recurse_dirctory('%s/%s' % (prefix, path), True)
                if tmpout:
                    out = '%s\n%s' % (out, tmpout)
    # print out
    return out


def recurse_dirctory(dir='H:/'):  
    global outlist
    outlist=[]
    if not os.path.exists(dir):
        return [] 
    for sub in os.listdir(dir):
        if sub=='.svn' or sub=='__init__.robot':continue
        path='%s/%s'%(dir,sub)
        if os.path.isdir(path): 
            # yield recurse_dirctory(path)
            outlist +=recurse_dirctory(path)
        else:
            if os.path.isfile(path): 
                # yield path 
                outlist.append(os.path.abspath(path))  
    return outlist

def test_generator(dir='H:/'):
    for sub in os.listdir(dir):
        if sub=='.svn' or sub=='__init__.robot':continue
        yield '%s/%s'%(dir,sub) 

def find_case_list(suite_name=''):
    with open(suite_name) as f:
        retlist = re.findall(r'\n\d+\r?\n', f.read(), re.DOTALL | re.MULTILINE)
        return [case.strip() for case in retlist]

def gen_case_list(base_dir='H:/',dst_dir='/temp/testlink/'): 
    ret=recurse_dirctory(dir=base_dir)
    for suite in ret.split('\n'): 
        if suite.endswith('.robot'):
            file_name=suite.replace(base_dir,'')
            file_name=file_name.replace('/','_')
            file_name=file_name.replace('.robot','') 
            with open('%s/%s.csv'%(dst_dir,file_name),'w') as f: 
                writer = csv.writer(f, lineterminator='\n')
                row='case_id', ''
                writer.writerow(row)
                for id in find_case_list(suite):
                    row=id, ''
                    writer.writerow(row)

def _edit_tags(base_dir):
    ret=recurse_dirctory(dir=base_dir) 
    suites=[]
    for suite in ret.split('\n'): 
        if not suite or suite in suites:continue  
        lines=[]
        suites.append(suite) 
        with open(suite) as f:
            flags=0 
            for line in f: 
                if re.search(r'^\d{1,4}$',line): 
                    flags=1 
                elif re.search(r'\[Tags\].*$',line) and flags==1: 
                    line='%s\t%s\n'%(line.rstrip(),'v4.5') 
                    flags=0  
                else:
                    if re.search(r'\[Tags\].*$',line): 
                        line='%s\t%s\n'%(line.rstrip(),'v5.3')
                lines.append(line) 
        with open(suite,'w') as writer: 
            for line in lines:
                writer.write(line) 

def file2dict(filename=''):
    with open(filename) as f:
        s_c_k=re.split(r'\*{3}.*?\*{3}',f.read())
    case=s_c_k[2]  
    case_id=re.findall(r'^\d+\n(?:.+\n)*\n?',case,re.M)
    if s_c_k[1]:
        wt=re.findall(r'(?<=Script Writer:)\s*\w*',s_c_k[1],re.M) 
    for case in case_id:
        yield _case2dict(case)

def _case2dict(case=''):  
    case_id,case=case.split('\n',1)
    case_dict=dict()  
    content=re.findall(r'(?:\s+\[\w+\].*\n(?:\s+\.+.*\n)*)|(?:    (?!\[).+\n)*',case,re.M) 
    for item in content:
        if item.strip().startswith('['):
            tmp=item.strip().split(']')
            case_dict.update({tmp[0].lstrip('['):tmp[1].strip()})
        else:
            if item.strip():  
                case_dict.update({'content':item.strip()})
    if case_dict.get('Documentation',None) is not None:
        wt=re.findall(r'(?<=Script Writer:)\s*\w*',case_dict.get('Documentation'),re.M)
        if wt[0]:
            case_dict.update({'Writer':wt[0]})
    case_dict=dict(zip([case_id.strip()],[case_dict]))  
    return case_dict


class case_handle(object):

    def __init__(self, **args):
        self._local_dir = args.get(
            'local_dir', '/home/zcyang/fortinet/FortiExtender/FortiExtender_Test/Regression_ALL/function_test')
        self._module = args.get('module', '22_SLB_SSL') 
        self._dir = recurse_dirctory(
            '%s/%s' % (self._local_dir, self._module)) 
        self.exclude_dict = dict() 

    def _task(self):
        for case_suite in self._dir:
            yield find_case_list('%s.robot' % case_suite)

    def gen_exclude(self):
        self._dir = [file.replace('\\','/') for file in self._dir if file]  
        for suite in self._dir:
            self.exclude_dict.update({suite: find_case_list(suite)})
        # print self.exclude_dict
        return self.exclude_dict

    def xml2csv(self, src, level=[1,2,3]):
        self.src=src
        xmltocsv(src=src, level=level, exclude_dict=self.exclude_dict,
                 exclude_prefix=self._local_dir)

    def gen_dict(self,csvfile=None):
        csvfile=csvfile if csvfile is not None else re.sub(r'\.xml$',r'.csv',self.src)
        print csvfile
        gen_dict(csvfile)


# for i in file2dict('H:/workspace/FortiADC_Robot/Current_Build/ADC_Test/03_Function_Test/02_SLB/02_SLBL7_HTTPS/07_Profile_HTTPS/16_local-cert-group.robot'): #03_Function_Test/02_SLB/02_SLBL7_HTTPS/07_Profile_HTTPS/16_local-cert-group.robot
#     pass 
# _case2dict()
# _edit_tags('H:/workspace/FortiADC_Robot/Current_Build/ADC_Test/03_Function_Test') 

# for i in test_generator(dir='H:/workspace/FortiADC_Robot/Current_Build/ADC_Test/03_Function_Test'):
#     print i

# for i in recurse_dirctory(dir='H:/workspace/FortiADC_Robot/Current_Build/ADC_Test/03_Function_Test'):
#     print i

# ret_dict={}
# for suite in ret.split('\n'): 
#     if suite.endswith('.robot'): 
#         ret_dict.update({suite:find_case_list(suite)})
# print ret_dict
# gen_case_list('H:/workspace/FortiADC_Robot/Current_Build/ADC_Test/03_Function_Test/06_Security')

caseexclude = case_handle(module='debug')
caseexclude.gen_exclude()
caseexclude.xml2csv(src='/home/zcyang/Downloads/single.xml', level=range(4))
caseexclude.gen_dict()

# xmltocsv('/temp/testlink/slb.xml')

# gen_dict('/temp/testlink/Firewall.csv')

# recurse_dirctory('H:\workspace\FortiADC_Robot\Current_Build\ADC_Test')




# find_case_list('H:/workspace/FortiADC_Robot/Current_Build/ADC_Test/03_Function_Test/22_SLB_SSL/22_SLB_SSL.robot')
# copy_setting('H:/workspace/FortiADC_Robot/Current_Build/Config_Template/43 New Features/1-to-1 NAT/764397-764405,764407-764410,764412,764415,764417','H:/workspace/FortiADC_Robot/Current_Build/Config_Template/03_Function_Test/05_Firewall/05_NAT/02_One_to_One_NAT/786981-786989,786991-786994,786996,786999,787001')
# copy_setting('H:/workspace/FortiADC_Robot/Current_Build/Config_Template/43 New Features/Authentication/all','H:/workspace/FortiADC_Robot/Current_Build/Config_Template/03_Function_Test/02_SLB/01_SLBL7_HTTP/12_AuthPolicy/all',)
# case2dict('/temp/testlink/data.robot')
# case2dict('/temp/testlink/data.robot')
