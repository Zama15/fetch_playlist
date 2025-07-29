export async function normalizeResponse(response) {
  const { status, ok } = response;

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    // Just leave payload as it is
  }

  return {
    ok,
    status,
    message: ok ? payload?.error || "Unknown error" : null,
    data: payload,
  };
}
