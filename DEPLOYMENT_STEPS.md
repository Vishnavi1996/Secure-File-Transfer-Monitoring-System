# FastAPI Deployment to PythonAnywhere - Final Steps

## Current Status ✓
- WSGI file created and configured
- Packages installed in virtualenv
- Updated `web_app.py` with absolute paths (committed and pushed to GitHub)
- Error resolved: Fixed "Directory 'static' does not exist" issue

## What Changed
The `web_app.py` file has been updated to use absolute file paths instead of relative paths. This fixes the deployment issue on PythonAnywhere where the working directory is different from expected.

**Changes made:**
- Added `BASE_DIR = os.path.dirname(os.path.abspath(__file__))`
- Updated all static file references to use absolute paths
- Updated all data directory references to use absolute paths

## Remaining Steps (Complete These on PythonAnywhere)

### Step 1: Pull Latest Changes from GitHub
Access PythonAnywhere bash console and run:
```bash
cd /home/vishnaviakula/app
git pull origin master
```

This will download the latest `web_app.py` with the path fixes.

### Step 2: Verify Packages are Installed
Run in bash console:
```bash
cd /home/vishnaviakula
source venv/bin/activate
pip list | grep -i "fastapi\|asgiref\|watchdog"
```

Should see: FastAPI, asgiref, watchdog, starlette, pydantic

If missing, install:
```bash
pip install -r "/home/vishnaviakula/app/file monitor/requirements.txt" asgiref
```

### Step 3: Reload PythonAnywhere Web App
1. Log into https://www.pythonanywhere.com
2. Go to "Web apps" tab
3. Click on "vishnaviakula.pythonanywhere.com"
4. Click the green "Reload" button at the top
5. Wait 5 seconds for reload to complete

### Step 4: Test the Deployment
Navigate to: https://vishnaviakula.pythonanywhere.com

You should see either:
- The FastAPI interactive docs, OR
- The welcome message from the app

### Step 5: Check Error Logs (If Issues Occur)
If you still see an error, check: https://www.pythonanywhere.com/user/vishnaviakula/files/var/log/vishnaviakula.pythonanywhere.com.error.log

## Troubleshooting

### "Module not found" errors
- Ensure packages are installed in virtualenv
- Check pip list output

### "Directory still doesn't exist" errors  
- Run `git pull` to get latest code
- Check that static directory exists in app folder

### 500 error without useful message
- Reload the web app again
- Wait 10 seconds and try again

## Architecture Summary

```
https://vishnaviakula.pythonanywhere.com/
    ↓
Nginx (reverse proxy)
    ↓
/var/www/vishnaviakula_pythonanywhere_com_wsgi.py (WSGI entry point)
    ↓
app = FastAPI() instance from web_app.py
    ↓
Routes: /api/start, /api/stop, /api/status, /api/simulate, /api/report, /api/alerts
```

## File Locations
- **App code:** `/home/vishnaviakula/app/file monitor/`
- **WSGI config:** `/var/www/vishnaviakula_pythonanywhere_com_wsgi.py`
- **Virtualenv:** `/home/vishnaviakula/venv/`
- **Error logs:** `/var/www/log/vishnaviakula.pythonanywhere.com.error.log`
- **Server logs:** `/var/www/log/vishnaviakula.pythonanywhere.com.server.log`

## Success Indicators
When working correctly, you should see:
- ✅ No 500 error
- ✅ API endpoints respond (check by visiting `/api/status`)
- ✅ Error log stops showing new errors after reload

Good luck! 🚀
