export const fetchCamera = async () => {
  try {
    const resp = await fetch(`${process.env.VUE_APP_BASE_URL}/cameras`);

    if (resp.status !== 200) throw await resp.text();

    return (await resp.json()) as any[];
  } catch (e) {
    console.error(e);
    return [];
  }
};

export const fetchSnapshots = async () => {
  try {
    const resp = await fetch(`${process.env.VUE_APP_BASE_URL}/snapshots`);

    if (resp.status !== 200) throw await resp.text();

    return (await resp.json()) as any[];
  } catch (e) {
    console.error(e);
    return [];
  }
};
