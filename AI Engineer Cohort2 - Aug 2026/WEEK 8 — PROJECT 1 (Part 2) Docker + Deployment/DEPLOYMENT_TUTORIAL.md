# Deployment Tutorial: Docker → ACR → Azure Web App

Do this yourself, step by step, in your own terminal. Every command block is
copy-paste ready for **PowerShell** (the shell used in the live session). If
you're on macOS/Linux, the `az` and `docker` commands are identical — only the
env-var syntax differs (`export VAR="..."` instead of `$env:VAR = "..."`).

By the end you'll have: your app running in Docker locally, the image sitting
in your own Azure Container Registry (ACR), and a live public URL serving it
via Azure App Service (a "Web App").

---

## Prerequisites

- Docker Desktop installed and **running** (check the whale icon in your
  system tray — if it's not there, Docker commands fail with a connection
  error before anything else goes wrong)
- Azure CLI installed — check with `az --version`; if that fails, install
  from https://aka.ms/installazurecliwindows, then **close and reopen your
  terminal** (PATH only refreshes on new terminal sessions)
- An Azure account ([azure.microsoft.com/free/students](https://azure.microsoft.com/free/students) if you have a school email — no card needed)
- Your `OPENAI_API_KEY`, `COHERE_API_KEY`, and `OPENAI_MODEL` (e.g. `gpt-4o-mini`) ready to paste

---

## Part 1: Run it in Docker, locally

Open a terminal in this project's `Live` folder (where the `Dockerfile` lives).

**Build the image:**
```powershell
docker build -t multidoc-assist .
```

**Set your keys for this terminal session** (quotes required when assigning):
```powershell
$env:OPENAI_API_KEY = "sk-your-real-key-here"
$env:COHERE_API_KEY = "your-real-cohere-key-here"
```

**Run the container:**
```powershell
docker run -p 8080:8080 --name multidoc-assist-app -e OPENAI_API_KEY=$env:OPENAI_API_KEY -e COHERE_API_KEY=$env:COHERE_API_KEY -e OPENAI_MODEL=gpt-4o-mini multidoc-assist
```

No quotes needed around the `$env:` references here — PowerShell expands them
to plain values before Docker ever sees them.

Open `http://localhost:8080`, upload a document, ask it a question. If that
works, your image is good — everything from here on is about getting *this
exact image* into Azure.

Stop the container when you're done testing:
```powershell
docker stop multidoc-assist-app
docker rm multidoc-assist-app
```

---

## Part 2: Push the image to Azure Container Registry (ACR)

**Log in:**
```powershell
az login
az account show --output table
```
If the table doesn't print, stop — nothing below will work until this does.

**Create a resource group** (one folder that holds everything you create today — deleting it later removes everything in one shot):
```powershell
az group create --name rg-multidoc-assist --location centralindia
```

**Create your registry** — replace `<yourinitials>` with your own initials, e.g. `abacrmultidoc`. ACR names are global across *all* of Azure, so a generic name will collide with someone else's:
```powershell
az acr create --resource-group rg-multidoc-assist --name <yourinitials>acrmultidoc --sku Basic --admin-enabled true
```

**Push your image in:**
```powershell
az acr login --name <yourinitials>acrmultidoc
docker tag multidoc-assist <yourinitials>acrmultidoc.azurecr.io/multidoc-assist:v1
docker push <yourinitials>acrmultidoc.azurecr.io/multidoc-assist:v1
```

**Verify it landed:**
```powershell
az acr repository list --name <yourinitials>acrmultidoc --output table
```
You should see `multidoc-assist` printed. If the table is empty, `acr login`
likely expired — re-run it and push again.

---

## Part 3: What is a Web App?

Before mapping anything, know what you're creating:

| Thing | What it actually is |
|---|---|
| **ACR** | Just storage — a private Docker Hub. Nothing runs from here on its own. |
| **App Service Plan** | The compute you're renting (a VM, sized by tier — e.g. B1) that your app will run on. |
| **Web App** (App Service) | The actual running app — it pulls an image from ACR, runs it on the Plan, and gives it a public URL (`*.azurewebsites.net`). |

So the flow is: **image sits in ACR (done in Part 2) → a Plan provides compute
→ a Web App points at the ACR image and runs on that Plan → you get a URL.**
A Web App doesn't store your code — it only knows *which* image to pull and
*which settings* to hand it at startup.

---

## Part 4: Map the image to a Web App

You have two ways to do this — try the CLI first; if any `az webapp` command
throws a `ConnectionResetError`, that's a known CLI bug (not your mistake),
and you switch to the Portal for that one step only.

### Option A — CLI (try this first)

**Create the compute plan:**
```powershell
az appservice plan create --name plan-multidoc-assist --resource-group rg-multidoc-assist --is-linux --sku B1
```

**Create the Web App, pointed at your ACR image:**
```powershell
$loginServer = az acr show --name <yourinitials>acrmultidoc --query loginServer --output tsv
az webapp create --resource-group rg-multidoc-assist --plan plan-multidoc-assist --name <yourinitials>-multidoc-assist --deployment-container-image-name "$loginServer/multidoc-assist:v1"
```
(`--name` must also be globally unique — it becomes your URL.)

**Give the Web App permission to pull from ACR:**
```powershell
$acrUser = az acr credential show --name <yourinitials>acrmultidoc --query username --output tsv
$acrPass = az acr credential show --name <yourinitials>acrmultidoc --query "passwords[0].value" --output tsv
az webapp config container set --resource-group rg-multidoc-assist --name <yourinitials>-multidoc-assist --container-image-name "$loginServer/multidoc-assist:v1" --container-registry-url "https://$loginServer" --container-registry-user $acrUser --container-registry-password $acrPass --output none
```

**Set the port and your secrets:**
```powershell
az webapp config appsettings set --resource-group rg-multidoc-assist --name <yourinitials>-multidoc-assist --settings WEBSITES_PORT=8080 OPENAI_API_KEY=$env:OPENAI_API_KEY COHERE_API_KEY=$env:COHERE_API_KEY OPENAI_MODEL=gpt-4o-mini --output none
```

**Watch it boot:**
```powershell
az webapp log tail --resource-group rg-multidoc-assist --name <yourinitials>-multidoc-assist
```
Wait for Streamlit's "You can now view your app" line, then open
`https://<yourinitials>-multidoc-assist.azurewebsites.net`.

### Option B — Portal (if any CLI step above threw `ConnectionResetError`)

1. **Create Resource → Web App.**
   - **Publish**: select **Container** (not "Code" — this is the field most
     people miss, and picking "Code" means Azure expects source code, not
     your image).
   - **Resource Group**: pick your existing `rg-multidoc-assist` from the
     dropdown — don't let it create a new one, or cleanup later needs two
     `az group delete` commands instead of one.
   - **Operating System**: Linux. Pick a region, give it a unique name.
   - Continue past Basics — a Container tab or section will ask for your
     registry, image, and tag: pick **Azure Container Registry**, your ACR
     name, image `multidoc-assist`, tag `v1`.
   - Review + Create. **Before creating**, check the Review page shows *your*
     ACR's image path, not Azure's default `mcr.microsoft.com/appsvc/staticsite`
     — if it still shows the default, go back and fill in the registry fields.

2. **If it got created with the wrong image anyway** (easy to miss on the
   first pass): go to the Web App → **Deployment Center → Containers**. Click
   the `main` container row → **Edit container**:
   - Image source: **Azure Container Registry**
   - Registry: your ACR
   - Authentication: **Admin Credentials** (simpler than Managed Identity for
     a course setup — Managed Identity needs an extra IAM role assignment or
     the pull fails)
   - Image: `multidoc-assist` (check for typos — `multidoc-assit` will
     silently fail to find the image)
   - Tag: `v1`
   - Apply.

3. **Set app settings**: Web App → **Settings → Environment variables** (or
   **Configuration → Application settings** depending on portal version).
   Add: `WEBSITES_PORT` = `8080`, `OPENAI_API_KEY`, `COHERE_API_KEY`,
   `OPENAI_MODEL` = `gpt-4o-mini`. Save, then explicitly click **Restart** on
   the Overview page — don't assume it auto-restarts.

---

## Part 5: Cleanup

When you're done testing, delete everything in one shot so nothing keeps
billing:
```powershell
az group delete --name rg-multidoc-assist --output none
```
If the Portal ever created a *second* resource group for you (check the Web
App's Overview page for its "Resource group" field), delete that one too.

**Remember**: a *stopped* Web App still bills for its App Service Plan.
Only deleting the resource group actually stops charges.
