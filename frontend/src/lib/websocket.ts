/**
 * WebSocket Client
 * 
 * Socket.IOを使用したWebSocketクライアント
 */

import { io, Socket } from 'socket.io-client';

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'http://localhost:8000';

interface DrawingEventData {
  type: 'locked' | 'unlocked';
  drawing_id: string;
  locked_by?: string;
}

type DrawingEventHandler = (data: DrawingEventData) => void;

class WebSocketClient {
  private socket: Socket | null = null;
  private subscriptions: Map<string, DrawingEventHandler[]> = new Map();

  /**
   * WebSocketに接続
   */
  connect(): void {
    if (this.socket?.connected) {
      return;
    }

    this.socket = io(`${WS_BASE_URL}/ws`, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    this.socket.on('connect', () => {
      console.log('[WebSocket] Connected');
    });

    this.socket.on('disconnect', () => {
      console.log('[WebSocket] Disconnected');
    });

    this.socket.on('drawing_locked', (data: { drawing_id: string; locked_by: string }) => {
      const handlers = this.subscriptions.get(data.drawing_id);
      if (handlers) {
        handlers.forEach((handler) => {
          handler({
            type: 'locked',
            drawing_id: data.drawing_id,
            locked_by: data.locked_by,
          });
        });
      }
    });

    this.socket.on('drawing_unlocked', (data: { drawing_id: string }) => {
      const handlers = this.subscriptions.get(data.drawing_id);
      if (handlers) {
        handlers.forEach((handler) => {
          handler({
            type: 'unlocked',
            drawing_id: data.drawing_id,
          });
        });
      }
    });

    this.socket.on('error', (error: any) => {
      console.error('[WebSocket] Error:', error);
    });
  }

  /**
   * WebSocketから切断
   */
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.subscriptions.clear();
    }
  }

  /**
   * 図面の変更を購読
   */
  subscribeDrawing(drawingId: string, handler: DrawingEventHandler): void {
    if (!this.socket?.connected) {
      this.connect();
    }

    // ハンドラーを登録
    if (!this.subscriptions.has(drawingId)) {
      this.subscriptions.set(drawingId, []);
    }
    this.subscriptions.get(drawingId)!.push(handler);

    // サーバーに購読を通知
    if (this.socket) {
      this.socket.emit('subscribe_drawing', { drawing_id: drawingId });
    }
  }

  /**
   * 図面の購読を解除
   */
  unsubscribeDrawing(drawingId: string): void {
    // ハンドラーを削除
    this.subscriptions.delete(drawingId);

    // サーバーに購読解除を通知
    if (this.socket) {
      this.socket.emit('unsubscribe_drawing', { drawing_id: drawingId });
    }
  }

  /**
   * 接続状態を確認
   */
  isConnected(): boolean {
    return this.socket?.connected ?? false;
  }
}

// シングルトンインスタンス
export const websocketClient = new WebSocketClient();

