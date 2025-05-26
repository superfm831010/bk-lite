FROM node:18-alpine AS builder

WORKDIR /app

RUN npm install -g pnpm
ADD . .

RUN cat > pnpm-workspace.yaml <<EOF
packages:
  - 'src/app/*'
EOF

RUN cat > .env.local <<EOF
NEXTAPI_INSTALL_APP="system-manager"
NEXT_PUBLIC_CLIENT_ID="system-manager"
NEXTAPI_URL="http://system-manager:8000"
EOF

RUN cd ./src/app && \
    find . -mindepth 1 -maxdepth 1 -type d ! \( -name \(core\) -o -name no-permission -o -name "system-manager" \) -print0 | xargs -0 rm -rf

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