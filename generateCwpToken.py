#!/usr/bin/env python3
# generateCwpToken.py
import logging
import os
from typing import Tuple

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed for verify=False
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global Variables
tlUrl = os.environ.get("tlUrl")


def generateCwpToken(accessKey: str, accessSecret: str) -> Tuple[int, str]:
    """Generates an authentication token from access keys."""
    if not tlUrl:
        logging.error("tlUrl environment variable not set.")
        exit(1)
    authURL = f"{tlUrl}/api/v1/authenticate"

    headers = {
        "accept": "application/json; charset=UTF-8",
        "content-type": "application/json",
    }
    body = {"username": accessKey, "password": accessSecret}

    try:
        response = requests.post(
            authURL, headers=headers, json=body, timeout=60, verify=False
        )
        if response.status_code == 200:
            data = response.json()
            logging.debug("Authentication token acquired successfully.")
            return 200, data.get("token", "")
        else:
            logging.error(
                "Unable to acquire token. Status code: %s", response.status_code
            )
            return response.status_code, ""
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during authentication: {e}")
        return 500, ""


def checkParam(paramName: str) -> str:
    """Checks if a required environment variable is set."""
    paramValue = os.environ.get(paramName)
    if paramValue is None:
        logging.error(f"Missing required environment variable: {paramName}")
        raise ValueError(f"Missing {paramName}")
    return paramValue


def main():
    """Main execution function to generate and print a token."""
    try:
        P: Tuple[str, str] = ("pcIdentity", "pcSecret")
        (accessKey, accessSecret) = map(checkParam, P)
    except ValueError:
        exit(1)  # Exit if required params are missing

    # Authenticate and get token
    auth_status, cwpToken = generateCwpToken(accessKey, accessSecret)

    # Print the token and exit
    if auth_status == 200 and cwpToken:
        print(cwpToken)
        exit(0)  # Exit successfully
    else:
        logging.error("Could not generate token. Exiting.")
        exit(1)  # Exit with an error


if __name__ == "__main__":
    main()
