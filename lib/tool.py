import os
import time
from typing import Any

import httpx
from fastmcp import FastMCP

GAMMA_API_BASE = "https://public-api.gamma.app/v1.0"
DEFAULT_TIMEOUT = float(os.getenv("GAMMA_HTTP_TIMEOUT", "30"))
DEFAULT_POLL_INTERVAL = float(os.getenv("GAMMA_POLL_INTERVAL_SECONDS", "2"))
DEFAULT_MAX_WAIT = float(os.getenv("GAMMA_MAX_WAIT_SECONDS", "180"))
DEFAULT_RETRIES = int(os.getenv("GAMMA_HTTP_RETRIES", "2"))
DEFAULT_RETRY_BACKOFF = float(os.getenv("GAMMA_HTTP_RETRY_BACKOFF_SECONDS", "1"))

TOOL_NAMES = [
    "generate_presentation",
    "create_from_template",
    "get_generation_status",
    "list_themes",
    "list_folders",
]


def _get_api_key() -> str:
    api_key = os.getenv("GAMMA_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GAMMA_API_KEY is missing. Add it to your environment or .env file."
        )
    return api_key


def _headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "accept": "application/json",
        "X-API-KEY": _get_api_key(),
    }


def _clean_payload(payload: dict[str, Any]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, dict):
            nested = _clean_payload(value)
            if nested:
                cleaned[key] = nested
            continue
        cleaned[key] = value
    return cleaned


def _error_from_response(response: httpx.Response) -> str:
    try:
        data = response.json()
        if isinstance(data, dict):
            return str(data.get("message") or data)
        return str(data)
    except Exception:
        return response.text or response.reason_phrase


def _request_json(
    method: str,
    path: str,
    *,
    json_body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{GAMMA_API_BASE}{path}"
    last_error: str | None = None

    for attempt in range(DEFAULT_RETRIES + 1):
        try:
            response = httpx.request(
                method=method,
                url=url,
                headers=_headers(),
                json=json_body,
                params=params,
                timeout=DEFAULT_TIMEOUT,
            )

            if response.status_code in {429, 500, 502, 503, 504}:
                last_error = (
                    f"Gamma temporary error ({response.status_code}): "
                    f"{_error_from_response(response)}"
                )
                if attempt < DEFAULT_RETRIES:
                    time.sleep(DEFAULT_RETRY_BACKOFF * (attempt + 1))
                    continue

            if not response.is_success:
                raise RuntimeError(
                    f"Gamma request failed ({response.status_code}): "
                    f"{_error_from_response(response)}"
                )
            return response.json()
        except httpx.TimeoutException as exc:
            last_error = f"Gamma request timeout: {exc}"
            if attempt < DEFAULT_RETRIES:
                time.sleep(DEFAULT_RETRY_BACKOFF * (attempt + 1))
                continue
            raise RuntimeError(last_error) from exc
        except httpx.RequestError as exc:
            last_error = f"Gamma network error: {exc}"
            if attempt < DEFAULT_RETRIES:
                time.sleep(DEFAULT_RETRY_BACKOFF * (attempt + 1))
                continue
            raise RuntimeError(last_error) from exc

    raise RuntimeError(last_error or "Unknown Gamma request error")


def _post_generation(endpoint: str, payload: dict[str, Any]) -> str:
    data = _request_json(
        "POST",
        endpoint,
        json_body=_clean_payload(payload),
    )
    generation_id = data.get("generationId")
    if not generation_id:
        raise RuntimeError(f"Gamma did not return generationId. Response: {data}")
    return generation_id


def _get_generation(generation_id: str) -> dict[str, Any]:
    return _request_json("GET", f"/generations/{generation_id}")


def _poll_generation(generation_id: str, max_wait_seconds: int) -> dict[str, Any]:
    elapsed = 0.0

    while elapsed <= max_wait_seconds:
        data = _get_generation(generation_id)
        status = data.get("status")

        if status == "completed":
            return data
        if status in {"failed", "error", "cancelled"}:
            raise RuntimeError(f"Gamma generation failed: {data}")

        time.sleep(DEFAULT_POLL_INTERVAL)
        elapsed += DEFAULT_POLL_INTERVAL

    raise TimeoutError(
        f"Gamma generation timed out after {max_wait_seconds}s. generationId={generation_id}"
    )


def _list_endpoint(
    endpoint: str,
    query: str | None = None,
    limit: int | None = None,
    after: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if query:
        params["query"] = query
    if limit is not None:
        params["limit"] = limit
    if after:
        params["after"] = after

    return _request_json("GET", f"/{endpoint}", params=params)


def register_tools(server: FastMCP) -> list[str]:
    @server.tool()
    def generate_presentation(
        input_text: str,
        text_mode: str = "generate",
        format: str = "presentation",
        theme_id: str | None = None,
        num_cards: int | None = 10,
        card_split: str | None = "auto",
        additional_instructions: str | None = None,
        folder_ids: list[str] | None = None,
        export_as: str | None = None,
        text_options: dict[str, Any] | None = None,
        image_options: dict[str, Any] | None = None,
        card_options: dict[str, Any] | None = None,
        sharing_options: dict[str, Any] | None = None,
        wait_for_completion: bool = True,
        max_wait_seconds: int = int(DEFAULT_MAX_WAIT),
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "inputText": input_text,
            "textMode": text_mode,
            "format": format,
            "themeId": theme_id,
            "numCards": num_cards,
            "cardSplit": card_split,
            "additionalInstructions": additional_instructions,
            "folderIds": folder_ids,
            "exportAs": export_as,
            "textOptions": text_options,
            "imageOptions": image_options,
            "cardOptions": card_options,
            "sharingOptions": sharing_options,
        }

        generation_id = _post_generation("/generations", payload)

        if not wait_for_completion:
            return {
                "generationId": generation_id,
                "status": "submitted",
                "message": "Use get_generation_status tool to check progress.",
            }

        return _poll_generation(generation_id, max_wait_seconds=max_wait_seconds)

    @server.tool()
    def create_from_template(
        gamma_id: str,
        prompt: str,
        theme_id: str | None = None,
        folder_ids: list[str] | None = None,
        export_as: str | None = None,
        image_options: dict[str, Any] | None = None,
        sharing_options: dict[str, Any] | None = None,
        wait_for_completion: bool = True,
        max_wait_seconds: int = int(DEFAULT_MAX_WAIT),
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "gammaId": gamma_id,
            "prompt": prompt,
            "themeId": theme_id,
            "folderIds": folder_ids,
            "exportAs": export_as,
            "imageOptions": image_options,
            "sharingOptions": sharing_options,
        }

        generation_id = _post_generation("/generations/from-template", payload)

        if not wait_for_completion:
            return {
                "generationId": generation_id,
                "status": "submitted",
                "message": "Use get_generation_status tool to check progress.",
            }

        return _poll_generation(generation_id, max_wait_seconds=max_wait_seconds)

    @server.tool()
    def get_generation_status(generation_id: str) -> dict[str, Any]:
        return _get_generation(generation_id)

    @server.tool()
    def list_themes(
        query: str | None = None,
        limit: int | None = None,
        after: str | None = None,
    ) -> dict[str, Any]:
        return _list_endpoint("themes", query=query, limit=limit, after=after)

    @server.tool()
    def list_folders(
        query: str | None = None,
        limit: int | None = None,
        after: str | None = None,
    ) -> dict[str, Any]:
        return _list_endpoint("folders", query=query, limit=limit, after=after)

    return TOOL_NAMES.copy()
