# Environment Setup Instructions - Week 2 Live Session

## Quick Start (2 minutes)

### Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in (create account if needed)
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-proj-`)
5. **Keep it SECRET** ✅

### Step 2: Create Your .env File

1. In the "Live Session" folder, rename `.env_student` → `.env`
2. Open `.env` in your editor
3. Replace `sk-proj-placeholder-replace-with-your-key` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
   ```
4. Save the file

### Step 3: Install Required Libraries

Run this in your terminal (inside the repository folder with virtual env activated):

```bash
pip install openai tiktoken python-dotenv numpy matplotlib
```

### Step 4: Verify Setup

In a Python cell, run:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ API Key loaded successfully!")
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized!")
else:
    print("❌ API Key not found. Check your .env file.")
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"

**Solution**: Install the package
```bash
pip install openai
```

### "API Key not found"

**Check**:
1. Is the file named `.env` (not `.env_student`)?
2. Is `OPENAI_API_KEY` spelled correctly (case-sensitive)?
3. Did you save the file after editing?
4. Is the key inside quotes? (Optional, but both work)

### "Authentication failed" error

**Cause**: Invalid API key
**Solution**:
1. Go to https://platform.openai.com/api-keys
2. Generate a new key
3. Update `.env` with the new key

### "Rate limit exceeded"

**Normal**: This happens if you make many API calls quickly
**Solution**: Wait a few seconds before trying again

---

## What Gets Created After Setup

After running a notebook cell with:
```python
from dotenv import load_dotenv
load_dotenv()
```

- ✅ Environment variables loaded from `.env`
- ✅ `OPENAI_API_KEY` available in `os.getenv("OPENAI_API_KEY")`
- ✅ OpenAI client ready to use

---

## Security Reminder

✅ **Good Practice** (Secure):
```python
# In .env file
OPENAI_API_KEY=sk-proj-xxx

# In code
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
```

❌ **Bad Practice** (Insecure):
```python
# Never do this!
api_key = "sk-proj-xxx"  # Exposed in code
```

---

## During the Live Session

**Before class starts**:
1. ✅ Create `.env` file with your API key
2. ✅ Install libraries with `pip install openai tiktoken python-dotenv numpy matplotlib`
3. ✅ Test the setup (run the verification script above)

**During class**:
- Share the Student notebook with everyone
- Keep your `.env` file PRIVATE (don't share!)
- If someone needs help, they can copy `.env_student` → `.env` and add their key

---

## Questions?

Post in the session chat or email for help!
