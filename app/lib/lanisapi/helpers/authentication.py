"""This script has various functions to log into Lanis."""
from time import time
from urllib.parse import urljoin

import re
import httpx
import machineid
from selectolax.parser import HTMLParser

from ..constants import LOGGER, URL
from .request import Request


def get_session_and_autologin(
    schoolid: str, username: str, password: str
) -> tuple[httpx.Cookies, str]:
    """Create new session (value: SPH-Session) at Lanis by posting to the login page and get Autologin cookie for the 30-days session.

    Note
    ----
    There are two login systems, the new one uses login.schulportal.hessen.de and the other
    one uses start.schulportal.hessen.de. This library currently supports only the new system.
    """
    params = {"i": schoolid}

    data = {
        "user2": username,
        "user": "{schoolid}.{username}".format(schoolid=schoolid, username=username),
        "password": password,
        "stayconnected": 1,
    }

    response = Request.post(URL.login, data=data, params=params)

    cookies = httpx.Cookies()
    cookies.set(
        "SPH-Session",
        response.headers.get("set-cookie").split(";")[0].split("=")[1],
        ".hessen.de",
        "/",
    )

    html = HTMLParser(response.content)

    # Get the <form> with id #registerBrowser to get the data for posting to /registerbrowser.
    registerbrowser_form = html.css_first(
        "#registerBrowser form[action='/registerbrowser']"
    )

    token = registerbrowser_form.css_first("input[name='token']").attributes.get(
        "value"
    )
    fingerprint = machineid.id()
    data = {
        "token": token,
        "url": "https://connect.schulportal.hessen.de/",
        "fg": fingerprint,
    }

    now = int(time())

    registerbrowser = Request.post(urljoin(URL.login, "registerbrowser"), data=data)

    # 1: Autologin token, 2: Timestamp when token expires
    autologin = [
        registerbrowser.headers["set-cookie"].split(";")[0].split("=")[1],
        now + int(registerbrowser.headers["set-cookie"].split(";")[2].split("=")[1]),
    ]

    return cookies, autologin


def get_session_by_autologin(schoolid: str, autologin: str) -> httpx.Cookies:
    """Create new session (value: SPH-Session) at Lanis by posting the autologin token to the login page.

    Note
    ----
    There are two login systems, the new one uses login.schulportal.hessen.de and the other
    one uses start.schulportal.hessen.de. This library currently supports only the new system.
    """
    params = {"i": schoolid}

    response = Request.post(
        URL.login, params=params, cookies=httpx.Cookies({"SPH-AutoLogin": autologin})
    )

    html = HTMLParser(response.content)

    # Get the <form> with id #registerBrowser to get the data for posting to /registerbrowser.
    registerbrowser_form = html.css_first("form[id='form']")

    token = registerbrowser_form.css_first("input[name='token']").attributes.get(
        "value"
    )
    fingerprint = machineid.id()  # Get an identifiable device id.
    data = {
        "token": token,
        "url": "",
        "fg": fingerprint,
    }

    # Get new session
    login_page_post = Request.post(
        URL.login,
        data=data,
        params=params,
        cookies=httpx.Cookies({"SPH-AutoLogin": autologin}),
    )

    cookies = httpx.Cookies()
    cookies.set(
        "SPH-Session",
        login_page_post.headers.get("set-cookie").split(";")[0].split("=")[1],
        ".hessen.de",
        "/",
    )

    return cookies


def get_session(
    schoolid: str,
    username: str,
    password: str,
) -> tuple[httpx.Cookies, str]:
    """Create new session (value: SPH-Session) at Lanis by posting to the login page.

    Note
    ----
    There are two login systems, the new one uses login.schulportal.hessen.de and the other
    one uses start.schulportal.hessen.de. This library currently supports only the new system.
    """
    params = {"i": schoolid}

    # `user2` = The username
    # `user` = The schoolid + username
    # `password` = The password
    # Idk why we need 2 usernames.
    data = {
        "user2": username,
        "user": "{schoolid}.{username}".format(schoolid=schoolid, username=username),
        "password": password,
    }

    response = Request.post(URL.login, data=data, params=params)

    cookies = httpx.Cookies()
    cookies.set(
        "SPH-Session",
        response.headers.get("set-cookie").split(";")[0].split("=")[1],
        ".hessen.de",
        "/",
    )

    # Link to the next page.
    location = response.headers.get("location")

    LOGGER.info("Authentication - Get session: Successfully created session.")

    return cookies, location


def get_authentication_url(cookies: httpx.Cookies) -> str:
    """Get the authentication url to get sid."""
    url = "https://connect.schulportal.hessen.de/"
    response = Request.head(url, cookies=cookies)

    # Link to the next (and final) page.
    authentication_url = response.headers.get("location")

    LOGGER.info("Authentication - Get url: Successfully got url.")

    return authentication_url


def get_authentication_sid(
    url: str,
    cookies: httpx.Cookies,
    schoolid: str,
) -> httpx.Cookies:
    """Get sid and return the 'final' cookies."""
    response = Request.head(url, cookies=cookies)

    cookies = httpx.Cookies()

    cookies.set("i", schoolid)
    print("set-cookie : ")
    print(response.headers.get("set-cookie"))
    
    # Hole alle Cookies aus dem Header
    set_cookie_header = response.headers.get("set-cookie")
    
    if set_cookie_header:
        # Regex, um "sid" und den alphanumerischen Wert zu extrahieren
        match = re.search(r'sid=([a-zA-Z0-9]+)', set_cookie_header)

        if match:
            sid_value = match.group(1)
            print(f"Der Wert von sid ist: {sid_value}")
        else:
            print("Kein sid-Wert gefunden.")

        print("sid : ")
        print(sid_value)

        # Setze den Cookie, falls 'sid' gefunden wurde
        if sid_value:
            cookies.set("sid", sid_value)
        else:
            print("sid-Cookie wurde nicht gefunden")
    else:
        print("Set-Cookie-Header ist leer oder nicht vorhanden")

    LOGGER.info("Authentication - Get sid: Success.")

    return cookies

