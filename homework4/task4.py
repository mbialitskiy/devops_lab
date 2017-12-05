"""
This script is for checking the artifacts in nexus repository.
Credentials is stored in settings file in decrypted format.
Link to nexus is also stored in settings file.
"""

import ConfigParser
import base64
import json
import urllib2


class Nexus(object):

    nexus_url = "http://nexus"

    def __init__(self, repo_name):
        """Constructor for class. Initialize all variables """
        self.repo_name = repo_name
        self.repos_artifacts = []
        settings_list = self.read_settings('login', 'password', 'nexus_url')
        self.nexus_login, self.nexus_password, self.nexus_url = [item for item in settings_list]
        self.get_repo_artifacts()

    def __str__(self):
        """Pretty print artifacts from repository"""
        for item in self.repos_artifacts:
            print item
        return "Total artifacts found: {0}".format(len(self.repos_artifacts))

    def get_repo_artifacts(self, extension='war'):
        """Using Nexus API to get the list of artifacts"""
        request = urllib2.Request(str(Nexus.nexus_url) + "/service/siesta/rest/beta/search/assets?repository="
                                  + self.repo_name+"&maven.extension="+extension)
        request.add_header("Authorization", "Basic {0}".format(self.get_crypt_credentials()))
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError, e:
            if e.reason == 'Not Found':
                print "Sorry, no such repository"
            else:
                print "FAILED to handle request - "+str(e.reason)
        else:
            clear_json = result.read()
            result_json = json.loads(clear_json, encoding="UTF-8")
            if result_json['items']:
                for item in result_json['items']:
                    self.repos_artifacts.append(item['path'].split('/')[3:])
            else:
                print "No artifacts found for repository {0}.".format(self.repo_name)

    def read_settings(self, *args):
        """Read the needed info from settings file"""
        config = ConfigParser.ConfigParser()
        config.read("settings")
        items = []
        for item in args:
            items.append(config.get('main', str(item)))
        return items

    def get_crypt_credentials(self):
        """Crypt our credentials"""
        return str(base64.b64encode("{0}:{1}".format(base64.b64decode(self.nexus_login),
                                                     base64.b64decode(self.nexus_password))))


new_repo = Nexus(raw_input("Please, enter the name of repository:"))
if len(new_repo.repos_artifacts) == 0:
    while True:
        answer = raw_input("Do you want to change extension for search?(y|n) :")
        if answer == 'y':
            new_repo.get_repo_artifacts(raw_input("Please, enter the extension: "))
            break
        if answer == 'n':
            print "Bye!"
            exit(0)
print new_repo

