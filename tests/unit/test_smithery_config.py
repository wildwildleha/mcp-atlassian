"""Test smithery.yaml configuration validation."""

import json
import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml


def load_smithery_config():
    """Load the smithery.yaml configuration."""
    smithery_path = Path(__file__).parent.parent.parent / "smithery.yaml"
    with open(smithery_path) as f:
        return yaml.safe_load(f)


def test_smithery_config_exists():
    """Test that smithery.yaml exists and is valid YAML."""
    smithery_path = Path(__file__).parent.parent.parent / "smithery.yaml"
    assert smithery_path.exists(), "smithery.yaml should exist"

    config = load_smithery_config()
    assert config is not None, "smithery.yaml should be valid YAML"
    assert "startCommand" in config, "Should have startCommand section"


def test_smithery_config_schema_has_anyof():
    """Test that schema uses anyOf to allow flexible configuration."""
    config = load_smithery_config()
    schema = config["startCommand"]["configSchema"]

    assert "anyOf" in schema, "Schema should have anyOf for flexible requirements"
    assert len(schema["anyOf"]) >= 4, "Should have at least 4 auth combinations"


def test_smithery_config_basic_auth_requirements():
    """Test that basic auth requires both username and apiToken."""
    config = load_smithery_config()
    schema = config["startCommand"]["configSchema"]

    # Check that one of the anyOf options requires username + apiToken
    has_jira_basic = any(
        set(option.get("required", [])) == {"jiraUrl", "jiraUsername", "jiraApiToken"}
        for option in schema["anyOf"]
    )
    has_confluence_basic = any(
        set(option.get("required", []))
        == {"confluenceUrl", "confluenceUsername", "confluenceApiToken"}
        for option in schema["anyOf"]
    )

    assert has_jira_basic, "Should require jiraUrl, jiraUsername, and jiraApiToken together"
    assert (
        has_confluence_basic
    ), "Should require confluenceUrl, confluenceUsername, and confluenceApiToken together"


def test_smithery_config_pat_requirements():
    """Test that PAT auth requires URL and personal token."""
    config = load_smithery_config()
    schema = config["startCommand"]["configSchema"]

    # Check that one of the anyOf options requires URL + personalToken
    has_jira_pat = any(
        set(option.get("required", [])) == {"jiraUrl", "jiraPersonalToken"}
        for option in schema["anyOf"]
    )
    has_confluence_pat = any(
        set(option.get("required", []))
        == {"confluenceUrl", "confluencePersonalToken"}
        for option in schema["anyOf"]
    )

    assert has_jira_pat, "Should require jiraUrl and jiraPersonalToken together"
    assert (
        has_confluence_pat
    ), "Should require confluenceUrl and confluencePersonalToken together"


def test_smithery_config_property_descriptions():
    """Test that properties have clear descriptions."""
    config = load_smithery_config()
    properties = config["startCommand"]["configSchema"]["properties"]

    # Check key properties have descriptions
    assert (
        "description" in properties["confluenceUsername"]
    ), "confluenceUsername should have description"
    assert (
        "description" in properties["confluenceApiToken"]
    ), "confluenceApiToken should have description"
    assert (
        "description" in properties["jiraUsername"]
    ), "jiraUsername should have description"
    assert (
        "description" in properties["jiraApiToken"]
    ), "jiraApiToken should have description"

    # Check that basic auth descriptions mention they're required together
    assert (
        "Required with" in properties["confluenceUsername"]["description"]
        or "For Basic Auth" in properties["confluenceUsername"]["description"]
    ), "confluenceUsername description should mention basic auth requirement"
    assert (
        "Required with" in properties["jiraUsername"]["description"]
        or "For Basic Auth" in properties["jiraUsername"]["description"]
    ), "jiraUsername description should mention basic auth requirement"


def test_smithery_config_password_format():
    """Test that sensitive fields use password format."""
    config = load_smithery_config()
    properties = config["startCommand"]["configSchema"]["properties"]

    # All token/password fields should have format: password
    assert (
        properties["confluenceApiToken"].get("format") == "password"
    ), "confluenceApiToken should use password format"
    assert (
        properties["confluencePersonalToken"].get("format") == "password"
    ), "confluencePersonalToken should use password format"
    assert (
        properties["jiraApiToken"].get("format") == "password"
    ), "jiraApiToken should use password format"
    assert (
        properties["jiraPersonalToken"].get("format") == "password"
    ), "jiraPersonalToken should use password format"


def test_smithery_command_function_syntax():
    """Test that commandFunction is valid JavaScript syntax."""
    config = load_smithery_config()
    command_func = config["startCommand"]["commandFunction"]

    # Basic syntax checks
    assert "(config)" in command_func, "Function should accept config parameter"
    assert "return" in command_func, "Function should have return statement"
    assert "command:" in command_func, "Should return command property"
    assert "env:" in command_func, "Should return env property"


def test_smithery_env_mapping():
    """Test that environment variables are properly mapped."""
    config = load_smithery_config()
    command_func = config["startCommand"]["commandFunction"]

    # Check key environment variable mappings exist
    assert "CONFLUENCE_URL" in command_func
    assert "CONFLUENCE_USERNAME" in command_func
    assert "CONFLUENCE_API_TOKEN" in command_func
    assert "JIRA_URL" in command_func
    assert "JIRA_USERNAME" in command_func
    assert "JIRA_API_TOKEN" in command_func


@pytest.mark.parametrize(
    "env_vars,should_work",
    [
        # Valid Confluence basic auth
        (
            {
                "CONFLUENCE_URL": "https://confluence.example.com",
                "CONFLUENCE_USERNAME": "user",
                "CONFLUENCE_API_TOKEN": "pass",
            },
            True,
        ),
        # Valid Jira basic auth
        (
            {
                "JIRA_URL": "https://jira.example.com",
                "JIRA_USERNAME": "user",
                "JIRA_API_TOKEN": "pass",
            },
            True,
        ),
        # Valid Confluence PAT
        (
            {
                "CONFLUENCE_URL": "https://confluence.example.com",
                "CONFLUENCE_PERSONAL_TOKEN": "token",
            },
            True,
        ),
        # Invalid: URL without credentials
        ({"CONFLUENCE_URL": "https://confluence.example.com"}, False),
        # Invalid: Username without token
        (
            {
                "CONFLUENCE_URL": "https://confluence.example.com",
                "CONFLUENCE_USERNAME": "user",
            },
            False,
        ),
        # Invalid: Token without username (for basic auth)
        (
            {
                "CONFLUENCE_URL": "https://confluence.example.com",
                "CONFLUENCE_API_TOKEN": "pass",
            },
            False,
        ),
    ],
)
def test_environment_validation(env_vars, should_work):
    """Test that environment configurations are properly validated."""
    from mcp_atlassian.utils.environment import get_available_services

    with patch.dict(os.environ, env_vars, clear=True):
        services = get_available_services()

        if "CONFLUENCE" in str(env_vars):
            if should_work:
                assert (
                    services["confluence"]
                ), f"Confluence should be setup with {env_vars}"
            else:
                assert (
                    not services["confluence"]
                ), f"Confluence should not be setup with incomplete config {env_vars}"

        if "JIRA" in str(env_vars):
            if should_work:
                assert services["jira"], f"Jira should be setup with {env_vars}"
            else:
                assert (
                    not services["jira"]
                ), f"Jira should not be setup with incomplete config {env_vars}"


def test_docker_compose_example_matches_smithery():
    """Test that docker-compose.example.yml uses valid environment variables."""
    docker_compose_path = (
        Path(__file__).parent.parent.parent / "docker-compose.example.yml"
    )

    if not docker_compose_path.exists():
        pytest.skip("docker-compose.example.yml not found")

    with open(docker_compose_path) as f:
        content = f.read()

    # Check that basic auth examples set both username and password
    assert (
        "CONFLUENCE_USERNAME" in content
    ), "Should have CONFLUENCE_USERNAME in examples"
    assert (
        "CONFLUENCE_API_TOKEN" in content
    ), "Should have CONFLUENCE_API_TOKEN in examples"
    assert "JIRA_USERNAME" in content, "Should have JIRA_USERNAME in examples"
    assert "JIRA_API_TOKEN" in content, "Should have JIRA_API_TOKEN in examples"
