// TODO: cache !?!?

export const load = async ({ fetch }) => {
  const res = await fetch("https://pigeonblog-db-default-rtdb.firebaseio.com/measurements.json");
  const _measurements = await res.json();
  const measurements = Object.keys(_measurements).map(k => _measurements[k]);
  return { measurements };
};
