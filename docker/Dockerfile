# Use Python 3.9 as base for backend
FROM python:3.9 AS backend

# Set backend working directory
WORKDIR /app

# Copy backend files
COPY backend ./backend

# Install backend dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Node.js for frontend build
RUN apt update && apt install -y curl && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt install -y nodejs

# Frontend build stage
FROM node:16 AS frontend
WORKDIR /app/frontend

# Copy frontend files correctly
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend ./  # Ensure all frontend files are copied
RUN npm run build

# Final stage - Serve React UI & Run Backend
FROM nginx:alpine

# Copy built frontend to Nginx web directory
COPY --from=frontend /app/frontend/build /usr/share/nginx/html

# Copy backend API files
COPY --from=backend /app /app

# Expose ports for API & Web UI
EXPOSE 80 8000

# Start Backend & Frontend Together
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
