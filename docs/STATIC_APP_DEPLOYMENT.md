# Deploying GenX_FX Frontend to Static.app (Windows)

This guide walks you through setting up your Node.js environment on Windows, building the frontend application, and deploying it to [Static.app](https://static.app/).

## Prerequisites

You have downloaded the Node.js portable zip file to:
`C:\Users\USER\AppData\Local\Temp\MicrosoftEdgeDownloads\80e34cce-6e88-4bd7-afc6-16abd7d96b1f\node-v24.14.0-win-x64.zip`

## Step 1: Install Node.js on Windows

1. **Extract the ZIP file**:
   - Navigate to the folder containing `node-v24.14.0-win-x64.zip`.
   - Right-click the file and select **Extract All...**.
   - Extract it to a permanent location, such as `C:\Program Files\nodejs` or `C:\node-v24.14.0-win-x64`.

2. **Add Node.js to your System PATH**:
   - Press the Windows Key and type **Environment Variables**.
   - Select **Edit the system environment variables**.
   - Click the **Environment Variables...** button at the bottom.
   - Under **System variables** (or User variables), find the `Path` variable, select it, and click **Edit...**.
   - Click **New** and add the path to the folder where you extracted Node.js (e.g., `C:\node-v24.14.0-win-x64`).
   - Click **OK** on all windows to save the changes.

3. **Verify the Installation**:
   - Open a new Command Prompt (`cmd`) or PowerShell window.
   - Run `node -v` to ensure it outputs `v24.14.0`.
   - Run `npm -v` to ensure npm is also installed and recognized.

## Step 2: Build the Frontend Application

The GenX_FX application consists of a React frontend and a Python backend. For Static.app, we only need to build and deploy the React frontend.

1. **Navigate to the Project Directory**:
   Open Command Prompt or PowerShell and navigate to your project folder:
   ```cmd
   cd path\to\your\GenX_FX\project
   ```

2. **Install Dependencies**:
   Run the following command to install all required Node.js packages:
   ```cmd
   npm install
   ```
   *(Note: If you encounter issues with `@neondatabase/serverless` during install, you can safely ignore them as they are known environment limitations or use `npm install --legacy-peer-deps`)*

3. **Build the Application**:
   Compile the React application into static HTML/CSS/JS files:
   ```cmd
   npm run build
   ```
   This will generate a `dist` folder inside the `client` directory (or the root depending on Vite config). All your static assets are now ready in `client/dist`.

## Step 3: Package the Static Files

1. **Navigate to the Build Output**:
   Go to the `client/dist` directory using File Explorer.
   ```
   C:\path\to\GenX_FX\client\dist
   ```

2. **Create a ZIP Archive**:
   - Select **all files and folders** inside the `dist` directory (like `index.html`, `assets/`, etc.).
   - Right-click the selected files, choose **Send to** -> **Compressed (zipped) folder**.
   - Name the file something like `genx_fx_frontend.zip`.

## Step 4: Deploy to Static.app

Static.app provides a one-click hosting solution for static websites.

1. **Go to Static.app**:
   Open your web browser and navigate to [https://static.app/](https://static.app/).

2. **Upload your ZIP file**:
   - You will see a large upload area on the homepage that says "ZIPs, images, or files — live and shareable in one click."
   - Drag and drop your `genx_fx_frontend.zip` file into this area.
   - Alternatively, click the upload area to open a file browser and select your ZIP file.

3. **Wait for Deployment**:
   - Static.app will automatically extract your ZIP file, host it, and generate a live, shareable URL for your application.
   - You can copy this URL to view your live GenX_FX trading dashboard!

## Step 5: Update the API URL (If necessary)

Since your frontend is now hosted on a static server, it needs to know where your Python FastAPI backend is located.

Before running `npm run build` in Step 2, ensure you create a `.env` file in the root or `client` directory with your actual production backend URL:

```env
VITE_API_URL=https://your-production-backend-url.com
```

If you don't do this, the frontend will try to connect to localhost (`http://127.0.0.1:8000`), which will only work if the user viewing the static app also has the backend running locally.
