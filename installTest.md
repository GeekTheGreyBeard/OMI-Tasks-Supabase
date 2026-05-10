# OMI-Tasks-Supabase install test

- Test host: omi-supabase-install-test
- Test started: 2026-05-10T23:05:31+00:00
- Repository: https://github.com/GeekTheGreyBeard/OMI-Tasks-Supabase.git
- Branch: main

Cloning into '/home/gtgb/omi-supabase-retest-20260510/OMI-Tasks-Supabase'...
- Commit: 3018c96 Add Omi task cockpit home page

## Static validation

static_content_ok
compose_config_ok
schema_apply_skipped
package_validation_ok
- PASS: static package validation

## Install

Created /home/gtgb/omi-supabase-retest-20260510/OMI-Tasks-Supabase/website/taskReviewUi/.env
 Network omi-tasks-supabase_default  Creating
 Network omi-tasks-supabase_default  Created
 Container omi-tasks-supabase-test-db  Creating
 Container omi-tasks-supabase-test-db  Created
 Container omi-tasks-supabase-test-db  Starting
 Container omi-tasks-supabase-test-db  Started
Waiting for Postgres...
Applying database schema...
CREATE EXTENSION
CREATE SCHEMA
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
INSERT 0 3
CREATE FUNCTION
DO
time="2026-05-10T23:05:41Z" level=warning msg="Docker Compose is configured to build using Bake, but buildx isn't installed"
#0 building with "default" instance using docker driver

#1 [omi-tasks-supabase-web internal] load build definition from Dockerfile
#1 transferring dockerfile:
#1 transferring dockerfile: 344B done
#1 DONE 0.3s

#2 [omi-tasks-supabase-web internal] load metadata for docker.io/library/python:3.12-slim
#2 DONE 0.2s

#3 [omi-tasks-supabase-web internal] load .dockerignore
#3 transferring context:
#3 transferring context: 2B done
#3 DONE 0.3s

#4 [omi-tasks-supabase-web internal] load build context
#4 ...

#5 [omi-tasks-supabase-web 1/5] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe
#5 resolve docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe 0.4s done
#5 DONE 0.4s

#4 [omi-tasks-supabase-web internal] load build context
#4 transferring context: 26.84kB done
#4 DONE 0.5s

#6 [omi-tasks-supabase-web 2/5] WORKDIR /app
#6 CACHED

#7 [omi-tasks-supabase-web 3/5] COPY requirements.txt /app/requirements.txt
#7 DONE 0.6s

#8 [omi-tasks-supabase-web 4/5] RUN pip install --no-cache-dir -r /app/requirements.txt
#8 4.563 Collecting fastapi==0.115.6 (from -r /app/requirements.txt (line 1))
#8 4.749   Downloading fastapi-0.115.6-py3-none-any.whl.metadata (27 kB)
#8 4.855 Collecting uvicorn==0.34.0 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 4.890   Downloading uvicorn-0.34.0-py3-none-any.whl.metadata (6.5 kB)
#8 4.946 Collecting psycopg==3.2.3 (from psycopg[binary]==3.2.3->-r /app/requirements.txt (line 3))
#8 4.986   Downloading psycopg-3.2.3-py3-none-any.whl.metadata (4.3 kB)
#8 5.038 Collecting python-multipart==0.0.20 (from -r /app/requirements.txt (line 4))
#8 5.069   Downloading python_multipart-0.0.20-py3-none-any.whl.metadata (1.8 kB)
#8 5.162 Collecting starlette<0.42.0,>=0.40.0 (from fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 5.185   Downloading starlette-0.41.3-py3-none-any.whl.metadata (6.0 kB)
#8 5.574 Collecting pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4 (from fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 5.633   Downloading pydantic-2.13.4-py3-none-any.whl.metadata (109 kB)
#8 5.750 Collecting typing-extensions>=4.8.0 (from fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 5.784   Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
#8 5.843 Collecting click>=7.0 (from uvicorn==0.34.0->uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 5.876   Downloading click-8.3.3-py3-none-any.whl.metadata (2.6 kB)
#8 5.911 Collecting h11>=0.8 (from uvicorn==0.34.0->uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 5.937   Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
#8 6.369 Collecting psycopg-binary==3.2.3 (from psycopg[binary]==3.2.3->-r /app/requirements.txt (line 3))
#8 6.396   Downloading psycopg_binary-3.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.8 kB)
#8 6.469 Collecting httptools>=0.6.3 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.500   Downloading httptools-0.7.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.5 kB)
#8 6.571 Collecting python-dotenv>=0.13 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.605   Downloading python_dotenv-1.2.2-py3-none-any.whl.metadata (27 kB)
#8 6.705 Collecting pyyaml>=5.1 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.740   Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
#8 6.850 Collecting uvloop!=0.15.0,!=0.15.1,>=0.14.0 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.892   Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.9 kB)
#8 7.113 Collecting watchfiles>=0.13 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 7.145   Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
#8 7.390 Collecting websockets>=10.4 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 7.409   Downloading websockets-16.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.8 kB)
#8 7.465 Collecting annotated-types>=0.6.0 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 7.493   Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
#8 9.181 Collecting pydantic-core==2.46.4 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.209   Downloading pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
#8 9.256 Collecting typing-inspection>=0.4.2 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.280   Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
#8 9.350 Collecting anyio<5,>=3.4.0 (from starlette<0.42.0,>=0.40.0->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.384   Downloading anyio-4.13.0-py3-none-any.whl.metadata (4.5 kB)
#8 9.456 Collecting idna>=2.8 (from anyio<5,>=3.4.0->starlette<0.42.0,>=0.40.0->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.484   Downloading idna-3.14-py3-none-any.whl.metadata (8.0 kB)
#8 9.536 Downloading fastapi-0.115.6-py3-none-any.whl (94 kB)
#8 9.580 Downloading uvicorn-0.34.0-py3-none-any.whl (62 kB)
#8 9.621 Downloading psycopg-3.2.3-py3-none-any.whl (197 kB)
#8 9.676 Downloading python_multipart-0.0.20-py3-none-any.whl (24 kB)
#8 9.713 Downloading psycopg_binary-3.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.2 MB)
#8 10.01    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 14.1 MB/s eta 0:00:00
#8 10.05 Downloading click-8.3.3-py3-none-any.whl (110 kB)
#8 10.08 Downloading h11-0.16.0-py3-none-any.whl (37 kB)
#8 10.11 Downloading httptools-0.7.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (517 kB)
#8 10.17 Downloading pydantic-2.13.4-py3-none-any.whl (472 kB)
#8 10.25 Downloading pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
#8 10.38    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 17.8 MB/s eta 0:00:00
#8 10.41 Downloading python_dotenv-1.2.2-py3-none-any.whl (22 kB)
#8 10.45 Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (807 kB)
#8 10.49    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 807.9/807.9 kB 18.8 MB/s eta 0:00:00
#8 10.52 Downloading starlette-0.41.3-py3-none-any.whl (73 kB)
#8 10.56 Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
#8 10.59 Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (4.4 MB)
#8 10.92    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.4/4.4 MB 14.1 MB/s eta 0:00:00
#8 10.94 Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (456 kB)
#8 10.99 Downloading websockets-16.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (184 kB)
#8 11.03 Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
#8 11.07 Downloading anyio-4.13.0-py3-none-any.whl (114 kB)
#8 11.11 Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
#8 11.13 Downloading idna-3.14-py3-none-any.whl (72 kB)
#8 11.35 Installing collected packages: websockets, uvloop, typing-extensions, pyyaml, python-multipart, python-dotenv, psycopg-binary, idna, httptools, h11, click, annotated-types, uvicorn, typing-inspection, pydantic-core, psycopg, anyio, watchfiles, starlette, pydantic, fastapi
#8 16.00 Successfully installed annotated-types-0.7.0 anyio-4.13.0 click-8.3.3 fastapi-0.115.6 h11-0.16.0 httptools-0.7.1 idna-3.14 psycopg-3.2.3 psycopg-binary-3.2.3 pydantic-2.13.4 pydantic-core-2.46.4 python-dotenv-1.2.2 python-multipart-0.0.20 pyyaml-6.0.3 starlette-0.41.3 typing-extensions-4.15.0 typing-inspection-0.4.2 uvicorn-0.34.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-16.0
#8 16.00 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#8 16.21 
#8 16.21 [notice] A new release of pip is available: 25.0.1 -> 26.1.1
#8 16.21 [notice] To update, run: pip install --upgrade pip
#8 DONE 17.2s

#9 [omi-tasks-supabase-web 5/5] COPY app.py /app/app.py
#9 DONE 0.7s

#10 [omi-tasks-supabase-web] exporting to image
#10 exporting layers
#10 exporting layers 5.0s done
#10 exporting manifest sha256:69a4d8e23575fd36c81a70ee602768030f111aa605eeaa316fbaf6031d6e8566
#10 exporting manifest sha256:69a4d8e23575fd36c81a70ee602768030f111aa605eeaa316fbaf6031d6e8566 0.2s done
#10 exporting config sha256:f9ce608ac9b23f1cbba69eac6462017da5cc724868cfd365554ec139c0a70aa9
#10 exporting config sha256:f9ce608ac9b23f1cbba69eac6462017da5cc724868cfd365554ec139c0a70aa9 0.2s done
#10 exporting attestation manifest sha256:486fea753dc2559417ecb1104488ca956cef24709f3b0754421de76c6301fab4
#10 exporting attestation manifest sha256:486fea753dc2559417ecb1104488ca956cef24709f3b0754421de76c6301fab4 0.5s done
#10 exporting manifest list sha256:4330a6757caff6267c57ae7420ff7e28d70a4437d1ea4f838fa86e295a1e85fc
#10 exporting manifest list sha256:4330a6757caff6267c57ae7420ff7e28d70a4437d1ea4f838fa86e295a1e85fc 0.4s done
#10 naming to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest
#10 naming to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest 0.1s done
#10 unpacking to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest
#10 unpacking to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest 2.0s done
#10 DONE 8.7s

#11 [omi-tasks-supabase-web] resolving provenance for metadata file
#11 DONE 0.0s
 omi-tasks-supabase-web  Built
time="2026-05-10T23:06:12Z" level=warning msg="Found orphan containers ([omi-tasks-supabase-test-db]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up."
 Container omi-tasks-supabase-web  Creating
 Container omi-tasks-supabase-web  Created
 Container omi-tasks-supabase-web  Starting
 Container omi-tasks-supabase-web  Started
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Creating
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Created
time="2026-05-10T23:06:14Z" level=warning msg="Found orphan containers ([omi-tasks-supabase-web omi-tasks-supabase-test-db]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up."
 Container omi-tasks-supabase-n8n  Creating
 Container omi-tasks-supabase-n8n  Created
 Container omi-tasks-supabase-n8n  Starting
 Container omi-tasks-supabase-n8n  Started
Containers:
omi-tasks-supabase-n8n	Up Less than a second	0.0.0.0:5679->5678/tcp, [::]:5679->5678/tcp
omi-tasks-supabase-web	Up 3 seconds	0.0.0.0:8098->8098/tcp, [::]:8098->8098/tcp
omi-tasks-supabase-test-db	Up 42 seconds (healthy)	0.0.0.0:55433->5432/tcp, [::]:55433->5432/tcp

Web UI: http://localhost:8098/review
n8n:    http://localhost:5679

Install complete.
- PASS: installer completed

## Page checks

- PASS: task home route returns 200
- PASS: task home contains cockpit heading
- PASS: review page contains home button
- PASS: review route returns 200
- PASS: primary tasks route returns 200
- PASS: new task route returns 200
- PASS: submissions route returns 200
- PASS: trash route returns 200
- PASS: n8n route reachable

## Uninstall

 Container omi-tasks-supabase-web  Stopping
 Container omi-tasks-supabase-web  Stopped
 Container omi-tasks-supabase-web  Removing
 Container omi-tasks-supabase-web  Removed
 Container omi-tasks-supabase-test-db  Stopping
 Container omi-tasks-supabase-n8n  Stopping
 Container omi-tasks-supabase-test-db  Stopped
 Container omi-tasks-supabase-test-db  Removing
 Container omi-tasks-supabase-test-db  Removed
 Container omi-tasks-supabase-n8n  Stopped
 Container omi-tasks-supabase-n8n  Removing
 Container omi-tasks-supabase-n8n  Removed
 Image omi-tasks-supabase-omi-tasks-supabase-web:latest  Removing
 Network omi-tasks-supabase_default  Removing
 Network omi-tasks-supabase_default  Removed
 Image omi-tasks-supabase-omi-tasks-supabase-web:latest  Removed
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Removing
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Removed
Uninstall complete. Only repository files should remain.
- PASS: uninstall completed
- PASS: no project containers remain
- PASS: no project volumes remain
- PASS: generated env removed

## Result

- Passed checks: 15
- Failed checks: 0
- Test completed: 2026-05-10T23:06:33+00:00

**Overall result: PASS**
