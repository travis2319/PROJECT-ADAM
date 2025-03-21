import { useState, useCallback } from 'react';

interface UseFetchReturn<T> {
  data: T | null;
  loading: boolean;
  disabled: boolean;
  fetchData: () => Promise<void>;
}

export const useFetch = <T>(fetchFunction: () => Promise<T>): UseFetchReturn<T> => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [disabled, setDisabled] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setDisabled(true);
    try {
      const result = await fetchFunction();
      setData(result);
    } catch (error) {
      console.error('Fetch error:', error);
    } finally {
      setLoading(false);
      setDisabled(false);
    }
  }, [fetchFunction]);

  return { data, loading, disabled, fetchData };
};