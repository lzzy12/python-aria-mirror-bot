from oauth2client.client import OAuth2WebServerFlow

# Why my "App isn't verified" ?
# This might returned by google APIs because we are using a high level scope here 
# How to fix it ?
# Just hit the continue anyway button because here you are using you own credentials so no one gonna steal your data
# else complete your developer/app profile and submit for review and get verified
# W4RR10R

__OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']
__REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

__CLIENT_ID = input("Enter the client id: ")
__CLIENT_SECRET = input("Enter the client secret: ")

flow = OAuth2WebServerFlow(
        __CLIENT_ID,
        __CLIENT_SECRET,
        __OAUTH_SCOPE,
        redirect_uri=__REDIRECT_URI
        )
auth_url = flow.step1_get_authorize_url()
print("Open this URL in any browser and get the refersh token: \n" + auth_url)
refresh_token = input("Enter the Refresh token: ")
auth = flow.step2_exchange(refresh_token).to_json()
print(auth)
