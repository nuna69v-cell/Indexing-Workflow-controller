const fs = require('fs');
let pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

pkg.devDependencies = {
    "@tootallnate/once": "^3.0.1",
    "@types/cors": "^2.8.17",
    "@types/express": "^4.17.21",
    "@types/node": "^20.12.12",
    "@types/react": "^18.3.2",
    "@types/react-dom": "^18.3.0",
    "@types/ws": "^8.5.10",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "drizzle-kit": "^0.31.9",
    "eslint": "^8.57.0",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "tar": "^7.5.11",
    "typescript": "^5.4.5",
    "vite": "^5.2.11",
    "vitest": "^1.6.0"
};

pkg.pnpm = {
  "overrides": {
    "tar": "^7.5.11",
    "@tootallnate/once": "^3.0.1"
  }
};

fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
