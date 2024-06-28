import { UTListFileUrl } from "@/lib/constants";
import { zip } from "@/lib/utils";
import { UTImage } from "@/types/api";
import { useEffect, useState } from "react";
import useFetchData from "./useFetchData";

/**
 * A React hook for retrieving image names and URLs from the connected uploadthing bucket.
 * @param imgNames a string of image names found in the uploadthing bucket separated by commas
 * @returns an array of UTImage objects
 * @example
 * {imgData, isLoading, error} = useFetchImgs("wall-of-stone,wall-of-thorns");
 */
const useFetchImgs = (imgNames: string) => {
  const [imgData, setImgData] = useState<UTImage[]>([]);

  const { data, isLoading, error } = useFetchData(
    `${UTListFileUrl}?filenames=${imgNames}`,
    {
      headers: {
        Accept: "application/json",
        method: "GET",
      },
    }
  );

  useEffect(() => {
    if (!imgNames) {
      return;
    }

    if (data) {
      const urlTemplate = `https://utfs.io/a/${process.env.NEXT_PUBLIC_UPLOADTHING_APP_ID}`;

      const result = zip(imgNames.split(","), data);

      let imgUrls: UTImage[] = [];
      result.map(([name, url]) => {
        imgUrls.push({
          name: name,
          url: `${urlTemplate}/${url}`,
        });
      });

      setImgData(imgUrls);
    }
  }, [imgNames, data]);

  return { imgData, isLoading, error };
};

export default useFetchImgs;
