import httpx
from pathlib import Path
from dotenv import dotenv_values
import json

config = dotenv_values(".env")


def _execute(
    query_name: str,
    id: str,
    variables: dict[str, str],
    export_name_suffix: str = "",
):
    query = Path(f"./lattice_export/queries/{query_name}.graphql").read_text()
    data = {
        "id": "CompetencyViewQuery",
        "query": query,
        "variables": variables,
    }
    with httpx.Client() as client:
        try:
            response = client.post(
                "https://torchbox.latticehq.com/graphql",
                json=data,
                cookies={
                    "access_token": config["LATTICE_ACCESS_TOKEN"],
                },
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.UNAUTHORIZED:
                print(
                    "Unauthorized access. You might need to refresh the Access Token. "
                    "Please check the README for guidance."
                )
            elif e.response.status_code == httpx.codes.NOT_FOUND:
                print(
                    "The requested resource was not found. Please check the URL and try again."
                )
            else:
                print(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.reason_phrase}"
                )

            try:
                error_details = e.response.json()
                print(f"Error details: {error_details}")
            except json.JSONDecodeError:
                print("Unable to decode the error response as JSON.")
            except Exception as error_parsing_exception:
                print(
                    f"Unexpected error while parsing error response: {error_parsing_exception}"
                )

            raise e

        return data


def get_competencies():
    response = _execute(
        query_name="competency-view",
        id="CompetencyViewQuery",
        variables={
            "userEntityId": config["LATTICE_USER_ENTITY_ID"],
        },
    )
    return response
