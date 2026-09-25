# Troubleshooting: Docker + Azure Deployment

Every issue on this list actually happened to someone during the live
session — not hypothetical. Find your symptom, apply the fix, keep going.
Organized by the phase you'll hit it in.

---

## Phase 1: Running locally (before Docker)

| Symptom | Cause | Fix |
|---|---|---|
| `TypeError` / 500 error in Streamlit after asking a question | Usually the backend returned `None` or an error object the frontend didn't expect | Check the FastAPI terminal for the real traceback — Streamlit's error is just the symptom, the cause is one level down |
| Swagger `/upload` or `/retrieve` still has `"string"` as a value | You're testing with the placeholder Swagger fills in automatically | Replace every `"string"` with a real value — e.g. `embedding_model` should be `"openai"` or `"small"`, not left as `"string"` |
| `UnboundLocalError: local variable 'embeddings' referenced before assignment` | An unmatched `model_type`/`embedding_model` value fell through every `if/elif` with no `else` | Pass a real, valid value (see above) — this is also a real gap worth knowing: some versions of `get_embeddings()` don't raise a clear error on a bad value, they just fail confusingly later |
| `openai.BadRequestError` / 401 auth error in the uvicorn terminal | `OPENAI_API_KEY` is missing, wrong, or expired | Check `src/backend/.env` has a real, current key; regenerate the key on platform.openai.com if unsure |
| "Skipping empty file" / 0 chunks indexed after upload | Multiple rapid `/upload` calls hit the same file path while it was still being written | Upload one file at a time, wait for the response before uploading the next |

## Phase 2: Docker

| Symptom | Cause | Fix |
|---|---|---|
| `error during connect` / Docker daemon not responding | Docker Desktop isn't running | Open Docker Desktop, wait for the whale icon to show "running," then retry |
| `docker build` fails during `pip install` | A `requirements.txt` version conflict | Read the actual pip error — it names the conflicting package and version |
| Container exits immediately after `docker run` | Almost always a missing env var crashing startup | `docker logs <container_name>` to see why — usually a missing API key |
| App runs but secrets seem empty/wrong inside the container | Used bash-style `$VAR` in PowerShell instead of `$env:VAR` | PowerShell needs `$env:VARNAME` to reference an environment variable — bare `$VARNAME` is an empty, unrelated PowerShell variable and silently passes an empty string |
| PowerShell tries to **execute** your API key as a command | Assigned the variable without quotes: `$env:OPENAI_API_KEY =sk-proj-...` | Always quote the value: `$env:OPENAI_API_KEY = "sk-proj-..."` |

## Phase 3: Azure CLI setup

| Symptom | Cause | Fix |
|---|---|---|
| `az : The term 'az' is not recognized...` | Azure CLI isn't installed — it's a separate install from any VS Code extension | Install from https://aka.ms/installazurecliwindows, then **close and reopen the terminal** (PATH doesn't refresh in an already-open one) |
| `(MissingSubscriptionRegistration) The subscription is not registered to use namespace 'Microsoft.ContainerRegistry'` | Brand-new subscriptions haven't activated every Azure service yet — a one-time per-subscription step | `az provider register --namespace Microsoft.ContainerRegistry`, then poll `az provider show --namespace Microsoft.ContainerRegistry --query registrationState --output tsv` until it says `Registered`, then retry your original command |
| `az acr create` fails with "name is already taken" | ACR names must be globally unique across **all** of Azure, not just your subscription | Add your initials or a random suffix to the name |

## Phase 4: Pushing to ACR

| Symptom | Cause | Fix |
|---|---|---|
| `az acr build` fails with `TasksOperationsNotAllowed` | ACR Tasks (cloud-side builds) are blocked on Azure for Students / free-trial subscriptions — an anti-abuse measure | Skip cloud builds entirely: `az acr login --name <ACR>`, then `docker build` + `docker tag` + `docker push` locally |
| `az acr build` / `az acr login` says `Unable to find 'Dockerfile'` | `--file` is resolved relative to your shell's **current directory**, not the source-context argument | Run the command from the folder that actually contains the `Dockerfile`, with context `.` |
| `az acr repository list` shows an empty table after you thought you pushed | `az acr login` token had expired before the `docker push` | Re-run `az acr login --name <ACR>`, then `docker push` again |

## Phase 5: Creating the Web App

| Symptom | Cause | Fix |
|---|---|---|
| Any `az webapp create` / `az webapp config container set` / `az webapp config appsettings set` fails with `ConnectionResetError`, traceback mentioning `is_flex_functionapp` | A known, reproducible Azure CLI bug — not something you did wrong. Confirmed to affect even read-only commands like `az webapp show` while unrelated commands (`az account show`) work fine | Do that specific step in the **Azure Portal** instead — CLI and Portal aren't mutually exclusive, mix them as needed |
| Portal "Create Web App" review screen shows `mcr.microsoft.com/appsvc/staticsite:latest` as the image | The Container/Registry fields on the Basics tab were left as Azure's default because "Publish" was left on **Code** instead of switched to **Container** | Go back to Basics, select **Container** under Publish, then fill in Registry/Image/Tag before creating — or fix it after creation via Deployment Center → Containers |
| Portal created a brand-new resource group like `plan-multidoc-assist_group` instead of your existing one | The Resource Group dropdown defaulted to "(New)" and wasn't changed | Select your existing resource group from the dropdown before creating. Not fatal if missed — the Web App can still pull from an ACR in a different resource group, it just means cleanup needs two `az group delete` commands instead of one |
| Container still shows `appsvc/staticsite` / wrong image after creation | The image was never changed from the Azure default during setup | Web App → **Deployment Center → Containers** → click the `main` container → **Edit container** → fix Image source / Registry / Image / Tag → Apply |
| Pulling the image fails after switching Authentication to **Managed Identity** | Managed Identity needs an extra step — granting that identity an `AcrPull` role on the registry via IAM — which wasn't done | Switch Authentication to **Admin Credentials** instead (works immediately since ACR was created with `--admin-enabled true`), or do the IAM role assignment if you want to keep Managed Identity |
| Typo in the Image field (e.g. `multidoc-assit`) | Manual entry required when using Managed Identity — image/tag don't auto-populate | Double-check the exact spelling against `az acr repository list` output |

## Phase 6: Once it's "created" but not working

| Symptom | Cause | Fix |
|---|---|---|
| Site returns a 503 that never clears, not just a slow cold start | `WEBSITES_PORT` set to `8000` (FastAPI's internal port) instead of `8080` — Streamlit can't bind, fails with "port already in use" | Set `WEBSITES_PORT=8080` in app settings |
| Every question fails with `openai.BadRequestError: you must provide a model parameter` | `OPENAI_MODEL` app setting is missing — it's easy to forget since it isn't a secret | Add `OPENAI_MODEL` (e.g. `gpt-4o-mini`) as an app setting |
| Overview page says "Cannot fetch health check data. Please try again later." right after creation | Normal and expected until the container has the right image *and* the right app settings and has actually booted | Ignore it until image + settings are both correct, then give it 1-2 minutes |
| You changed a setting in the Portal but the app still behaves the old way | The log stream can show stale, buffered output — or the app never restarted | Explicitly click **Restart** on the Web App's Overview page after any config change — don't assume it happens automatically |
| Portal shows "Failed to start web app" / "ajaxExtended call failed" | Generic Portal error, often a stale session/token after inactivity | Simply retry clicking **Start** — this resolved itself without any other change in a real case |

## General reminders

- A **stopped** Web App still bills for its App Service Plan — only deleting
  the resource group actually stops charges.
- Never paste a real API key directly into a command you're about to share a
  screenshot of — use `$env:VARNAME` references, and if a real key is ever
  shown on screen, **rotate/regenerate it immediately** on the provider's
  dashboard rather than trusting it's fine.
- When in doubt about whether an `az` command actually did something, most
  write commands are safe to re-run — `az group create`, `az acr create`, and
  `az webapp create` all succeed silently if the resource already exists.
