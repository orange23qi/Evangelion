# -*- coding: UTF-8 -*-
import gitlab
#import base64

from django.conf import settings


class gitLab(object):
    def __init__(self):
        self.branchName = 'test'
        self.projectId = 476
        try:
            self.gitUrl = getattr(settings, 'GIT_URL')
            self.privateToken = getattr(settings, 'GIT_PRIVATE_TOKEN')
        except AttributeError as a:
            print("Error: %s" % a)
        except ValueError as v:
            print("Error: %s" % v)
#        self.gitUrl = 'http://gitlab.1dmy.com'
#        self.privateToken = 'm-_z7wngsMAx-oi_T5q2'

    def getProjectName(self, projectName):
        """
        根据项目名称,获取gitlab中的项目ID
        """
        pageNum = 1
        projectId = 0

        gl = gitlab.Gitlab(self.gitUrl, self.privateToken)
        while pageNum < 10:
            projects = gl.projects.list(page=pageNum, per_page=50)
            for project in projects:
                if project.__dict__['name'] == projectName:
                    projectId = project.__dict__['id']
                    pageNum = 10
                    break
            pageNum += 1
        return projectId

    def uploadFile(self, serviceName, tableName, fileContent, commitMessage):
        """
        根据库名/表名,上传yaml文件
        """
        filePath = serviceName + '/MySQL/' + tableName + '.yaml'

        gl = gitlab.Gitlab(self.gitUrl, self.privateToken)
        gl.project_files.create({
                                    'file_path': filePath,
                                    'branch_name': self.branchName,
                                    'content': fileContent,
                                    'commit_message': commitMessage
                                }, project_id=self.projectId)

    def updateFile(self, serviceName, tableName, fileContent, commitMessage):
        """
        根据库名/表名,存在则更新yaml文件,没有则上传yaml文件
        """
        filePath = serviceName + '/MySQL/' + tableName + '.yaml'
        gl = gitlab.Gitlab(self.gitUrl, self.privateToken)
#       判断yaml文件是否存在
        try:
            f = gl.project_files.get(file_path=filePath,
                                     ref=self.branchName,
                                     project_id=self.projectId)
#       如果报错,表示文件不存在,从新上传一个yaml文件
        except Exception:
            self.uploadFile(serviceName, tableName, fileContent, commitMessage)
#       不报错则更新yaml文件
        else:
            f.content = fileContent
            f.save(branch_name=self.branchName,
                   commit_message=commitMessage,
                   encoding='utf8')
