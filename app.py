from flask import Flask, render_template, request, redirect, url_for
from defines import getCreds
from instagramGraphAPI_test import getUserPages, getBusinessAccount, getUserMedia, getCarouselAlbum, businessDiscovery, getURLById, createMediaObject, publishMedia, getMediaObjectStatus, getLocationId, getMediaInsights, getUserInsights, getLongLiveToken
import json
import time

app=Flask(__name__)
@app.route("/")
def index():
    params = getCreds()
    response = getUserPages(params)
    data=dict()
    data['json_data'] = json.loads(response.content)
    return render_template("index.html", response=data['json_data']['data'], length=len(data['json_data']['data']))

@app.route("/getLongLiveToken")
def longLiveToken():
    params = getCreds()
    response = getLongLiveToken(params)
    data=dict()
    data['json_data'] = json.loads(response.content)
    return render_template("longLiveToken.html", response=data['json_data'])

@app.route("/getPages/")
def getPages():
    params = getCreds()
    response = getUserPages(params)
    data=dict()
    data['json_data'] = json.loads(response.content)
    return render_template("userPages.html", response=data['json_data']['data'], length=len(data['json_data']['data']))


@app.route("/getBusiness/")
def getAccount():
    params = getCreds()
    response = getBusinessAccount(params)
    data=dict()
    data['json_data'] = json.loads(response.content)
    return render_template("getBusinessAccount.html", response=data['json_data'])


@app.route("/media/")
def getMedia():
    params = getCreds()
    response = getUserMedia(params, params['instagram_account_id'])
    data=dict()
    data['json_data'] = json.loads(response.content)
    return render_template("getMedia.html", response=data['json_data']['data'], length=len(data['json_data']['data']))

@app.route("/businessDiscovery/")
def getUsername():
    return render_template("getUsername.html")

@app.route("/businessAccountData/", methods = ['GET', 'POST'])
def business_discovery():
    if request.method=='POST':
        username = request.form.get("username")
    else:
        return redirect(url_for("getUsername"))
    params = getCreds()
    response = businessDiscovery(params, username)
    data=dict()
    data['business_discovery'] = json.loads(response.content)
    length=len(data['business_discovery']['business_discovery']['media']['data'])
    for media in data['business_discovery']['business_discovery']['media']['data']:
        try:
            if media['media_type']=='CAROUSEL_ALBUM':
                for child in media['children']['data']:
                    child['media_url']=getURLById(params, child['id'])
            elif media['media_type']=='VIDEO':
                media['thumbnail_url']=getURLById(params, media['id'])
        except:
            media['thumbnail_url']='#'

    return render_template("businessDiscovery.html", response=data, length=length)

@app.route("/getPostData/")
def getPostData():
    return render_template("getPostData.html")

@app.route("/postImage/", methods = ['GET', 'POST'])
def postPhotos():
    if request.method=='POST':
        media_url = str(request.form.get("post_url"))
        usernames = str(request.form.get("user_tags"))
        location = str(request.form.get("location"))
        caption = str(request.form.get("caption"))
    else:
        return redirect(url_for('getPostData'))
    params = getCreds()
    response=list()
    
    locationResponse = getLocationId(params, location)
    locationData = json.loads(locationResponse.content)
    response.append(locationData)
    try:
        location_id = locationData['data'][0]['id']
        params['location_id']=location_id
    except:
        params['location_id'] = '7640348500'

    params['media_type'] = 'IMAGE'
    params['media_url'] = media_url
    params['caption'] = caption
    
    usernames = list(usernames.split())
    inc=1/len(usernames)
    x=inc-0.01
    y=inc-0.01
    user_tags=[]
    for username in usernames:
        user=dict()
        user['username']=username
        user['x']=round(x,1)
        user['y']=round(y,1)
        x+=inc
        y+=inc
        user_tags.append(user)

    user_tags = json.dumps(user_tags)
    params['user_tags']=user_tags
    imageMediaObjectResponse = createMediaObject( params )
    IG_Container = json.loads(imageMediaObjectResponse.content)
    response.append(IG_Container)
    creation_id=IG_Container['id']
    imageMediaStatus='IN_PROGRESS'

    while imageMediaStatus!='FINISHED':
        imageMediaStatusResponse=getMediaObjectStatus(creation_id, params)
        data = json.loads(imageMediaStatusResponse.content)
        imageMediaStatus = data['status_code']
        response.append(data)
        time.sleep(5)
    
    publishMediaResponse=publishMedia(params, creation_id)
    data=json.loads(publishMediaResponse.content)
    response.append(data)
    # return render_template("postImage.html", response=response)
    return redirect(url_for('getMedia'))

@app.route("/getMediaId/")
def getMediaId():
    return render_template("getMediaId.html")

@app.route("/getMediaInsights/", methods = ['GET', 'POST'])
def mediaInsights():
    '''
    if 'VIDEO' == response['json_data']['data'][0]['media_type'] : # media is a video
        params['metric'] = 'engagement,impressions,reach,saved,video_views'
    else : # media is an image
        params['metric'] = 'engagement,impressions,reach,saved'
    '''
    if request.method=='POST':
        media_id = request.form.get("media_id")
    else:
        return redirect(url_for('getMediaId'))
    params = getCreds()
    response = getMediaInsights(params, media_id)
    data=json.loads(response.content)
    return render_template("getMediaInsights.html", response=data)

@app.route("/getUserInsights/")
def userInsights():
    params = getCreds()
    response = getUserInsights(params)
    data=json.loads(response.content)
    return render_template("getUserInsights.html", response=data)
