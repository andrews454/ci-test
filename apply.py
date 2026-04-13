import json
import hmac
import hashlib
import os
import requests
from datetime import datetime, timezone


def submit_application():

    # Canonicalize payload
    json_payload = json.dumps({
        "action_run_link": os.environ.get('ACTION_RUN_LINK'),
        "email": os.environ.get('EMAIL'),
        "name": os.environ.get('FULLNAME'),
        "repository_link": os.environ.get('REPO_LINK'),
        "resume_link": os.environ.get('RESUME_LINK'),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    }, sort_keys=True, separators=(',', ':')).encode('utf-8')

    #Sign payload
    signature = hmac.new(
        os.environ.get('SIGNING_SECRET').encode('utf-8'),
        json_payload,
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}"
    }

    print("Submitting application ...")
    response = requests.post("https://b12.io/apply/submission", data=json_payload, headers=headers)

    if response.status_code == 200:
        receipt = response.json().get('receipt')
        print("\n" + "=" * 30)
        print("SUBMISSION SUCCESSFUL!")
        print(f"RECEIPT: {receipt}")
        print("=" * 30)
        print("Copy the receipt above into the B12 application form.")
    else:
        print(f"Submission failed with status: {response.status_code}")
        print(f"Response: {response.text}")


submit_application()