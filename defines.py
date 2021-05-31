def getCreds() :
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""

	creds = dict() # dictionary to hold everything
	creds['access_token'] = 'ACCESS-TOKEN' # access token for use with all api calls
	creds['client_id'] = 'CLIENT-ID' # client id (App ID) from facebook app
	creds['client_secret'] = 'CLIENT-SECRET' # client secret from facebook app
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v10.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['page_id'] = 'PAGE-ID' # users page id
	creds['instagram_account_id'] = 'INSTAGRAM-ACCOUNT-ID' # users instagram account id
	creds['ig_username'] = 'INSTAGRAM_USERNAME' # ig username

	return creds
