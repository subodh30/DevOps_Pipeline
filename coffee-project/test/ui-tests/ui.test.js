const puppeteer = require('puppeteer');
const assert = require('assert');

(async () => {
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Navigate to the website URL
    await page.goto('http://152.7.177.44:3000/'); // Replace with your website URL

    // Wait for the button with text 'Order' to be visible and clickable
    const orderButton = await page.waitForXPath('//button[contains(text(), "Order")]');
    await orderButton.click();

    // Wait for the alert to appear
    const alert = await new Promise(resolve => page.on('dialog', resolve));

    // Get the alert text
    const alertText = alert.message();

    // Validate the alert text
    assert.ok(alertText.startsWith('Ordered'), 'Alert text does not start with "Ordered"');

    console.log('Alert with text starting "Ordered" is visible.');

    await alert.dismiss();
    await browser.close();
  } catch (error) {
    console.error('Error:', error);
    process.exit(1); // Exit with a non-zero status code to indicate test failure
  }
})();
