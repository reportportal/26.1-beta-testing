#!/usr/bin/env python3
"""Generate and replay Stream A / Stream B Postman collections against ReportPortal.

Collections are generated from catalog.py (the source of truth). Replay substitutes
{{variables}}, captures item UUIDs from Postman test scripts, injects nested steps
and realistic logs, then triages failed items (PB / AB / SI; TI is left unclassified).

Usage:
    python3 rp_stream_upload.py --generate
    python3 rp_stream_upload.py stream-a-cancellations-mobile.postman_collection.json
    python3 rp_stream_upload.py stream-b-booking-nfr.postman_collection.json --reset
    python3 rp_stream_upload.py --all

RP_PROJECT / --project is the organization slug only (the part before the dot).
The script appends the stream project: Stream A -> {org}.stream-a, Stream B -> {org}.stream-b.
"""

from __future__ import annotations

import argparse
import datetime
import json
import mimetypes
import os
import re
import sys
import time
import uuid
import zlib
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SCRIPT_DIR / "fixtures"
sys.path.insert(0, str(SCRIPT_DIR))

from catalog import STREAMS, cases_for_suite, issue_for  # noqa: E402


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


# ---------------------------------------------------------------------------
# Durations
# ---------------------------------------------------------------------------

def _crc(text: str) -> int:
    return zlib.crc32(text.encode("utf-8"))


def planned_duration(case: dict) -> float:
    if case.get("quick"):
        base = 8 + _crc(case["id"]) % 13
    else:
        base = 25 + _crc(case["id"]) % 36
    if case["status"] == "failed":
        base += 30 + _crc(case["id"]) % 16
    return base * (0.92 + (_crc(case["id"]) % 17) / 100)


# ---------------------------------------------------------------------------
# Postman collection generator
# ---------------------------------------------------------------------------

def _event(listen: str, lines: list[str]) -> dict:
    return {"listen": listen, "script": {"exec": lines, "type": "text/javascript"}}


def _bearer() -> dict:
    return {"type": "bearer", "bearer": [{"key": "token", "value": "{{token}}", "type": "string"}]}


def _url(raw: str, path: list[str]) -> dict:
    return {"raw": raw, "host": ["{{url}}"], "path": path}


def _pm_item(name: str, method: str, url_raw: str, path: list[str], *,
             raw: str | None = None, prerequest: list[str] | None = None,
             test: list[str] | None = None) -> dict:
    item = {
        "name": name,
        "event": [],
        "request": {
            "auth": _bearer(),
            "method": method,
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": _url(url_raw, path),
        },
        "response": [],
    }
    if prerequest is not None:
        item["event"].append(_event("prerequest", prerequest))
    if test is not None:
        item["event"].append(_event("test", test))
    if raw is not None:
        item["request"]["body"] = {"mode": "raw", "raw": raw}
    return item


def _start_capture(var: str, status: int = 201) -> list[str]:
    return [
        "let jsonData = pm.response.json();",
        f'pm.environment.set("{var}", jsonData.id);',
        "",
        f'pm.test("Status code is {status}", function () {{',
        f"    pm.response.to.have.status({status});",
        "});",
    ]


def _status_ok(code: int = 200) -> list[str]:
    return [
        f'    pm.test("Status code is {code}", function () {{',
        f"    pm.response.to.have.status({code});",
        "    });",
    ]


def _item_attributes(case: dict, stream_key: str) -> list[dict]:
    attrs = [
        {"key": "priority", "value": case["priority"]},
        {"key": "area", "value": case["area"]},
        {"key": "type", "value": case["case_type"]},
        {"key": "author", "value": case["author"]},
        {"key": "stream", "value": stream_key},
    ]
    for tag in case["tags"]:
        attrs.append({"value": tag})
    return attrs


def generate_collection(stream: dict) -> dict:
    items = [
        _pm_item(
            "Generate token",
            "POST",
            "{{host}}/uat/sso/oauth/token",
            ["uat", "sso", "oauth", "token"],
            test=[
                "let jsonData = pm.response.json();",
                'pm.environment.set("token", jsonData.access_token);',
            ],
        ),
        _pm_item(
            "Start launch",
            "POST",
            "{{url}}/{{project}}/launch",
            ["{{project}}", "launch"],
            prerequest=['pm.environment.set("date", new Date());'],
            test=_start_capture("current_launch_uuid"),
            raw=json.dumps({
                "description": stream["launch_description"],
                "name": stream["launch_name"],
                "startTime": "{{date}}",
                "mode": "DEFAULT",
                "rerun": False,
                "attributes": stream["attributes"],
            }, indent=2),
        ),
    ]

    for suite in stream["suites"]:
        items.append(_pm_item(
            f"Start Suite: {suite['name']}",
            "POST",
            "{{url}}/{{project}}/item",
            ["{{project}}", "item"],
            prerequest=['pm.environment.set("date", new Date());'],
            test=_start_capture("current_suite_uuid"),
            raw=json.dumps({
                "description": suite["description"],
                "launchUuid": "{{current_launch_uuid}}",
                "name": suite["name"],
                "startTime": "{{date}}",
                "type": "SUITE",
                "attributes": [
                    {"key": "tms-folder", "value": str(suite["folder_id"])},
                    {"key": "stream", "value": stream["key"]},
                ],
            }, indent=2),
        ))

        for case in cases_for_suite(stream, suite["name"]):
            items.append(_pm_item(
                f"Start {case['id']}",
                "POST",
                "{{url}}/{{project}}/item/{{current_suite_uuid}}",
                ["{{project}}", "item", "{{current_suite_uuid}}"],
                prerequest=['pm.environment.set("date", new Date());'],
                test=_start_capture("current_step_uuid"),
                raw=json.dumps({
                    "description": case["description"],
                    "launchUuid": "{{current_launch_uuid}}",
                    "name": case["name"],
                    "startTime": "{{date}}",
                    "type": "STEP",
                    "retry": False,
                    "testCaseId": case["id"],
                    "codeRef": case["code_ref"],
                    "attributes": _item_attributes(case, stream["key"]),
                }, indent=2),
            ))
            items.append(_pm_item(
                f"Info log for {case['id']}",
                "POST",
                "{{url}}/{{project}}/log",
                ["{{project}}", "log"],
                prerequest=['pm.environment.set("date", new Date());'],
                test=_start_capture("current_log_id"),
                raw=json.dumps({
                    "launchUuid": "{{current_launch_uuid}}",
                    "itemUuid": "{{current_step_uuid}}",
                    "time": "{{date}}",
                    "level": "info",
                    "message": f"placeholder log for {case['id']} (replaced on replay)",
                }, indent=2),
            ))
            finish_body: dict = {
                "endTime": "{{date}}",
                "status": case["status"],
                "launchUuid": "{{current_launch_uuid}}",
            }
            if case["status"] == "failed":
                finish_body["issue"] = {
                    "autoAnalyzed": False,
                    "comment": "",
                    "ignoreAnalyzer": False,
                    "issueType": "ti001",
                }
            items.append(_pm_item(
                f"Finish {case['id']}",
                "PUT",
                "{{url}}/{{project}}/item/{{current_step_uuid}}",
                ["{{project}}", "item", "{{current_step_uuid}}"],
                prerequest=['pm.environment.set("datePlus", new Date().getTime()+6000);'],
                test=_status_ok(200),
                raw=json.dumps(finish_body, indent=2),
            ))

        items.append(_pm_item(
            f"Finish Suite: {suite['name']}",
            "PUT",
            "{{url}}/{{project}}/item/{{current_suite_uuid}}",
            ["{{project}}", "item", "{{current_suite_uuid}}"],
            prerequest=['pm.environment.set("date", new Date());'],
            test=_status_ok(200),
            raw=json.dumps({
                "endTime": "{{date}}",
                "launchUuid": "{{current_launch_uuid}}",
            }, indent=2),
        ))

    items.append(_pm_item(
        "Finish launch",
        "PUT",
        "{{url}}/{{project}}/launch/{{current_launch_uuid}}/finish",
        ["{{project}}", "launch", "{{current_launch_uuid}}", "finish"],
        prerequest=['pm.environment.set("datePlus", new Date().getTime()+6000);'],
        test=_status_ok(200),
        raw=json.dumps({"endTime": "{{datePlus}}"}, indent=2),
    ))

    return {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": stream["collection_name"],
            "description": stream["launch_description"],
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items,
    }


def write_collections(target_dir: Path | None = None) -> list[Path]:
    target_dir = target_dir or SCRIPT_DIR
    written = []
    for stream in STREAMS.values():
        path = target_dir / stream["collection_file"]
        path.write_text(json.dumps(generate_collection(stream), indent=2) + "\n")
        written.append(path)
        print(f"Wrote {path.name} ({len(stream['cases'])} cases)")
    return written


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------

class VirtualClock:
    def __init__(self, start_epoch: float):
        self.t = start_epoch

    def advance(self, seconds: float) -> None:
        self.t += seconds

    def advance_to(self, epoch: float) -> None:
        self.t = max(self.t, epoch)


CLOCK = VirtualClock(time.time())


def set_clock(start_epoch: float) -> None:
    global CLOCK
    CLOCK = VirtualClock(start_epoch)


def iso_now() -> str:
    dt = datetime.datetime.fromtimestamp(CLOCK.t, datetime.timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


class ScriptEmulator:
    SET_RE = re.compile(r'pm\.environment\.set\(\s*"([^"]+)"\s*,\s*(.+?)\s*\)\s*;?\s*$')
    LET_RE = re.compile(r'let\s+(\w+)\s*=\s*jsonData\.(\w+)\s*;?\s*$')
    TEST_RE = re.compile(r"Status code is (\d+)")

    def __init__(self, env: dict):
        self.env = env

    def run(self, exec_lines: list[str], response_json: dict | None = None) -> None:
        js_vars = {}
        for line in exec_lines:
            line = line.strip()
            if line.startswith("//"):
                continue
            m = self.LET_RE.match(line)
            if m and response_json is not None:
                js_vars[m.group(1)] = response_json.get(m.group(2))
                continue
            m = self.SET_RE.search(line)
            if not m:
                continue
            name, expr = m.group(1), m.group(2)
            if expr == "new Date()":
                value = iso_now()
            elif expr.startswith("new Date().getTime()"):
                offset = re.search(r"\+\s*(\d+)", expr)
                value = int(CLOCK.t * 1000) + (int(offset.group(1)) if offset else 0)
            elif expr in js_vars:
                value = js_vars[expr]
            elif expr.startswith("jsonData.") and response_json is not None:
                value = response_json.get(expr[len("jsonData."):])
            else:
                value = expr.strip('"')
            if value is not None:
                self.env[name] = value

    def expected_status(self, exec_lines: list[str]) -> int | None:
        m = self.TEST_RE.search("\n".join(exec_lines))
        return int(m.group(1)) if m else None


class CollectionReplayer:
    VAR_RE = re.compile(r"\{\{(\w+)\}\}")

    def __init__(self, url: str, project: str, api_key: str, attachments_dir: Path,
                 stream: dict, launch_overrides: dict | None = None):
        self.env = {"url": f"{url.rstrip('/')}/api/v1", "project": project}
        self.attachments_dir = attachments_dir
        self.stream = stream
        self.launch_overrides = launch_overrides or {}
        self.planned = {c["id"]: c for c in stream["cases"]}
        self.custom_logged_items: set[str] = set()
        self.item_records: dict[str, dict] = {}
        self._pending_case: dict | None = None
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {api_key}"
        self.emulator = ScriptEmulator(self.env)

    def substitute(self, text: str) -> str:
        return self.VAR_RE.sub(lambda m: str(self.env.get(m.group(1), m.group(0))), text)

    def _scripts(self, item: dict, listen: str) -> list[str]:
        return [line
                for ev in item.get("event", [])
                if ev.get("listen") == listen
                for line in ev.get("script", {}).get("exec", [])]

    def _resolve_file(self, src: str) -> Path:
        name = Path(src).name
        for folder in (self.attachments_dir, FIXTURES_DIR, SCRIPT_DIR):
            local = folder / name
            if local.is_file():
                return local
        sys.exit(f"Attachment not found: {name} (referenced as {src})")

    def replay_request(self, item: dict) -> None:
        name = item["name"]
        request = item["request"]
        url = self.substitute(request["url"]["raw"])

        if "oauth/token" in url:
            print(f"  ~ {name}: skipped (using API key instead)")
            return

        self.emulator.run(self._scripts(item, "prerequest"))
        url = self.substitute(request["url"]["raw"])
        method = request["method"]
        body = request.get("body", {})

        if method == "POST" and url.rstrip("/").endswith("/log") and body.get("mode") == "raw":
            raw_log = self.substitute(body["raw"])
            if any(item_uuid in raw_log for item_uuid in self.custom_logged_items):
                print(f"  ~ {name}: skipped (replaced by catalog logs)")
                return

        if method == "PUT" and "/launch/" in url and url.rstrip("/").endswith("/finish"):
            if len(self.item_records) != len(self.planned):
                sys.exit(f"PLAN GUARD: only {len(self.item_records)} of {len(self.planned)} "
                         "planned test items started. Aborting before launch finish.")

        kwargs: dict = {}
        open_files = []
        try:
            if body.get("mode") == "raw":
                raw = self.substitute(body["raw"])
                if method == "POST" and url.rstrip("/").endswith("/launch") and self.launch_overrides:
                    payload = json.loads(raw)
                    payload.update(self.launch_overrides)
                    raw = json.dumps(payload)
                elif method == "POST":
                    raw = self._rewrite_item_start(raw)
                elif method == "PUT":
                    raw = self._rewrite_item_finish(url, raw)
                kwargs["data"] = raw.encode("utf-8")
                kwargs["headers"] = {"Content-Type": "application/json"}
            elif body.get("mode") == "formdata":
                files = []
                for part in body["formdata"]:
                    if part.get("disabled"):
                        continue
                    if part.get("type") == "file":
                        path = self._resolve_file(part["src"])
                        content_type = (mimetypes.guess_type(path.name)[0]
                                        or "application/octet-stream")
                        handle = path.open("rb")
                        open_files.append(handle)
                        files.append((part["key"], (path.name, handle, content_type)))
                    else:
                        files.append((part["key"], (None,
                                                    self.substitute(part["value"]),
                                                    part.get("contentType") or None)))
                kwargs["files"] = files

            response = self.session.request(method, url, **kwargs)
        finally:
            for handle in open_files:
                handle.close()

        expected = self.emulator.expected_status(self._scripts(item, "test"))
        if expected is not None and response.status_code != expected:
            sys.exit(f"ERROR on '{name}': expected {expected}, got {response.status_code}\n"
                     f"{method} {url}\n{response.text}")
        if expected is None and not response.ok:
            sys.exit(f"ERROR on '{name}': {response.status_code}\n{method} {url}\n{response.text}")

        try:
            response_json = response.json()
        except ValueError:
            response_json = None
        self.emulator.run(self._scripts(item, "test"), response_json)
        print(f"  ✓ {name} [{response.status_code}]")

        if method == "PUT" and "/launch/" in url and url.rstrip("/").endswith("/finish"):
            self._post_finish_triage()

        if method == "POST" and response_json and body.get("mode") == "raw":
            case, self._pending_case = self._pending_case, None
            if case:
                record = {
                    "id": case["id"],
                    "failed": case["status"] == "failed",
                    "start": CLOCK.t,
                    "duration": planned_duration(case),
                    "defect": case.get("defect"),
                }
                self.item_records[response_json["id"]] = record
                self.inject_scenario(response_json["id"], case, record)

    def _rewrite_item_start(self, raw: str) -> str:
        try:
            payload = json.loads(raw)
        except ValueError:
            return raw
        if payload.get("type") != "STEP" or payload.get("hasStats") is False:
            return raw
        tc_id = payload.get("testCaseId")
        case = self.planned.get(tc_id)
        if not case:
            return raw
        payload["attributes"] = _item_attributes(case, self.stream["key"])
        payload["description"] = case["description"]
        payload["testCaseId"] = case["id"]
        payload["codeRef"] = case["code_ref"]
        payload["startTime"] = iso_now()
        self._pending_case = case
        return json.dumps(payload)

    def _rewrite_item_finish(self, url: str, raw: str) -> str:
        record = self.item_records.get(url.rstrip("/").rsplit("/", 1)[-1])
        if not record:
            return raw
        try:
            payload = json.loads(raw)
        except ValueError:
            return raw
        if record["failed"]:
            payload["status"] = "failed"
            payload.pop("issue", None)
        else:
            payload["status"] = "passed"
            payload.pop("issue", None)
        CLOCK.advance_to(record["start"] + record["duration"])
        payload["endTime"] = iso_now()
        CLOCK.advance(1 + _crc(record["id"]) % 3)
        return json.dumps(payload)

    def _post_finish_triage(self) -> None:
        to_triage = [(item_uuid, record) for item_uuid, record in self.item_records.items()
                     if record["failed"] and issue_for(self.planned[record["id"]])]
        if not to_triage:
            print("      + no post-finish triage (failed items stay To Investigate)")
            return
        issues = []
        for item_uuid, record in to_triage:
            issue = dict(issue_for(self.planned[record["id"]]))
            numeric_id = self._api("GET", f"/item/uuid/{item_uuid}")["id"]
            issues.append({"testItemId": numeric_id, "issue": issue})
        self._api("PUT", "/item", json={"issues": issues})
        print(f"      + post-finish triage applied to {len(issues)} failed items")

    def _api(self, method: str, path: str, **kwargs) -> dict:
        response = self.session.request(
            method, f"{self.env['url']}/{self.env['project']}{path}", **kwargs)
        if not response.ok:
            sys.exit(f"ERROR {response.status_code} on {method} {path}:\n{response.text}")
        return response.json() if response.content else {}

    def _post_log(self, item_uuid: str, level: str, message: str,
                  attachment: str | None = None) -> None:
        entry = {
            "launchUuid": self.env["current_launch_uuid"],
            "itemUuid": item_uuid,
            "level": level,
            "message": message,
            "time": iso_now(),
        }
        if attachment is None:
            self._api("POST", "/log", json=entry)
            return
        path = self._resolve_file(attachment)
        entry["file"] = {"name": path.name}
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        with path.open("rb") as handle:
            self._api("POST", "/log", files=[
                ("json_request_part", (None, json.dumps([entry]), "application/json")),
                ("file", (path.name, handle, content_type)),
            ])

    def inject_scenario(self, parent_uuid: str, case: dict, record: dict) -> None:
        launch_uuid = self.env["current_launch_uuid"]
        nested = case.get("nested") or []
        if nested:
            slice_s = record["duration"] * 0.8 / len(nested)
            for step in nested:
                step_uuid = self._api("POST", f"/item/{parent_uuid}", json={
                    "launchUuid": launch_uuid,
                    "name": step["name"],
                    "type": "STEP",
                    "hasStats": False,
                    "startTime": iso_now(),
                })["id"]
                for level, message, *attachment in step["logs"]:
                    self._post_log(step_uuid, level, message,
                                   attachment[0] if attachment else None)
                    CLOCK.advance(0.4)
                CLOCK.advance(max(0.2, slice_s - 0.4 * len(step["logs"])))
                self._api("PUT", f"/item/{step_uuid}", json={
                    "launchUuid": launch_uuid,
                    "endTime": iso_now(),
                    "status": step["status"],
                })
                short = step["name"].split(" <br />")[0]
                print(f"      + nested: {short} [{step['status']}]")
        for level, message, *attachment in case.get("item_logs") or []:
            self._post_log(parent_uuid, level, message,
                           attachment[0] if attachment else None)
            CLOCK.advance(0.5)
        self.custom_logged_items.add(parent_uuid)
        print(f"      + {len(case.get('item_logs') or [])} item logs ({case['id']})")
        self.env["date"] = iso_now()

    def replay(self, collection: dict) -> None:
        def walk(nodes):
            for node in nodes:
                if "item" in node:
                    walk(node["item"])
                elif "request" in node:
                    self.replay_request(node)
        walk(collection["item"])


def delete_existing_launches(url: str, project: str, api_key: str, name: str) -> None:
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {api_key}"
    api = f"{url.rstrip('/')}/api/v1/{project}"
    response = session.get(f"{api}/launch", params={"filter.eq.name": name, "page.size": 100})
    response.raise_for_status()
    ids = [launch["id"] for launch in response.json().get("content", []) if launch["name"] == name]
    if not ids:
        print("Reset: no existing launches to delete.")
        return
    response = session.delete(f"{api}/launch", params={"ids": ",".join(map(str, ids))})
    response.raise_for_status()
    print(f"Reset: deleted {len(ids)} existing launch(es): {ids}")


def stream_for_collection(path: Path) -> dict:
    name = path.name
    for stream in STREAMS.values():
        if stream["collection_file"] == name:
            return stream
    sys.exit(f"Unknown collection file: {name}. Expected one of: "
             + ", ".join(s["collection_file"] for s in STREAMS.values()))


def resolve_project_key(org: str, stream: dict) -> str:
    """Build RP project key: {org}.{stream-a|stream-b}.

    RP_PROJECT / --project is the organization slug (part before the dot).
    A full key like org.stream-b is accepted and reduced to org first.
    """
    org_slug = org.strip().split(".", 1)[0]
    if not org_slug:
        sys.exit("RP_PROJECT / --project must be a non-empty organization slug.")
    return f"{org_slug}.{stream['project_slug']}"


def upload_collection(path: Path, url: str, org: str, api_key: str,
                      reset: bool) -> None:
    stream = stream_for_collection(path)
    project = resolve_project_key(org, stream)
    collection = json.loads(path.read_text())
    if reset:
        delete_existing_launches(url, project, api_key, stream["launch_name"])
    set_clock(time.time() - 2400)
    launch_overrides = {
        "name": stream["launch_name"],
        "description": stream["launch_description"],
        "attributes": stream["attributes"],
        "startTime": iso_now(),
    }
    print(f"\n=== {stream['launch_name']} ===")
    print(f"Replaying '{collection['info']['name']}' -> {url} / {project}")
    replayer = CollectionReplayer(url, project, api_key, FIXTURES_DIR, stream,
                                  launch_overrides=launch_overrides)
    replayer.replay(collection)
    print(f"Done. Launch UUID: {replayer.env.get('current_launch_uuid', '?')}")
    print(f"View: {url.rstrip('/')}/ui/#{project}/launches/all")


def main() -> None:
    load_dotenv(SCRIPT_DIR / ".env")
    demo_env = SCRIPT_DIR.parent.parent / "Demo launch" / ".env"
    load_dotenv(demo_env)

    parser = argparse.ArgumentParser(description="Generate / replay Stream A & B RP collections")
    parser.add_argument("collection", nargs="?", help="Postman collection JSON to replay")
    parser.add_argument("--generate", action="store_true",
                        help="Write both Postman collections from catalog.py and exit")
    parser.add_argument("--all", action="store_true",
                        help="Generate both collections and upload them")
    parser.add_argument("--url", default=os.environ.get("RP_URL"))
    parser.add_argument("--project", default=os.environ.get("RP_PROJECT"),
                        help="Organization slug only (part before the dot). "
                             "Stream A uploads to {org}.stream-a, Stream B to {org}.stream-b")
    parser.add_argument("--api-key", default=os.environ.get("RP_API_KEY"))
    parser.add_argument("--reset", action="store_true",
                        help="Delete existing launches with the same name before upload")
    args = parser.parse_args()

    if args.generate:
        write_collections()
        return

    missing = [n for n, v in (("RP_URL/--url", args.url),
                              ("RP_PROJECT/--project", args.project),
                              ("RP_API_KEY/--api-key", args.api_key)) if not v]
    if missing:
        sys.exit("Missing config: " + ", ".join(missing)
                 + ". Fill .env next to this script (or Demo launch/.env) or pass CLI flags. "
                 "RP_PROJECT is the organization slug; stream-a/stream-b is appended per collection.")

    if args.all:
        paths = write_collections()
        for path in paths:
            upload_collection(path, args.url, args.project, args.api_key, args.reset)
        return

    if not args.collection:
        parser.print_help()
        sys.exit("\nPass a collection JSON, --generate, or --all.")

    collection_path = Path(args.collection)
    if not collection_path.is_file():
        collection_path = SCRIPT_DIR / args.collection
    if not collection_path.is_file():
        sys.exit(f"Collection not found: {args.collection}")
    upload_collection(collection_path, args.url, args.project, args.api_key, args.reset)


if __name__ == "__main__":
    main()
