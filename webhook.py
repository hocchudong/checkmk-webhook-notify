#!/usr/bin/env python3
# Webhook Notify

import os
import sys
import requests
import json


# Get Tines WebHookURL from the environment variables and validate it
def GetPluginParams():
  env_vars = os.environ

  WebHookURL = str(env_vars.get("NOTIFY_PARAMETER_1"))

  # "None", if not in the environment variables
  if (WebHookURL == "None"):
          print("Tines-plugin: Mandatory first parameter is missing: Webhook URL")
          return 2, ""    # do not return anything, create final error

  return 0, WebHookURL


# Get the content of the message from the environment variables
def GetNotificationDetails():
  env_vars = os.environ
  print(env_vars)
  HOSTNAME = env_vars.get("NOTIFY_HOSTNAME")
  HOSTALIAS = env_vars.get("NOTIFY_HOSTALIAS")
  ADDRESS = env_vars.get("NOTIFY_HOSTADDRESS")
  SERVICE = env_vars.get("NOTIFY_SERVICEDESC")
  OUTPUT_HOST = env_vars.get("NOTIFY_HOSTOUTPUT")
  OUTPUT_SERVICE = env_vars.get("NOTIFY_SERVICEOUTPUT")
  LONG_OUTPUT_HOST = env_vars.get("NOTIFY_LONGHOSTOUTPUT")
  LONG_OUTPUT_SERVICE = env_vars.get("NOTIFY_LONGSERVICEOUTPUT")
  PERF_DATA = env_vars.get("NOTIFY_SERVICEPERFDATA")
  
  NOTIFY_SERVICESTATE = env_vars.get("NOTIFY_SERVICESTATE")
  NOTIFY_LASTSERVICESTATE = env_vars.get("NOTIFY_LASTSERVICESTATE")
  
  NOTIFY_HOSTSTATE = env_vars.get("NOTIFY_HOSTSTATE")
  NOTIFY_LASTHOSTSHORTSTATE = env_vars.get("NOTIFY_LASTHOSTSHORTSTATE")
  
  
  EVENT_HOST = f"{NOTIFY_HOSTSTATE} -> {NOTIFY_LASTHOSTSHORTSTATE}"
  EVENT_SERVICE = f"{NOTIFY_LASTSERVICESTATE} -> {NOTIFY_SERVICESTATE}"

  
  host_notify = {
    "Summary": f"CheckMK {HOSTNAME} - {EVENT_HOST}",
    "Host": HOSTNAME,
    "Alias": HOSTALIAS,
    "Address": ADDRESS,
    "Event": EVENT_HOST,
    "Output": OUTPUT_HOST,
    "LongOutput": LONG_OUTPUT_HOST
  }
  
  service_notify = {
    "Summary": f"CheckMK {HOSTNAME}/{SERVICE} {EVENT_SERVICE}",
    "Host": HOSTNAME,
    "Alias": HOSTALIAS,
    "Address": ADDRESS,
    "Service": SERVICE,
    "Event": EVENT_SERVICE,
    "Output": OUTPUT_SERVICE,
    "LongOutput": LONG_OUTPUT_SERVICE,
    "PerfData": PERF_DATA
  }
  
  what = env_vars.get("NOTIFY_WHAT")
  # Handy hosts or service differently
  if what == "SERVICE":
          notify = service_notify
  else:
          notify = host_notify


  return notify


# Send the message to Tines.io
def StartTinesWorkflow(WebHookURL, data):
  return_code = 0

  # Set header information
  headers = {
    'Content-Type': 'application/json'
  }

  try:
  # Make the POST request to start the workflow
    response = requests.post(WebHookURL, headers=headers, json=data)

  # Check the response status code
    if response.status_code == 200:
      print(f"Tines-plugin: Workflow started successfully.")
    else:
      print(f"Tines-plugin: Failed to start the workflow. Status code: {response.status_code}")
      print(response.text)
      return_code = 2
  except Exception as e:
    print(f"Tines-plugin: An error occurred: {e}")
    return_code = 2

  return return_code



def main():
        return_code, WebHookURL = GetPluginParams()

        if return_code != 0:
                return return_code   # Abort, if parameter for the webhook is missing

        data = GetNotificationDetails()

        return_code = StartTinesWorkflow(WebHookURL, data)

        return return_code


if __name__ == '__main__':
        sys.exit(main())
