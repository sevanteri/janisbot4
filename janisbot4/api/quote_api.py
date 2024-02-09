from urllib.parse import quote as urlquote

import requests

from janisbot4.config import cfg

QUOTE_API_TOKEN = cfg.get("QUOTE_API_TOKEN")
QUOTE_API_URL = cfg.get("QUOTE_API_URL")

HEADERS = {"Authorization": QUOTE_API_TOKEN}

EMPTY_RESPONSE = "???"

REQUEST_TIMEOUT = 60


def quotelast(channel, quote, victim=None, adder=None):
    requests.post(
        f"{QUOTE_API_URL}/rpc/quotelast",
        headers=HEADERS,
        json={
            "a_channel": channel,
            "a_victim": victim,
            "a_adder": adder,
            "a_quote": quote,
        },
        timeout=REQUEST_TIMEOUT,
    )


def request(request_str):
    response = requests.get(f"{QUOTE_API_URL}/{request_str}", headers=HEADERS, timeout=REQUEST_TIMEOUT)
    return response.json()


def get_random_quote(arguments=None):
    argumentstr = _parse_include_exclude(arguments)
    req = "random_quotes?limit=1" + argumentstr
    response = request(req)
    return response[0].get("quote", EMPTY_RESPONSE) if len(response) > 0 else EMPTY_RESPONSE


def get_quote_metadata(quote):
    req = (
        "irc_quote?quote=eq."
        + urlquote(quote, safe="")
        + "&limit=1&select=user:user_id(name),adder:adder_id(name),channel:channel_id(name),timestamp"
    )
    response = request(req)

    return response[0] if len(response) > 0 else EMPTY_RESPONSE


def get_quote_count(user=None):
    req = "quote_count"
    if user:
        req = "quotes_per_user?limit=1&name=ilike." + urlquote(user, safe="")

    response = request(req)

    return response[0]["count"] if len(response) > 0 else EMPTY_RESPONSE


def _parse_include_exclude(arguments):
    return "" if not arguments else _parse_arguments([_parse_include_exclude_str(arg) for arg in arguments])


def _parse_include_exclude_str(argument):
    if argument.startswith("-"):
        return f"quote=not.ilike.*{urlquote(argument.lstrip('-'), safe='')}*"

    return f"quote=ilike.*{urlquote(argument, safe='')}*"


def _parse_arguments(arguments=None):
    return "&" + "&".join(arguments)
