import { normalizeResponse } from "@/services/helpers";

const API = import.meta.env.VITE_FETCHER_API;

export async function fetchPlaylistsByAuthor(channelId) {
  const response = await fetch(`${API}/author/${channelId}`);

  return normalizeResponse(response);
}

export async function fetchPlaylistMetadataById(id) {
  const response = await fetch(`${API}/meta/playlist/${id}`);

  return normalizeResponse(response);
}

export async function fetchAuthorMetadataById(id) {
  const response = await fetch(`${API}/meta/author/${id}`);

  return normalizeResponse(response);
}

export async function fetchLimitedPlaylistItemsById(
  id,
  offset = 0,
  limit = 10
) {
  const queryParams = new URLSearchParams({ offset, limit }).toString();
  const response = await fetch(`${API}/playlist/${id}?${queryParams}`);

  return normalizeResponse(response);
}
