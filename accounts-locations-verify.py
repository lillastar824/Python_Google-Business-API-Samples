#
#    Copyright 2019 Google LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        https://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import sys
import json

from googleapiclient import sample_tools
from googleapiclient.http import build_http

discovery_doc = "gmb_discovery.json"


def main(argv):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(
        argv,
        "mybusiness",
        "v4",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/business.manage",
        discovery_filename=discovery_doc)

    # Get the list of accounts the authenticated user has access to
    accountsList = service.accounts().list().execute()
    print("List of Accounts:\n")
    print(json.dumps(accountsList, indent=2) + "\n")

    # Choose one account to work with. Change index below as needed
    accInd = 9
    randomAccount = accountsList["accounts"][accInd]["name"]
    randomAccountName = accountsList["accounts"][accInd]["accountName"]

    # Get the list of locations for the first account in the list
    print("Choosing Account: " + randomAccountName)
    locationsList = service.accounts().locations().list(
        parent=randomAccount).execute()
    #print(json.dumps(locationsList, indent=2))
    print("Found " + str(len(locationsList["locations"])) + " locations")

    # Choose one location to work with. Change index below as needed
    locInd = 1
    randomLocation = locationsList["locations"][locInd]["name"]
    randomLocationName = locationsList["locations"][locInd]["locationName"]

    print("Choosing location: " + randomLocationName)

    verifyBody = {
        "method": "PHONE_CALL",
        "languageCode": "en",
        "phoneInput": {
            "phoneNumber": "+61 2 8084 6690"
        }
    }

    # Call verify
    output = service.accounts().locations().verify(name=randomLocation,
                                                   body=verifyBody).execute()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main(sys.argv)
