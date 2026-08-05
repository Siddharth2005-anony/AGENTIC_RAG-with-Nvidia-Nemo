# =====================================================================
#  Dockerfile  (frontend) - React + Vite dev server
#
#  This replaces running:  npm run dev
#  (build context = the frontend-rag/react folder)
# =====================================================================

# Node 24 matches the Node version used on your local machine (v24.12.0).
FROM node:24-slim

WORKDIR /app

ENV NODE_ENV=development

# Install dependencies first (helps Docker layer caching).
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the frontend source.
COPY . .

# Port Vite's dev server runs on.
EXPOSE 5173

# Same as `npm run dev`, but forced to bind to 0.0.0.0 so the host
# browser can open http://localhost:5173.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]