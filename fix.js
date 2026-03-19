import fs from 'fs';
let pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.dependencies["@neondatabase/serverless"] = "^1.0.2";
pkg.pnpm = {
  overrides: {
    "tar": "^7.5.11",
    "@tootallnate/once": "^3.0.1"
  }
};
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
