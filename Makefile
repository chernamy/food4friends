deploy_backend:
	git subtree push --prefix backend heroku master
	heroku config:add APP_TOKEN="$(cat backend/fb.token)"
	heroku ps:scale web=1
