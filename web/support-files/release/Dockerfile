FROM node:18-alpine AS builder

WORKDIR /app

RUN npm install -g pnpm
ADD . .

RUN cat > pnpm-workspace.yaml <<EOF
packages:
  - 'src/app/*'
EOF

RUN cat > .env.local <<EOF
NEXTAPI_URL="http://bklite-server:8000"
EOF

RUN pnpm install
RUN pnpm run build

FROM node:18-alpine
RUN npm install -g pnpm
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

CMD ["pnpm", "run", "start"]