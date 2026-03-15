# Stage 1: Build the React application
FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Stage 2: Serve the application using Nginx
FROM nginx:alpine

# Copy built files from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
