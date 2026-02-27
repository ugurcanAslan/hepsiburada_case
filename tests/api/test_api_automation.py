import pytest


@pytest.mark.api
def test_swagger_generator_status_and_chained_get(api_client):
    get_languages = api_client.get("/gen/clients")
    assert get_languages.status_code == 200
    languages = get_languages.json()
    assert isinstance(languages, list) and languages

    language = "python" if "python" in languages else languages[0]
    payload = {"swaggerUrl": "https://petstore.swagger.io/v2/swagger.json", "options": {}}

    post_generate = api_client.post(f"/gen/clients/{language}", json_body=payload)
    assert post_generate.status_code == 200

    file_id = post_generate.json().get("code")
    assert file_id, "POST response does not contain file id code."

    download_generated = api_client.get(f"/gen/download/{file_id}")
    assert download_generated.status_code == 200
