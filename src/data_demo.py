from typing import TypedDict, Callable, TypeVar, Any, List, Dict
from collections import namedtuple
from dataclasses import dataclass
from pydantic import BaseModel
import numpy as np
from numpy.typing import NDArray
import time
import pandas as pd
import os
import json
import yaml  # Requires: pip install PyYAML


# ----------------------------
# User structures
# ----------------------------


class UserTypedDict(TypedDict):
    name: str
    age: int
    email: str


UserNamedTuple = namedtuple("UserNamedTuple", ["name", "age", "email"])


@dataclass
class UserDataclass:
    name: str
    age: int
    email: str


class UserPydantic(BaseModel):
    name: str
    age: int
    email: str


# ----------------------------
# Timing decorator
# ----------------------------

T = TypeVar("T")


def measure_time(func: Callable[..., T]) -> Callable[..., T]:
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start: float = time.time()
        result: T = func(*args, **kwargs)
        end: float = time.time()
        print(f"Execution time of {func.__name__}: {end - start:.6f} seconds")
        return result

    return wrapper


@measure_time
def example_function(n: int) -> int:
    return sum(range(n))


# ----------------------------
# CSV loader
# ----------------------------


def load_csv_to_dataframe(file_path: str) -> pd.DataFrame:
    try:
        print("Current working directory:", os.getcwd())
        print(f"Looking for {file_path} at:", os.path.abspath(file_path))
        df: pd.DataFrame = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure the file exists.")
        raise


# ----------------------------
# Main function
# ----------------------------


def main() -> None:
    # ---------------- User examples ----------------
    user_td_example: UserTypedDict = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com",
    }
    print(user_td_example)

    user_nt = UserNamedTuple(name="Alice", age=30, email="alice@example.com")
    print(user_nt)

    user_dc = UserDataclass(name="Alice", age=30, email="alice@example.com")
    print(user_dc)

    user_pd = UserPydantic(name="Alice", age=30, email="alice@example.com")
    print(user_pd)

    # ---------------- Python list vs NumPy ----------------
    python_list: list[int] = list(range(1, 6))
    print("Python list:", python_list)

    numpy_array: NDArray[np.int64] = np.array([1, 2, 3, 4, 5])
    print("NumPy array:", numpy_array)

    N: int = 1_000_000
    scalar: int = 2

    python_list = list(range(N))
    start = time.time()
    _ = [scalar * x for x in python_list]  # underscore avoids ruff F841
    end = time.time()
    print(f"Python list time: {end - start:.6f} seconds")

    numpy_array = np.arange(N)
    start = time.time()
    _ = scalar * numpy_array
    end = time.time()
    print(f"NumPy array time: {end - start:.6f} seconds")

    # ---------------- JSON ----------------
    json_file: str = os.path.join("src", "users.json")
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            json_data: List[Dict[str, Any]] = json.load(f)["users"]
            for user_data in json_data:
                json_user_td: UserTypedDict = {
                    "name": str(user_data["name"]),
                    "age": int(user_data["age"]),
                    "email": str(user_data["email"]),
                }
                json_user_dc = UserDataclass(
                    name=str(user_data["name"]),
                    age=int(user_data["age"]),
                    email=str(user_data["email"]),
                )
                print("JSON UserTypedDict:", json_user_td)
                print("JSON UserDataclass:", json_user_dc)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")

    # ---------------- YAML ----------------
    yaml_file: str = os.path.join("src", "users.yaml")
    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            yaml_content = yaml.safe_load(f)
            yaml_data: List[Dict[str, Any]] = yaml_content.get("users", [])
            for user_data in yaml_data:
                yaml_user_td: UserTypedDict = {
                    "name": str(user_data["name"]),
                    "age": int(user_data["age"]),
                    "email": str(user_data["email"]),
                }
                yaml_user_dc = UserDataclass(
                    name=str(user_data["name"]),
                    age=int(user_data["age"]),
                    email=str(user_data["email"]),
                )
                print("YAML UserTypedDict:", yaml_user_td)
                print("YAML UserDataclass:", yaml_user_dc)
    except FileNotFoundError:
        print(f"Error: {yaml_file} not found.")

    # ---------------- CSV ----------------
    csv_file: str = os.path.join("src", "user.csv")
    df: pd.DataFrame = load_csv_to_dataframe(csv_file)
    print(df)


if __name__ == "__main__":
    main()
