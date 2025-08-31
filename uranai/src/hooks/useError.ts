"use client";

import { useState, useCallback } from 'react';

export function useError() {
  const [error, setError] = useState<string | null>(null);

  const handleError = useCallback((error: string) => {
    setError(error);
    // 3秒後にエラーメッセージをクリア
    setTimeout(() => setError(null), 3000);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return { error, handleError, clearError };
}
