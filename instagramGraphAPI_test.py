import requests
import json

def getLongLiveToken(params):
    '''
    curl -i -X GET 
    https://graph.facebook.com/{graph-api-version}/oauth/access_token
    ?grant_type=fb_exchange_token
    &client_id={app-id}&client_secret={app-secret}
    &fb_exchange_token={your-access-token}
    '''
    endpointParams = dict()
    endpointParams['client_id'] = params['client_id']
    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = params['access_token']
    url = params['endpoint_base'] + 'oauth/access_token'
    return requests.get( url, endpointParams)

"""
def refreshLongLiveAccessToken(params):
    '''
    curl -i -X GET 
    "https://graph.instagram.com/refresh_access_token
    ?grant_type=ig_refresh_token
    &access_token={long-lived-access-token}"
    '''
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    endpointParams['grant_type'] = 'ig_refresh_token'
    url = params['endpoint_base'] + 'refresh_access_token'
    return requests.get( url, endpointParams)

def getUserNode(params):
    '''
    curl -X GET \
    'https://graph.instagram.com/{user-id}?fields=id,username&access_token={access-token}'`

    Alternate link
    curl -X GET \
    'https://graph.instagram.com/me?fields=id,username&access_token=IGQVJ...'
    
    '''
    endpointParams = dict()
    endpointParams['fields'] = 'id,username'
    endpointParams['access_token'] = params['access_token']
    url = params['endpoint_base'] + params['user_id']
    return requests.get(url, endpointParams)
"""

def getUserPages(params):
    '''
    curl -i -X GET \
    "https://graph.facebook.com/v10.0/me/accounts?access_token={access-token}"
    '''
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    url = params['endpoint_base'] + 'me/accounts'
    return requests.get(url, endpointParams)

def getBusinessAccount(params):
    '''
    curl -i -X GET \
    "https://graph.facebook.com/v10.0/134895793791914?fields=instagram_business_account&access_token={access-token}"
    '''
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    endpointParams['fields'] = 'instagram_business_account'
    url = params['endpoint_base'] + params['page_id']
    return requests.get( url, endpointParams)

def getUserMedia(params, ig_ac_id):
    '''
    curl -i -X GET \
    "https://graph.facebook.com/v10.0/17841405822304914/media?access_token={access-token}"
    '''
    endpointParams = dict()
    endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,comments_count,like_count,children{media_url,media_type,thumbnail_url},comments{username, timestamp,text, id}'
    endpointParams['access_token'] = params['access_token']
    url = params['endpoint_base'] + ig_ac_id + '/media'
        
    return requests.get( url, endpointParams)

def getCarouselAlbum(children, params):
    '''
    https://graph.facebook.com/v10.0/17895695668004550?fields=id,media_type,media_url,username,timestamp&access_token=IGQVJ...'
    '''
    data=dict()
    data['access_token']=params['access_token']
    data['fields']='media_url,media_type,thumbnail_url'
    response_list=list()
    for child in children['data']:
        url = params['endpoint_base'] + child['id']
        response=requests.get(url, data)
        link=json.loads(response.content)
        if link['media_type']=='IMAGE':
            response_list.append(link['media_url'])
        else:
            response_list.append(link['thumbnail_url'])
    return response_list

def businessDiscovery(params, username):
    '''
    curl -i -X GET \
    "https://graph.facebook.com/v3.2/17841405309211844?fields=business_discovery.username(bluebottle){followers_count,media_count}&access_token={access-token}"
    '''
    endpointParams = dict()
    endpointParams['fields'] = 'business_discovery.username(' + username + '){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{comments_count,like_count,caption,media_type,media_url,timestamp,children}}'
    endpointParams['access_token'] = params['access_token']
    url = params['endpoint_base'] + params['instagram_account_id']
    return requests.get( url, endpointParams)

def getURLById(params, media_id):
    data=dict()
    data['access_token']=params['access_token']
    data['fields']='media_url,thumbnail_url,media_type'
    url = params['endpoint_base'] + media_id
    response=requests.get(url, data)
    url_dict = json.loads(response.content)
    if url_dict['media_type']!='IMAGE':
        return url_dict['thumbnail_url']
    return url_dict['media_url']

def createMediaObject(params):
    '''
    POST graph.facebook.com/17841400008460056/media
    ?image_url=https//www.example.com/images/bronz-fonz.jpg
    &caption=%23BronzFonz
    '''
    url=params['endpoint_base']+params['instagram_account_id']+'/media'
    endpointParams=dict()
    endpointParams['caption']=params['caption']
    endpointParams['access_token']=params['access_token']
    try:
        endpointParams['user_tags']=params['user_tags']
    except:
        endpointParams['user_tags'] = None
    try:
        endpointParams['location_id'] = params['location_id']
    except:
        endpointParams['location_id'] = None
    if params['media_type']=='IMAGE':
        endpointParams['image_url']=params['media_url']
    else:
        endpointParams['media_type']=params['media_type']
        endpointParams['video_url']=params['media_url']
    
    return requests.post(url, endpointParams)

def publishMedia(params, creation_id):
    '''
    https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
    '''
    url=params['endpoint_base']+params['instagram_account_id']+'/media_publish'
    endpointParams=dict()
    endpointParams['creation_id']=creation_id
    endpointParams['access_token']=params['access_token']
    return requests.post(url, endpointParams)

def getMediaObjectStatus(creation_id, params):
    '''
    https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
    '''
    url=params['endpoint_base']+creation_id
    endpointParams=dict()
    endpointParams['fields']='status_code'
    endpointParams['access_token']=params['access_token']
    return requests.get(url, endpointParams)

def getLocationId(params, location):
    '''
    GET 
    https://graph.facebook.com/pages/search
    ?q=guggenheim
    &fields=name,location,link
    &access_token={access-token}
    '''
    url='https://graph.facebook.com/pages/search'
    endpointParams=dict()
    endpointParams['q']=location
    endpointParams['fields']='name,location,link'
    endpointParams['access_token']=params['access_token']
    return requests.get(url, endpointParams)


def getMediaInsights(params, media_id):
    """
	https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}


    if 'VIDEO' == response['json_data']['data'][0]['media_type'] : # media is a video
        params['metric'] = 'engagement,impressions,reach,saved,video_views'
    else : # media is an image
        params['metric'] = 'engagement,impressions,reach,saved'

	"""
    endpointParams = dict()
    endpointParams['metric'] = 'engagement,impressions,reach,saved'
    endpointParams['access_token'] = params['access_token']
    url = params['endpoint_base'] + media_id +'/insights'
    return requests.get( url, endpointParams)

def getUserInsights(params):
    """
	https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}

	"""
    endpointParams = dict()
    endpointParams['metric'] = 'follower_count,impressions,profile_views,reach'
    endpointParams['period'] = 'day'
    endpointParams['access_token'] = params['access_token']
    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'
    return requests.get( url, endpointParams)