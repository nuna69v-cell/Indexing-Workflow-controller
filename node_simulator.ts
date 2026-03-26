import io from "socket.io-client";

const SERVER_URL = "http://localhost:3000";
const socket = io(SERVER_URL);

const nodeId = `node-${Math.random().toString(36).substr(2, 9)}`;
const nodeName = process.argv[2] || "Simulated-Node";

console.log(`Starting Node: ${nodeName} (${nodeId})`);

socket.on("connect", () => {
  console.log("Connected to Central Brain");

  // Send heartbeat every 5 seconds
  setInterval(() => {
    const heartbeat = {
      id: nodeId,
      name: nodeName,
      type: "FOREX",
      broker: "Exness",
      status: "TRADING",
      latency: Math.floor(Math.random() * 50) + 10,
      cpu: Math.floor(Math.random() * 30) + 5,
      memory: Math.floor(Math.random() * 40) + 20,
    };
    socket.emit("node:heartbeat", heartbeat);
  }, 5000);

  // Simulate random trade signals
  setInterval(() => {
    if (Math.random() > 0.8) {
      const signal = {
        id: `sig-${Date.now()}`,
        nodeId,
        symbol: "EURUSD",
        side: Math.random() > 0.5 ? "BUY" : "SELL",
        price: 1.0842 + (Math.random() - 0.5) * 0.01,
        timestamp: new Date().toISOString(),
      };
      console.log("Sending trade signal:", signal);
      socket.emit("trade:signal", signal);
    }
  }, 10000);
});

socket.on("disconnect", () => {
  console.log("Disconnected from Central Brain");
});

socket.on("trade:alert", (data) => {
  console.log("Global Trade Alert received:", data);
});
