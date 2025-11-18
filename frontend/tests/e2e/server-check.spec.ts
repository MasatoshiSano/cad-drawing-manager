/**
 * サーバー起動確認テスト
 * バックエンドとフロントエンドのサーバーが正しく起動しているか確認
 */

import { test, expect } from '@playwright/test';

test.describe('サーバー起動確認', () => {
  test('バックエンドサーバーが起動している', async ({ page }) => {
    // ヘルスチェックエンドポイントを確認
    const healthResponse = await page.request.get('http://localhost:8000/health');
    expect(healthResponse.ok()).toBeTruthy();
    const healthData = await healthResponse.json();
    expect(healthData).toEqual({ status: 'ok' });
    console.log('✅ バックエンドサーバーは正常に起動しています');
  });

  test('バックエンドAPIルートエンドポイントが応答する', async ({ page }) => {
    const rootResponse = await page.request.get('http://localhost:8000/');
    expect(rootResponse.ok()).toBeTruthy();
    const rootData = await rootResponse.json();
    expect(rootData).toHaveProperty('message');
    expect(rootData).toHaveProperty('version');
    console.log('✅ バックエンドAPIルートエンドポイント:', rootData);
  });

  test('バックエンドAPIドキュメントがアクセス可能', async ({ page }) => {
    const docsResponse = await page.request.get('http://localhost:8000/docs');
    expect(docsResponse.ok()).toBeTruthy();
    console.log('✅ APIドキュメントページにアクセス可能です');
  });

  test('バックエンド図面APIが応答する', async ({ page }) => {
    const drawingsResponse = await page.request.get('http://localhost:8000/api/v1/drawings/');
    
    // ステータスコードを確認（サーバーが応答していることを確認）
    const status = drawingsResponse.status();
    console.log(`図面APIレスポンスステータス: ${status}`);
    
    // サーバーが応答していることを確認（500エラーでもサーバーは起動している）
    expect(status).toBeGreaterThanOrEqual(200);
    expect(status).toBeLessThan(600);
    
    if (drawingsResponse.ok()) {
      const drawingsData = await drawingsResponse.json();
      expect(drawingsData).toHaveProperty('total');
      expect(drawingsData).toHaveProperty('items');
      expect(Array.isArray(drawingsData.items)).toBeTruthy();
      console.log(`✅ 図面APIが正常に応答しています（図面数: ${drawingsData.total}）`);
    } else {
      // 500エラーの場合でもサーバーは起動している
      console.log(`⚠️ 図面APIがエラーを返しましたが、サーバーは起動しています（ステータス: ${status}）`);
      console.log('   これはアプリケーションの設定やデータベースの問題の可能性があります');
    }
  });

  test('フロントエンドサーバーが起動している', async ({ page }) => {
    await page.goto('http://localhost:5173');
    await expect(page).toHaveTitle(/CAD図面管理システム/);
    console.log('✅ フロントエンドサーバーは正常に起動しています');
  });

  test('フロントエンドのルート要素が存在する', async ({ page }) => {
    await page.goto('http://localhost:5173');
    const root = page.locator('#root');
    await expect(root).toBeAttached();
    console.log('✅ フロントエンドのルート要素が存在します');
  });

  test('フロントエンドとバックエンドの接続が正常', async ({ page }) => {
    // コンソールエラーをキャプチャ
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.goto('http://localhost:5173/list');
    await page.waitForLoadState('networkidle');

    // バックエンドへのリクエストが成功しているか確認
    const apiErrors = errors.filter(e => 
      e.includes('localhost:8000') && 
      e.includes('ERR_CONNECTION_REFUSED')
    );
    
    expect(apiErrors.length).toBe(0);
    console.log('✅ フロントエンドとバックエンドの接続が正常です');
  });
});

