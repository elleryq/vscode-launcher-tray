from .config import Config
from .project_dialog import ProjectDialog
from .manage_dialog import ManageDialog
from .main import main

__all__ = ["Config", "ProjectDialog", "ManageDialog", "main"]


if __name__ == '__main__':
    main()