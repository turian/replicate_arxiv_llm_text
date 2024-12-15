# `cog.yaml` Configuration Summary

This document provides a concise summary of all the permissible configuration options available in the `cog.yaml` file. Use this as a quick reference to understand how to set up your model configurations correctly.

## `build`

The `build` section describes how to build the Docker image for your model. It includes the following options:

- **`gpu`** (boolean):
  - **Purpose**: Enables GPU support when set to `true`.
  - **Default**: `false`
  - **Example**:
    ```yaml
    build:
      gpu: true
    ```

- **`python_version`** (string):
  - **Purpose**: Specifies the minor or patch version of Python to use (e.g., `'3.11'` or `'3.11.1'`).
  - **Default**: `'3.11'`
  - **Example**:
    ```yaml
    build:
      python_version: '3.11.1'
    ```

- **`python_packages`** (list of strings):
  - **Purpose**: A list of Python packages to install from PyPI, specified in the format `package==version`.
  - **Cannot be used simultaneously with `python_requirements`.**
  - **Example**:
    ```yaml
    build:
      python_packages:
        - requests==2.25.1
        - numpy==1.19.5
    ```

- **`python_requirements`** (string):
  - **Purpose**: Path to a `requirements.txt` file specifying Python packages to install.
  - **Cannot be used simultaneously with `python_packages`.**
  - **Example**:
    ```yaml
    build:
      python_requirements: requirements.txt
    ```

- **`system_packages`** (list of strings):
  - **Purpose**: A list of Ubuntu APT packages to install.
  - **Example**:
    ```yaml
    build:
      system_packages:
        - git
        - ffmpeg
    ```

- **`run`** (list of strings or dictionaries):
  - **Purpose**: A list of shell commands to run during the build process. Can include environment variable settings and other setup commands.
  - **Example**:
    ```yaml
    build:
      run:
        - export ENV_VAR=value
        - apt-get update && apt-get install -y some-package
    ```

#### **Setting Environment Variables**

- **Purpose:** Include environment variables inline in the commands within the `run` section.
- **Note:** Using `export` may not work as expected because each command in the `run` section is executed in a separate shell environment.
- **How to Set Variables Inline:** Prepend the variables to the command, separated by spaces.

- **Example:**

  ```yaml
  build:
    run:
      - VAR1=value1 VAR2=value2 command_here arg1 arg2
  ```

- **Multiline Command Example:**

  ```yaml
  build:
    run:
      - |
        VAR1=value1 \
        VAR2=value2 \
        command_here arg1 arg2
  ```

- **Explanation:**
  - Environment variables `VAR1` and `VAR2` are set only for the duration of `command_here`.
  - This method ensures variables are available when needed without affecting other commands.

## `image`

- **`image`** (string):
  - **Purpose**: Specifies the name of the Docker image to be built. If pushing to a registry, include the registry name.
  - **Example**:
    ```yaml
    image: 'registry.example.com/username/model-name'
    ```

## `predict`

- **`predict`** (string):
  - **Purpose**: Points to the `Predictor` class in your code that defines how predictions are run. Format: `'file.py:PredictorClassName'`.
  - **Example**:
    ```yaml
    predict: 'predict.py:Predictor'
    ```

---

*This summary serves as a quick reference for configuring `cog.yaml`. Ensure to follow the structure and examples to set up your model configurations effectively.*
