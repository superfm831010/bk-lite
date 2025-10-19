# 修改页面左上角Banner文字

## 修改目的
将页面左上角的banner文字从"BlueKing Lite"改为"黄埔AI运维"，实现定制化品牌展示。

## 修改位置
- **文件路径**: `web/src/components/top-menu/index.tsx`
- **修改行数**: 第234行

## 修改内容

### 修改前
```tsx
<div className="font-medium">BlueKing Lite</div>
```

### 修改后
```tsx
<div className="font-medium">黄埔AI运维</div>
```

## 相关定制化修改
1. 页面标题（浏览器标签页）: 已改为"黄埔海关智能运维平台" (在 `web/src/app/layout.tsx:117`)
2. 运维控制台描述: 已定制为"黄埔海关智能运维控制台" (在 `web/src/app/ops-console/locales/zh.json`)

## 验证方式
1. 启动Web开发服务器: `cd web && pnpm dev`
2. 访问页面后，查看左上角logo旁边的文字是否显示为"黄埔AI运维"

## 注意事项
- 修改后需要重启Web服务才能看到效果
- 此修改仅影响前端页面显示，不影响系统后端逻辑
