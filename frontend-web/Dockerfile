FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/node:20-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# 构建时传入 API 地址
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
