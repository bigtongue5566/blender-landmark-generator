# Blender Landmark Generator

結合 **Google Earth、Google Maps 街景與照片**，將建築或園區製作成 **Blender 模型、GLB 與可離線開啟的互動 HTML** 的 Codex skill。

Earth 俯視與旋轉斜視用於核對棟體寬深、屋頂、退縮及中庭；街景用於核對立面、入口、圍牆與地下車道。流程先驗證粗模比例，再加入細節，保留來源日期與近似尺寸說明。詳見 [Earth 與街景建模](references/google-earth-street-view.md)。

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

也可提供指定位置與修正重點：

```text
使用 $blender-landmark-generator，依我提供的 Google Earth 連結與 Google Maps 街景重建這座建築。
先核對各棟寬深、屋頂凹口、中庭及地下車道，再製作立面；交付 Blender、GLB、離線 HTML 和來源／尺寸推估說明。
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
- 地圖參考流程需實際查看可用影像；無 3D 或街景覆蓋時使用其他照片並註明缺少的角度。Earth 平面量測與影像推估不等於測繪，也不能直接提供樓高或地下落差。
- 以參考影像建立原創幾何，不需要 Google API 金鑰或下載 Google 的原始 3D 網格。
- 已驗證技能格式、腳本語法、範例複製完整性及拒絕覆寫行為。每次建模仍需重新執行 Blender、GLB 與 HTML 檢查；不宣稱最新版模板已完成所有瀏覽器互動測試。
- 不包含已生成的 `.blend`／GLB 成品、第三方照片、帳號設定或憑證。

建築資料來源與互動概念參考見 [範例設計說明](assets/kmfa-starter/DESIGN.md)。
