from commands import getoutput
import json
import re
import os


def found_dirs_with_pyenv():
    users_dirs = os.listdir('/home/')
    users = []
    for user in users_dirs:
        if not os.path.exists('/home/'+str(user)+'/.pyenv'):
            print str(user) + ' - .pyenv not found'
        else:
            print "Pyenv for user \"" + str(user) + "\" found!"
            users.append(user)
    return users


def get_python_versions(list_of_pyenv_dirs):
    python_vers = {}
    for folder in list_of_pyenv_dirs:
        try:
            vers = os.popen('cd /home/'+folder+'/.pyenv/versions | ls -l ~/.pyenv/versions/ | grep -v ^l | cut -d" " -f9')\
                .read().strip('\n').split('\n')
        except IOError as e:
            print "Pyenv in folder " + str(folder) + " - " + e.message
        else:
            if len(vers) > 0:
                python_vers.update({folder: vers})
    return python_vers


def check_for_existance(ch_path, ch_item):
    if os.path.isfile("{0}{1}".format(ch_path, ch_item)):
        result = "{0}{1}".format(ch_path, ch_item)
    else:
        result = None
    return result


def get_site_packages(pip_path):
    site_packages_tmp = os.popen('{0} freeze'.format(pip_path)).read()
    site_packages = {}
    if site_packages_tmp:
        for package in site_packages_tmp.strip().split('\n'):
            site_packages.update({package.split('==')[0]: package.split('==')[1]})
    return site_packages


def get_vienv_params(user, version):
    wd = '/home/{0}/.pyenv/versions/{1}/envs/'.format(user, version)
    virt_params = {}
    virt_envs = os.listdir(wd)
    print "For version {0}, found virtual environments: {1}".format(version, virt_envs)
    for virt_env in virt_envs:
        pip_path = check_for_existance(wd+str(virt_env), '/bin/pip')
        pyton_path = check_for_existance(wd+str(virt_env), '/bin/python')
        if os.path.isdir(wd+str(virt_env)+'/lib/python'+version[:3]+'/site-packages'):
            site_pack_location = wd+str(virt_env)+'/lib/python'+version[:3]+'/site-packages'
        if pip_path:
            vienv_packages = get_site_packages(pip_path)
        virt_params.update({virt_env:
                                {'pip_path': pip_path,
                                 'python_path': pyton_path,
                                 'site-packages': site_pack_location,
                                 'packages': vienv_packages,
                                 }
                            })
    return virt_params


def get_info_about_version(user, version):
    wd = '/home/{0}/.pyenv/versions/{1}'.format(user, version)
    pip_path = check_for_existance(wd, '/bin/pip')
    python_path = check_for_existance(wd, '/bin/python')
    var_pp = os.popen('env | grep PYTHONPATH').read().replace('\n', '')
    version_packages = get_site_packages(pip_path)
    return {'pip_path': pip_path,
            'python_exec_path': python_path,
            '$PYTHONPATH': var_pp,
            'packages': version_packages,
            'virtual_envs': get_vienv_params(user, version)
            }


def get_system_python_info():
    if os.path.isfile('/usr/bin/python'):
            python_exec_path ='/usr/bin/python'
            search = re.search('\d.*', getoutput(python_exec_path + ' -V'))
            if search:
                python_version = search.group(0)
                if python_version:
                    where_is_python = getoutput('whereis {0}'.format(python_exec_path)).split()[1:]
                    if os.path.isfile('/usr/bin/pip'):
                        pip_path = '/usr/bin/pip'
                        sys_pip_packages = get_site_packages(pip_path)
                return {'version': python_version, 'python_local': where_is_python, 'site-packages' : sys_pip_packages }


my_pyvenv = found_dirs_with_pyenv()
versions = get_python_versions(my_pyvenv)
versions_plus_params = {}
for user in versions:
    temp_list = []
    for item in versions.values():
        for ver in item:
            item = {ver: get_info_about_version(user, ver)}
            temp_list.append(item)
    versions_plus_params.update({user: temp_list})
versions_plus_params.update({'system_python':get_system_python_info()})
try:
    json_file = file('python.json', 'w')
    json_file.write(json.dumps(versions_plus_params))
except Exception as e:
    print "ERROR writing to json - {0}".format(e.message)
else:
    json_file.close()

try:
    import yaml
except Exception as e:
    print "To export to yaml please install pyyaml lib"
else:
    yaml_file = file('python.yaml', 'w')
    yaml.dump(versions_plus_params, yaml_file, default_flow_style=False)
    yaml_file.close()
