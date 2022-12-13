export const fetchCameras = async () => {
  try {
    const resp = await fetch(`${process.env.VUE_APP_BASE_URL}/cameras`);

    if (resp.status !== 200) {
      throw await resp.text();
    }

    return await resp.json();
  } catch (e) {
    return [];
  }
};
