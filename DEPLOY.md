# Deploying FormatWave 🌊

## Recommended Hosting: Render.com

This application is best hosted on **Render** (as a Web Service) because it requires:
1.  **File Uploads:** Handling large files (>4.5MB).
2.  **Long Processing Times:** Converting multi-page PDFs can take >10 seconds.
3.  **Local Filesystem:** Storing temporary files for processing.

### How to Deploy on Render

1.  Push your code to GitHub.
2.  Sign up on [Render.com](https://render.com).
3.  Click **New +** -> **Web Service**.
4.  Connect your `FormatWave` repository.
5.  Render will automatically detect:
    *   **Environment:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app:app` (from the `Procfile`)
6.  Click **Create Web Service**.

That's it! Your app will be live in a few minutes.

---

## Why avoid Vercel for this app?

Vercel is fantastic for frontend apps (Next.js, React), but it has strict limits for serverless functions on the free tier:

*   **❌ 4.5MB Request Body Limit:** Users cannot upload files larger than 4.5MB.
*   **❌ 10-Second Timeout:** Large PDF conversions will fail/timeout.
*   **❌ Read-Only Filesystem:** You cannot save uploaded files to disk easily without external storage (S3/R2).

Render's free tier is much more generous for this specific use case.
