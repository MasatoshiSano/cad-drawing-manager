/**
 * アプリケーションスクリーンショット取得テスト
 */

import { test, expect } from '@playwright/test';

test.describe('アプリケーションスクリーンショット', () => {
  test('アップロードページのスクリーンショット', async ({ page }) => {
    await page.goto('http://localhost:5173/upload');
    await page.waitForLoadState('networkidle');
    
    // ページが正しく読み込まれたことを確認
    await expect(page).toHaveTitle(/CAD図面管理システム/);
    
    // スクリーンショットを撮影
    await page.screenshot({
      path: 'screenshots/app-upload-page.png',
      fullPage: true
    });
    
    console.log('✅ アップロードページのスクリーンショットを保存しました: screenshots/app-upload-page.png');
  });

  test('一覧ページのスクリーンショット', async ({ page }) => {
    await page.goto('http://localhost:5173/list');
    await page.waitForLoadState('networkidle');
    
    // ページが正しく読み込まれたことを確認
    await expect(page).toHaveTitle(/CAD図面管理システム/);
    
    // 少し待機してコンテンツが読み込まれるのを待つ
    await page.waitForTimeout(2000);
    
    // スクリーンショットを撮影
    await page.screenshot({
      path: 'screenshots/app-list-page.png',
      fullPage: true
    });
    
    console.log('✅ 一覧ページのスクリーンショットを保存しました: screenshots/app-list-page.png');
  });

  test('検索ページのスクリーンショット', async ({ page }) => {
    await page.goto('http://localhost:5173/search');
    await page.waitForLoadState('networkidle');
    
    // ページが正しく読み込まれたことを確認
    await expect(page).toHaveTitle(/CAD図面管理システム/);
    
    // スクリーンショットを撮影
    await page.screenshot({
      path: 'screenshots/app-search-page.png',
      fullPage: true
    });
    
    console.log('✅ 検索ページのスクリーンショットを保存しました: screenshots/app-search-page.png');
  });

  test('APIが正常に動作していることを確認', async ({ page }) => {
    // 図面APIをテスト
    const response = await page.request.get('http://localhost:8000/api/v1/drawings/');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data).toHaveProperty('total');
    expect(data).toHaveProperty('items');
    expect(Array.isArray(data.items)).toBeTruthy();
    
    console.log(`✅ APIが正常に動作しています（図面数: ${data.total}）`);
  });
});

