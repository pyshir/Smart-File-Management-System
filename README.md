# 📁 Smart File Management System
## 👨‍💻 Author
**pyShir**
📱 WhatsApp: [+8801309495010](https://wa.me/8801309495010)

A Python-based **Smart File Management System** designed to organize, manage, track, and secure files efficiently. It provides an automated workspace with file categorization, metadata indexing, backup management, duplicate detection, and quarantine functionality.

---

## ✨ Features

- **Initialize Workspace** – Automatically creates the required directory structure.
- **Organize Files** – Sorts files into categories based on file extensions.
- **Scan Files** – Scans workspace files and updates metadata.
- **Search Files** – Search for files by their names.
- **View File Metadata** – Displays detailed file information.
- **Create Backup** – Creates backups of the SmartFileManager workspace.
- **List Backups** – Shows all available backups.
- **Restore Backup** – Restores workspace data from a selected backup.
- **Find Duplicate Files** – Identifies potential duplicate files based on file name and size.
- **File Quarantine** – Moves selected files into quarantine.
- **Restore Quarantined Files** – Restores files from quarantine to their original locations.
- **Operation History** – Keeps a record of completed operations.
- **Generate Report** – Generates a summary of the file management system.

---

## 🛠️ Technologies Used

- Python 3
- OS Module
- Shutil Module
- JSON
- CSV
- Pathlib
- Sys

---

## 📂 Project Directory Structure

After initializing the workspace, the following directory structure will be created:

```text
SmartFileManager/
│
├── workspace/
│   ├── documents/
│   ├── images/
│   ├── videos/
│   └── others/
│
├── backups/
│
├── metadata/
│   └── file_index.json
│
├── reports/
│   ├── operation_log.csv
│   └── inventory.csv
│
└── quarantine/
    └── data.json
```

---

## 🚀 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/pyShir/Smart-File-Management-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Smart-File-Management-System
```

### 3. Run the Program

```bash
python main.py
```

**Note:** Make sure Python 3 is installed on your system.

---

## 📋 Available Operations

When you run the program, you will see the following menu:

```text
========================================
    SMART FILE MANAGEMENT SYSTEM
========================================

1. Initialize Workspace
2. Organize Files
3. Scan Files
4. Search Files
5. View File Metadata
6. Create Backup
7. List Available Backups
8. Restore Backup
9. Find Duplicate Candidates
10. Move File to Quarantine
11. Restore from Quarantine
12. View Operation History
13. Generate Report
14. Exit
```

Select an option to perform the desired operation.

---

## ⚠️ Important Notes

- Initialize the workspace before using other operations.
- Place files inside the `SmartFileManager` directory before organizing them.
- Backup and restore operations should be performed carefully.
- Duplicate detection currently uses file names and file sizes.
- Quarantining a file moves it from its original location.
- Keep backup copies of important files before performing restore operations.

---

## 🔮 Future Improvements

- GUI-based file management interface.
- Advanced duplicate detection using file hashing.
- Support for more file formats.
- Automated scheduled backups.
- Improved error handling and logging.
- File encryption and password protection.

---

## 📜 License

This project is available for educational and personal use.

---

⭐ If you find this project useful, don't forget to give it a star!

**Developed with ❤️ by pyShir**
