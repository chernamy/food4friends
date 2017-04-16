deploy_backend:
	git subtree push --prefix backend heroku master
	heroku config:add APP_TOKEN="$(shell cat backend/fb.token)"
	heroku config:add DB_AUTH="$(shell cat backend/db.token)"
	heroku ps:scale web=1
