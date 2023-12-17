FROM node:17-alpine as builder
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL="${REACT_APP_API_URL}"
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.19.0
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
