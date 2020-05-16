import os
import requests
from zipfile import ZipFile

class Github(object):

	def __init__(self, token):
		self.base_url = "https://api.github.com"
		self.token = token
		self.headers = {
			'Accept': 'application/vnd.github.v3+json',
			'Authorization': 'token {}'.format(token)
		}
		self.path = './downloads/'
		self.blacklist = [
			'__pycache__',
		]
		self.images_ext = ['png', 'jpg', 'jpeg']

	def _check_dir(self, dirname):
		return dirname in self.blacklist

	def _serialize_repo_content(self, content, path=''):
		for element in content:
			if element['type'] == 'file':
				#print('Downloading {}'.format(element['name']))
				curr_url = element['download_url']
				file_bytes = requests.get(curr_url).content
				#print(path+element['name'])
				self.zip_obj.writestr(path+element['name'], file_bytes)
				'''if element['name'].split('.')[1] not in self.images_ext:
					write_file = open(path+element['name'], 'w')
					write_file.write(file_bytes.decode())
				else:
					write_file = open(path+element['name'], 'wb')
					write_file.write(file_bytes)'''
			elif element['type'] == 'dir':
				if not self._check_dir(element['name']):
					#print('Entering dir {}'.format(element['name']))
					dir_url = element['_links']['self']
					curr_path = path + element['name'] + '/'
					self._serialize_repo_content(
						self._get_repo_folder(dir_url),
						path = curr_path
					)

	def authetication(self):
		return requests.get(self.base_url, headers=self.headers).json()

	def repos(self):
		repo_url = "https://api.github.com/repos/{owner}/{repo}"
		return requests.get(
			repo_url.format(
			owner='liljackx',
			repo='projects'
			),
			headers=self.headers
		).json()

	def _get_repo_folder(self, url):
		return requests.get(
				url,
				headers=self.headers,
			).json()

	def download(self, repo, path, username):
		zip_name = path.split('/')[-1]
		self.zip_obj = ZipFile('{}.zip'.format(zip_name), 'w')
		download_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
		contents = requests.get(
			download_url.format(
			owner=username,
			repo=repo,
			path=path
			),
			headers=self.headers,
		).json()

		self._serialize_repo_content(contents)
		self.zip_obj.close()

