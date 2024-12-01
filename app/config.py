from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = ROOT_DIR / "secrets" / ".env"
SWAGGER_TEMPLATE_FILEPATH = ROOT_DIR / "swagger" / "base.yml"
