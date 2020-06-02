import argparse
import json
import os
import sys

from smb.SMBConnection import SMBConnection

TMP_FILE_PATH = "./tmp.json"

# Run this script using the following format
# poetry run python smb_store.py --arg1 value1 --arg2 value2 --argN valueN
parser = argparse.ArgumentParser(description="Store json file on SMB/CIFS remote file share.")
parser.add_argument("--username", required=True, help="SMB/CIFS network username.")
parser.add_argument("--password", required=True, help="SMB/CIFS network password.")
parser.add_argument("--client", required=True, help="The local NetBIOS machine name identifying the connection origin.")
parser.add_argument("--remote-server", required=True, help="The NetBIOS machine name of the remote server.")
parser.add_argument("--server-ip", required=True, help="IP address for the SMB/CIFS network file share.")
parser.add_argument("--dicom-results-json", required=True, help="Path to the output.json file.")
parser.add_argument("--smb-folder-name", required=True, help="Name of the shared folder.")
parser.add_argument("--smb-file-path", required=True, help="Path to the remote SMB/CIFS file storage.")
parser.add_argument("--use-ntlm-v2", default=True, help="NTLMv1 or NTLMv2 authentication algorithm for authentication.")
parser.add_argument("--is-direct-tcp", default=False, help="Default TCP/IP port is 139. Direct connection may use 443.")
parser.add_argument("--domain", default="", help="The network domain. On windows, it is known as the workgroup.")
parser.add_argument("--timeout", default=30, help="Time in seconds to wait for SMB connection.")
args = parser.parse_args()


def extract_smb_config(config_file):
    required_keywords = [
        "username", "password", "client", "remote_server", "server_name",
        "smb_folder_name", "smb_file_path", "timeout", "server_ip"
    ]

    with open(config_file) as json_file:
        smb_dict = json.load(json_file)
        valid_json = all(smb_dict[keyword] for keyword in required_keywords)
        if not valid_json:
            raise Exception("SMB config file is missing required parameters")

    return smb_dict


def generate_smb_json_drop(dicom_output_json, config_file):
    """
    :param dicom_output_json: Filepath to the output.json from rapid server
    :return: smb_json_file: File object containing selected fields from the output.json
    """
    with open(dicom_output_json) as json_file:
        data = json.load(json_file)
        patient_data = data.get("DICOMHeaderInfo") and data.get("DICOMHeaderInfo")["Patient"]
        if not patient_data:
            raise Exception("Invalid DICOMHeaderInfo property")
        if not data.get("Measurements"):
            raise Exception("Hemorrhage results not found.")

        smb_data = {
            "PatientId": patient_data.get("PatientID"),
            "AccessionNumber": patient_data.get("AccessionNumber"),
            "PatientName": patient_data.get("PatientName"),
            "HemorrhageSuspected": data["Measurements"]["HemorrhageDetected"],
        }

    with open(TMP_FILE_PATH, "wb") as smb_json_file:
        json.dump(smb_data, smb_json_file, indent=2)

    return smb_json_file


def main():
    print("Running SMB/CIFS storage script...")
    smb_config = extract_smb_config(args.smb_config_path)
    smb_file = generate_smb_json_drop(args.dicom_results_json)

    print("Performing NTLM authentication on '{server_name}'...".format(server_name=args.remote_server))
    smb = SMBConnection(
        username=args.username,
        password=args.password,
        my_name=args.client,
        remote_name=args.remote_server,
        domain=args.domain,
        use_ntlm_v2=args.use_ntlm_v2,
        is_direct_tcp=args.is_direct_tcp,
    )
    print("Successfully authenticated as '{username}'".format(username=args.username))

    port = 445 if args.is_direct_tcp else 139
    print("Connecting to network SMB share via {ip}:{port}...".format(ip=args.server_ip, port=port))
    smb.connect(ip=args.server_ip, timeout=args.timeout, port=port)
    print("Successfully connected to {ip}:{port}".format(ip=args.server_ip, port=port))

    print("Writing '{smb_file}' to '{folder}'...".format(smb_file=args.smb_file_path, folder=args.smb_folder_name))
    smb.storeFile(
        service_name=args.smb_folder_name,
        path=args.smb_file_path,
        file_obj=open(smb_file.name)
    )
    os.remove(TMP_FILE_PATH)
    print("Successfully stored '{json_file}' on '{server_name}' in '{shared_folder}'".format(
        json_file=args.smb_file_path,
        server_name=args.remote_server,
        shared_folder=args.smb_folder_name
    ))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("ERROR:", err)
        if os.path.exists(TMP_FILE_PATH):
            os.remove(TMP_FILE_PATH)
        sys.exit(1)
