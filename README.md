# Blender Landmark Generator

將照片參考的建築或園區，製作成 **Blender 模型、GLB 與可離線開啟的互動 HTML** 的 Codex skill。

附帶高雄市立美術館範例：館體、斜面採光頂、半圓迴廊、廣場、湖岸與示意植栽。網頁支援視角切換、光照、白模、圖層顯示與 PNG／GLB 下載。

## 安裝到 Codex

將本儲存庫複製到個人技能目錄：

```powershell
git clone https://github.com/bigtongue5566/blender-landmark-generator.git "$env:USERPROFILE\.codex\skills\blender-landmark-generator"
```

如果同名技能已存在，先比對內容，不要覆蓋本機修改。也可安裝到專案的 `.agents/skills/blender-landmark-generator`。

## 使用

```text
使用 $blender-landmark-generator，參考照片製作臺南市美術館，並輸出互動 HTML。
```

技能入口：[SKILL.md](SKILL.md)。需要 Blender、Python 與 Node.js；可使用已連線的 Blender MCP，或 Blender 背景 Python 模式。

建立獨立高美館範例專案：

```powershell
python scripts/scaffold.py C:\Projects\kmfa-demo
```

腳本拒絕覆寫非空目錄。後續建模與打包步驟見產生專案中的 README。範例使用 Three.js 與 esbuild，保留 npm lockfile；完成打包的 HTML 不依賴 CDN。

## 範圍與驗證

- 這是可重用的建模工作流程及具體範例，不是輸入任意名稱就能精確重建的通用參數模型。
- 高美館為照片推估的外觀模型，並非館方官方模型或測繪成果；植栽與雕塑為情境元素。
- 已驗證技能格式、腳本語法、範例複製完整性及拒絕覆寫行為。每次建模仍需重新執行 Blender、GLB 與 HTML 檢查；不宣稱最新版模板已完成所有瀏覽器互動測試。
- 不包含已生成的 `.blend`／GLB 成品、第三方照片、帳號設定或憑證。

建築資料來源與互動概念參考見 [範例設計說明](assets/kmfa-starter/DESIGN.md)。
