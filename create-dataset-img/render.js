// start static server on site folder on port 3030 before running this script
const fs = require('fs');
const puppeteer = require('puppeteer');

const LETTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
const SIZE = 28;

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:3030');
    // create results folder
    try { fs.mkdirSync(`out`); } catch(err) {}
    for (let i = 0; i < LETTERS.length; i++) {
        const l = LETTERS[i];
        try { fs.mkdirSync(`out/${l}_${i}`); } catch(err) {}
    }
    for (let i = 0; i < 1320; i++) {
        const font_id = `font_${i}`
        await page.evaluate(`document.body.style.fontFamily = "${font_id}"`);
        for (let j = 0; j < LETTERS.length; j++) {
            const l = LETTERS[j];
            await page.evaluate(`document.body.innerHTML = "${l}"`);
            const png_path = `out/${l}_${j}/${font_id}.png`;
            await page.screenshot({ path: png_path , clip: { x: 0, y: 0, width: SIZE, height: SIZE }});
            console.log(png_path)
        }
    }
    await browser.close();
})();