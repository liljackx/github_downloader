from libs.Github import Github
from flask import Flask, request, send_file

app = Flask("gdown api")

@app.route('/repoDownload', methods=['GET'])
def repoDownload():
	# Requested paramaters: repo_name, path, token
	# Note: to use this software u need a valid access token from github

	print(request.args)

	access_token = request.args.get('token')
	repo = request.args.get('repo')
	path = request.args.get('path')

	git = Github(access_token)
	git.download(repo, path, '')
	path_name = path.split('/')[-1]
	return send_file('./{}.zip'.format(path_name))

if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)