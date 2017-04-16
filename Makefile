deploy_backend:
	git subtree push --prefix backend heroku master
	heroku config:add APP_TOKEN="$(shell cat backend/fb.token)"
	heroku ps:scale web=1
