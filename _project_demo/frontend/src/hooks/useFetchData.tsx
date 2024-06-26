import { useEffect, useState } from "react";

/**
 * A React hook for fetching data from a URL using the [Next.js FetchAPI](https://nextjs.org/docs/app/api-reference/functions/fetch).
 * @param url the URL to retrieve data from
 * @param options an optional object of configuration options
 * @returns a set of data based on a given type, a boolean flag stating the loading status, and an error object (if any)
 * @example
 * {data, isLoading, error} = useFetchData<FancyData[]>("https://example.com?page=1&per_page=20");
 */
const useFetchData = <T,>(
  url: string,
  options: object = {}
) => {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) {
      return;
    }

    const fetchData = async (
      url: string,
      options: object = {}
    ) => {
      try {
        const response = await fetch(url, options);

        if (response.ok) {
          const result = await response.json();
          setData(result);
        }
      } catch (error: any) {
        console.error("Error fetching data:", error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData(url, options);
  }, [url]);

  return { data, isLoading, error };
};

export default useFetchData;
