import http.client, httplib2, os, random, sys, time, fnmatch, json
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from argparse import Namespace
from googleapiclient.errors import ResumableUploadError
#from MySQLOps import MySQLOps
from threading import Thread
import subprocess as s

httplib2.RETRIES = 1

#Tutorial Video
#sudo ./video_upload_partner_api.py --file="Wildlife_Sample_Video.mp4" --title="Danish Test Video" --description="Sample Video" --keywords="Tag1, Tag2" --OnBehalfOfContentOwner=fnbek7vfj3DxYLvMeK-TFQ --onBehalfOfContentOwnerChannel=UCvyEhyM9z1Xu0YiDokA_ciA

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = ( httplib2.HttpLib2Error, IOError, http.client.NotConnected,
        http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine, )

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
CLIENT_SECRETS_FILE = "client_secret.json" #'client_secret_3.json' "client_secret_345.json"
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload","https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/youtubepartner","https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the Developers Console
https://console.developers.google.com/
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
ONBEHALFOFCONTENTOWNER = ""
ONBEHALFOFCONTENTOWNERCHANNEL = ""

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print ("Uploading file...")
      status, response = insert_request.next_chunk()
      if 'id' in response:
        print ("Video id '%s' was successfully uploaded." % response['id'])
      else:
        exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                                             scope=YOUTUBE_UPLOAD_SCOPE,
                                                             message=MISSING_CLIENT_SECRETS_MESSAGE
                                                                )

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))



def initialize_upload(youtube, options):
        tags = None
        if options.keywords:
                tags = options.keywords.split(",")

        ONBEHALFOFCONTENTOWNER = options.OnBehalfOfContentOwner
        ONBEHALFOFCONTENTOWNERCHANNEL = options.onBehalfOfContentOwnerChannel
        body=dict(
        snippet=dict(
        title=options.title,
        description=options.description,
        tags=tags,
        categoryId=options.category,
        ),
        status=dict(
        privacyStatus=options.privacyStatus
        ),
        )


  # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
                        part=",".join(body.keys()),
                        body=body,
                        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True),
                        autoLevels=True,
                        onBehalfOfContentOwner= ONBEHALFOFCONTENTOWNER,
                        onBehalfOfContentOwnerChannel= ONBEHALFOFCONTENTOWNERCHANNEL
                   )

        resumable_upload(insert_request)



args = Namespace(
                    keywords="DAM Dummy Keyword", category=22, file='C:/Users/Mango050/Desktop/Trash/rabbit.mp4',
                    privacyStatus='private',
                    title='Danish Test Video', description="DAM: Edit Up Description Here",
                    onBehalfOfContentOwnerChannel='UCFQ3uL9suLcOFrUP2TRKlgQ',
                    OnBehalfOfContentOwner= 'knQcwg_dT1LbpjgKXILtRg',
                    logging_level='ERROR',
                    auth_host_name='localhost',
                    auth_host_port=[8080,8090],
                    noauth_local_webserver=False
                     )

youtube = get_authenticated_service(args)
initialize_upload( youtube, args )
