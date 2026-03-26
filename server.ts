import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import { createServer as createViteServer } from "vite";
import path from "path";
import { fileURLToPath } from "url";
import { initializeApp } from "firebase/app";
import { initializeFirestore, collection, query, where, onSnapshot, updateDoc, doc } from "firebase/firestore";
import fs from "fs";
import { exec, spawn } from "child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load Firebase Config
const firebaseConfig = JSON.parse(fs.readFileSync(path.join(__dirname, "firebase-applet-config.json"), "utf8"));
const firebaseApp = initializeApp(firebaseConfig);
const db = initializeFirestore(firebaseApp, {
  experimentalForceLongPolling: true,
}, firebaseConfig.firestoreDatabaseId);

// Spawn AI Orchestrator (Python)
let orchestratorProcess: any = null;
let ioInstance: any = null;

function startOrchestrator() {
  console.log("[SYSTEM] Starting AI Orchestrator (Python)...");
  orchestratorProcess = spawn("python3", ["main.py"]);

  orchestratorProcess.stdout.on("data", (data: any) => {
    console.log(`[ORCHESTRATOR] ${data}`);
    if (ioInstance) {
      ioInstance.emit("system:orchestrator_status", { status: "running", lastOutput: data.toString() });
    }
  });

  orchestratorProcess.stderr.on("data", (data: any) => {
    console.error(`[ORCHESTRATOR ERROR] ${data}`);
    if (ioInstance) {
      ioInstance.emit("system:orchestrator_status", { status: "error", lastOutput: data.toString() });
    }
  });

  orchestratorProcess.on("close", (code: any) => {
    console.log(`[ORCHESTRATOR] Process exited with code ${code}. Restarting in 5s...`);
    if (ioInstance) {
      ioInstance.emit("system:orchestrator_status", { status: "stopped", code });
    }
    setTimeout(startOrchestrator, 5000);
  });
}

// Start orchestrator if not in production or if explicitly requested
if (process.env.NODE_ENV === "production" || process.env.START_ORCHESTRATOR === "true") {
  startOrchestrator();
}

async function startServer() {
  const app = express();
  const httpServer = createServer(app);
  const io = new Server(httpServer, {
    cors: {
      origin: "*",
    },
  });
  ioInstance = io;

  const PORT = Number(process.env.PORT) || 3000;

  // Command Processor Simulation
  const unsubscribeCommands = onSnapshot(
    query(collection(db, "commands"), where("status", "==", "PENDING")), 
    (snapshot) => {
      snapshot.docs.forEach(async (commandDoc) => {
        const command = commandDoc.data();
        console.log(`[COMMAND] Processing ${command.command} for node ${command.nodeId}`);
        
        // Simulate processing delay
        setTimeout(async () => {
          try {
            await updateDoc(doc(db, "commands", commandDoc.id), {
              status: "EXECUTED",
              executedAt: new Date().toISOString()
            });
            console.log(`[COMMAND] ${command.command} executed for node ${command.nodeId}`);
            
            // Also update node status in Firestore
            io.emit("node:command_executed", { nodeId: command.nodeId, command: command.command });
          } catch (err) {
            console.error("Error updating command status:", err);
          }
        }, 2000);
      });
    },
    (error) => {
      console.error("Firestore onSnapshot Error [commands]:", error);
      // If it's a timeout/cancelled error, we might want to log it specifically
      if (error.message.includes("CANCELLED") || error.message.includes("idle stream")) {
        console.warn("Firestore idle stream disconnected. SDK will automatically reconnect.");
      }
    }
  );

  // Middleware
  app.use(express.json());

  // API Routes
  app.get("/api/health", (req, res) => {
    res.json({ status: "operational", timestamp: new Date().toISOString() });
  });

  // Socket.io Logic
  io.on("connection", (socket) => {
    console.log("Client connected:", socket.id);

    socket.on("node:heartbeat", (data) => {
      // Broadcast node health to all clients (dashboard)
      io.emit("node:status", { ...data, lastSeen: new Date().toISOString() });
    });

    socket.on("trade:signal", (data) => {
      // Broadcast trade signals
      io.emit("trade:alert", data);
    });

    socket.on("shell:command", (command) => {
      console.log(`[SHELL] Executing: ${command}`);
      
      // Security: Basic command filtering could go here
      // For this applet, we'll allow standard commands
      
      exec(command, (error, stdout, stderr) => {
        const output = stdout || stderr || (error ? error.message : "Command executed with no output.");
        socket.emit("shell:output", {
          command,
          output,
          isError: !!error || !!stderr
        });
      });
    });

    socket.on("disconnect", () => {
      console.log("Client disconnected:", socket.id);
    });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.join(__dirname, "dist")));
    app.get("*", (req, res) => {
      res.sendFile(path.join(__dirname, "dist", "index.html"));
    });
  }

  httpServer.listen(PORT, "0.0.0.0", () => {
    console.log(`GenX VisionOps Central Brain running on http://localhost:${PORT}`);
  });
}

startServer();
