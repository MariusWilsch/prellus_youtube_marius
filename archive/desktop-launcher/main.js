const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn, exec } = require('child_process');
const path = require('path');
const fs = require('fs');

let mainWindow;
let appProcess;
let isAppRunning = false;

// Create the browser window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    icon: path.join(__dirname, 'icons/app.png')
  });

  mainWindow.loadFile('index.html');
  
  // Open DevTools during development if needed
  // mainWindow.webContents.openDevTools();

  mainWindow.on('closed', function() {
    mainWindow = null;
  });
}

// Start the application when Electron is ready
app.whenReady().then(() => {
  createWindow();
  
  app.on('activate', function() {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed (except on macOS)
app.on('window-all-closed', function() {
  if (process.platform !== 'darwin') app.quit();
});

// Handler for app quit
app.on('before-quit', async (event) => {
  // Stop Docker containers if they're running
  if (isAppRunning) {
    event.preventDefault();
    await stopApp();
    app.exit(0);
  }
});

// IPC handlers for communication with the renderer process
ipcMain.on('start-app', async () => {
  if (!isAppRunning) {
    await startApp();
  } else {
    mainWindow.webContents.send('app-status', 'App is already running');
  }
});

ipcMain.on('stop-app', async () => {
  if (isAppRunning) {
    await stopApp();
  } else {
    mainWindow.webContents.send('app-status', 'App is not running');
  }
});

ipcMain.on('check-status', async () => {
  await checkAppStatus();
});

ipcMain.on('open-app', () => {
  openWebApp();
});

// Function to start the Docker containers
async function startApp() {
  mainWindow.webContents.send('app-status', 'Starting app...');
  
  // First check if Docker is running
  try {
    await execPromise('docker info');
  } catch (error) {
    mainWindow.webContents.send('app-status', 'Error: Docker is not running. Please start Docker Desktop first.');
    return;
  }
  
  // Get the parent directory (where docker-compose.yaml is located)
  const appDir = path.join(__dirname, '..');
  
  try {
    // Start the containers with docker-compose
    await execPromise('docker-compose up -d', { cwd: appDir });
    isAppRunning = true;
    mainWindow.webContents.send('app-status', 'App started successfully!');
    
    // Wait a moment for services to be ready
    setTimeout(() => {
      mainWindow.webContents.send('app-ready');
    }, 5000);
  } catch (error) {
    mainWindow.webContents.send('app-status', `Error starting app: ${error.message}`);
  }
}

// Function to stop the Docker containers
async function stopApp() {
  mainWindow.webContents.send('app-status', 'Stopping app...');
  
  // Get the parent directory (where docker-compose.yaml is located)
  const appDir = path.join(__dirname, '..');
  
  try {
    // Stop the containers with docker-compose
    await execPromise('docker-compose down', { cwd: appDir });
    isAppRunning = false;
    mainWindow.webContents.send('app-status', 'App stopped successfully!');
    mainWindow.webContents.send('app-stopped');
  } catch (error) {
    mainWindow.webContents.send('app-status', `Error stopping app: ${error.message}`);
  }
}

// Function to check if the app is currently running
async function checkAppStatus() {
  const appDir = path.join(__dirname, '..');
  
  try {
    const output = await execPromise('docker-compose ps', { cwd: appDir });
    if (output.includes('backend') && output.includes('Up')) {
      isAppRunning = true;
      mainWindow.webContents.send('app-status', 'App is running');
      mainWindow.webContents.send('app-ready');
    } else {
      isAppRunning = false;
      mainWindow.webContents.send('app-status', 'App is not running');
      mainWindow.webContents.send('app-stopped');
    }
  } catch (error) {
    mainWindow.webContents.send('app-status', `Error checking status: ${error.message}`);
  }
}

// Function to open the web app in the default browser
function openWebApp() {
  const url = 'http://localhost:3000';
  const start = (process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'start' : 'xdg-open');
  spawn(start, [url], { shell: true });
}

// Helper function to promisify exec
function execPromise(command, options = {}) {
  return new Promise((resolve, reject) => {
    exec(command, options, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        resolve(stdout.trim());
      }
    });
  });
} 