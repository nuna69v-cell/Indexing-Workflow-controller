module.exports = {
  apps: [
    {
      name: "GenX-Central-Brain",
      script: "server.ts",
      interpreter: "tsx",
      env: {
        NODE_ENV: "production",
        PORT: 3000
      },
      restart_delay: 5000,
      max_restarts: 10
    },
    {
      name: "GenX-AI-Orchestrator",
      script: "main.py",
      interpreter: "python3",
      restart_delay: 5000,
      max_restarts: 10
    }
  ]
};
