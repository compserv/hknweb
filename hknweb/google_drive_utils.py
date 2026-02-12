from functools import wraps
import google.oauth2.service_account as service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from django.core.exceptions import ImproperlyConfigured


from pathlib import Path
import os
import json

# Thank you Brian Yu as much of this code and framework is taken from his work on the google calendar

# Alter the path to a server environment path


def get_credentials():  # pragma: no cover
    """
    Gets the google drive service account's credentials from the server.
    Should not be called anywhere else.

    Returns:
        google.oauth2.service_acount.Credentials
    """
    SCOPE = ["https://www.googleapis.com/auth/drive"]

    CRED = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_CREDS")
    if not CRED:
        raise RuntimeError("Google Drive Service Accounts Creds not found")

    creds = service_account.Credentials.from_service_account_file(CRED, scopes=SCOPE)

    return creds


def check_credentials_wrapper(fn):
    @wraps(fn)
    def new_fn(*args, **kwargs):
        get_credentials()
        return fn(*args, **kwargs)

    return new_fn


@check_credentials_wrapper
def get_service():  # pragma: no cover
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    return service


def create_metadata(
    name: str,
    mimeType: str,
    parents: list,
    description: str,
) -> dict:
    data = dict()
    data["name"] = name
    data["mimeType"] = mimeType

    if description is not None:
        data["description"] = description

    if parents is not None:
        data["parents"] = parents

    return data


def create_folder(
    name: str,
    parents: list = None,
    description: str = None,
) -> dict:  # pragma: no cover
    folder_resource = create_metadata(
        name=name,
        mimeType="application/vnd.google-apps.folder",
        description=description,
        parents=parents,
    )

    try:
        folder = (
            get_service()
            .files()
            .create(body=folder_resource, fields="id", supportsAllDrives=True)
            .execute()
        )

        return {"status": True, "result": folder["id"]}
    except HttpError as e:
        if e.resp.status == 403:
            return {
                "status": False,
                "result": "Service Account: Insufficent Permissions",
            }
        else:
            raise


def create_pdf(
    name: str,
    file,
    parents: list = None,
    description: str = None,
) -> dict:  # pragma: no cover
    pdf_resource = create_metadata(
        name=name,
        mimeType="application/pdf",
        description=description,
        parents=parents,
    )

    try:
        file.seek(0)

        media = MediaIoBaseUpload(file, mimetype="application/pdf")

        pdf = (
            get_service()
            .files()
            .create(
                body=pdf_resource, media_body=media, fields="id", supportsAllDrives=True
            )
            .execute()
        )

        return {"status": True, "result": pdf["id"]}
    except HttpError as e:
        if e.resp.status == 403:
            return {
                "status": False,
                "result": "Service Account: Insufficient Permissions",
            }
        else:
            raise


def create_permission(
    fileID: str,
    typeID: str,
    role: str,
    emailAddress: str = None,
    domain: str = None,
) -> dict:  # pragma: no cover
    body = {
        "type": typeID,
        "role": role,
    }
    if typeID in ["user", "group"]:
        if not emailAddress:
            raise ValueError(
                "Email Address required for 'user' and 'group' permissions"
            )
        body["emailAddress"] = emailAddress
    elif typeID == "domain":
        if not domain:
            raise ValueError("Domain required for 'domain' permissions")
        body["domain"] = domain
        body["allowFileDiscovery"] = False
    elif typeID == "anyone":
        body["allowFileDiscovery"] = False

    try:
        permission = (
            get_service()
            .permissions()
            .create(fileId=fileID, body=body, fields="id", supportsAllDrives=True)
            .execute()
        )
        return {"status": True, "id": permission["id"]}
    except HttpError as e:
        if e.resp.status == 403:
            return {"status": False}
        else:
            raise


def delete_permission(
    fileID: str, typeID: str, role: str, emailAddress: str = None, domain: str = None
) -> dict:  # pragma: no cover
    permissionID = get_permission_id(fileID, typeID, role, emailAddress, domain)
    if not permissionID:
        return {"status": False, "result": "No permission found"}
    try:
        deletion = (
            get_service()
            .permissions()
            .delete(fileId=fileID, permissionId=permissionID, supportsAllDrives=True)
            .execute()
        )
        return {"status": True}
    except HttpError as e:
        if e.resp.status == 403:
            return {
                "status": False,
                "result": "Service Account: Insufficent Permissions",
            }
        else:
            raise


def update_permission(
    fileID: str,
    typeID: str,
    role: str,
    new_role: str,
    emailAddress: str = None,
    domain: str = None,
) -> dict:  # pragma: no cover
    permissionID = get_permission_id(fileID, typeID, role, emailAddress, domain)
    if not permissionID:
        return {"status": False, "result": "No permission found"}
    try:
        update = (
            get_service()
            .permissions()
            .update(
                fileId=fileID,
                permissionId=permissionID,
                supportsAllDrives=True,
                body={"role": new_role},
            )
            .execute()
        )
        return {"status": True}
    except HttpError as e:
        if e.resp.status == 403:
            return {
                "status": False,
                "result": "Service Account: Insufficent Permissions",
            }
        else:
            raise


def get_permission_id(
    fileID: str, typeID: str, role: str, emailAddress: str = None, domain: str = None
) -> str:  # pragma: no cover
    permissions = (
        get_service()
        .permissions()
        .list(
            fileId=fileID,
            fields="permissions(id,type,role,emailAddress,domain)",
            supportsAllDrives=True,
        )
        .execute()
        .get("permissions", [])
    )

    for p in permissions:
        if p["type"] != typeID:
            continue
        if p["role"] != role:
            continue
        if typeID in ["user", "group"] and p["emailAddress"] != emailAddress:
            continue
        if typeID == "domain" and p["domain"] != domain:
            continue
        return p["id"]
    return None


def get_files(folderID: str, mimeType: str = None) -> str:  # pragma: no cover
    query = f"'{folderID}' in parents and trashed = false"

    if mimeType:
        query += f" and mimeType = '{mimeType}'"

    files = (
        get_service()
        .files()
        .list(
            q=query,
            fields="files(id, name, mimeType)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            spaces="drive",
        )
        .execute()
    )

    return files.get("files", [])
