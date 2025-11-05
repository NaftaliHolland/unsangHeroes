import axiosInstance from "./axios";

export const fetchFeaturedStories = async () => {
  const { data } = await axiosInstance.get("/stories/featured");
  return data;
}
