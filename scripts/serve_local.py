"""DEV-only local stand-in for the Scaleway Serverless Jobs API."""

import datetime
import json
import re
import subprocess
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

WORKER = "pizza-worker"
START = re.compile(r"^/serverless-jobs/v1alpha2/regions/[^/]+/job-definitions/([^/]+)/start$")
# map your local job-def ids (SCW_*_JOB_ID in .env) to the worker subcommand to run
JOBS = {
    "local-run-pending": [WORKER, "run-pending"],
    "local-add-category": [WORKER, "add-category"],
}


class H(BaseHTTPRequestHandler):
    """HTTP handler that answers the Scaleway Jobs "start" endpoint and runs the worker."""

    def do_POST(self):  # noqa: ANN201
        """Match the start endpoint, launch the worker subcommand, return a fake JobRun.

        The job-definition id in the URL selects which worker subcommand to run; any
        ``environment_variables`` in the request body (e.g. WORKER_PAYLOAD_ID) are
        forwarded to the subprocess. Replies with a minimal StartJobDefinitionResponse.
        """
        m = START.match(self.path)
        if not m:
            self.send_error(404)
            return
        job_def_id = m.group(1)
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0) or 0)) or b"{}")
        env_overrides = body.get("environment_variables") or {}  # for add-category later
        subprocess.Popen(  # noqa: S603
            JOBS.get(job_def_id, [WORKER, "run-pending"]),
            env={**__import__("os").environ, **env_overrides},
        )  # fire-and-forget = a job run
        run = {
            "id": str(uuid.uuid4()),
            "job_definition_id": job_def_id,
            "state": "queued",
            "region": "fr-par",
            "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
        }
        data = json.dumps({"job_runs": [run]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


HTTPServer(("0.0.0.0", 8080), H).serve_forever()  # noqa: S104
