import os
import json
import googleapiclient.discovery
import pandas as pd
import s3fs
def ytetl():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "**************"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet,id,replies",
        maxResults=100,
        videoId="0qFxjJ1yrKo"
    )
    response = request.execute()
  
    comment = response.get('items', [])
  
# Create an empty list to store all comments
    allcomments = []
    snippet=[]
    for comment_item in comment:
      
    # Extract the nested "snippet" object from the comment
      snippet.append(comment_item.get('snippet'))
      
    #   innersnippet=snippet.get('snippet')
      for inner in snippet:
        #  insnippet=json.load(inner)
         insnippet=inner.get('topLevelComment', {}).get('snippet', {})
    # # Extract information from the snippet
        
         author_display_name=insnippet.get('authorDisplayName')
         Maintext=insnippet.get('textOriginal')
         Likecount=insnippet.get('likeCount')
         Publishat=insnippet.get('publishedAt')
    # # # # Create a dictionary to store the extracted information
         comment_info = {
         "Name": author_display_name,
         "Comment":Maintext,
         "Likes":Likecount,
         "PublishAt":Publishat
        # Add more fields as needed
        }
    
    # # # # Append the comment information to the list of all comments
         allcomments.append(comment_info)
      

# Print all comments
    Allcom=pd.DataFrame(allcomments)
    s3fs.S3File
    Allcom.to_csv("s3://ytairflow/youtube_comment.csv")



ytetl()

