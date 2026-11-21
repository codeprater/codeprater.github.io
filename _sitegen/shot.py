import sys, asyncio
from playwright.async_api import async_playwright
async def main(pages):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for path, name, w, h, full in pages:
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            await pg.goto("http://localhost:8765" + path, wait_until="networkidle")
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=f"/home/claude/shots/{name}.png", full_page=full)
            await pg.close()
        await b.close()
import os; os.makedirs("/home/claude/shots", exist_ok=True)
specs=[]
for a in sys.argv[1:]:
    path,name,w,h,full=a.split(",")
    specs.append((path,name,int(w),int(h),full=="1"))
asyncio.run(main(specs))
