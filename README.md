# Pose2Pose - Proof of Concept

A simple PoC project with Streamlit frontend that directly imports and uses Python backend functions. No API layer needed - keeping it simple!

## 🏗️ Project Structure

```
SUDOCODE_Pose2Pose/
├── backend/                    # Python backend functions
│   └── main.py                # Core processing functions
├── frontend/                   # Streamlit frontend
│   ├── app.py                 # Main Streamlit application
│   └── .streamlit/
│       └── config.toml        # Streamlit configuration
├── pyproject.toml             # Project dependencies (uv)
├── Dockerfile                 # Single container configuration
├── docker-compose.yml         # Docker orchestration (simplified)
├── Makefile                   # Convenient commands
├── .dockerignore             # Docker ignore patterns
├── .gitignore                # Git ignore patterns
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed (for containerized deployment)
- (Optional) UV package manager for local development

### Running with Docker (Recommended)

1. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

   Or using the Makefile:
   ```bash
   make docker-build
   make docker-up
   ```

2. **Access the application:**
   - Streamlit App: http://localhost:8501

3. **View logs:**
   ```bash
   make docker-logs
   ```

4. **Restart the application:**
   ```bash
   make docker-restart
   ```

5. **Stop the application:**
   ```bash
   make docker-down
   ```

### Running Locally (Development)

#### 1. Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Complete setup (recommended for new developers)

```bash
# One command to set up everything (installs uv + dependencies)
make setup
```

Or install manually:

```bash
# Install uv first (if not installed)
make install-uv

# Install all dependencies
make install

# Or directly with uv
uv sync
```

#### 3. Run the application

```bash
make dev
# or
make run
# or manually
cd frontend && streamlit run app.py
```

The application will be available at http://localhost:8501

## 🔧 How It Works

This PoC uses a **simplified architecture** perfect for quick prototyping:

### Architecture Overview

**Frontend** directly imports **Backend** functions - no HTTP requests needed!

```
User Input (Streamlit UI) 
    ↓
Direct Function Import
    ↓
Backend Functions (Python)
    ↓
Results Display (Streamlit)
```

### Backend Module (`backend/main.py`)

Pure Python functions that can be directly imported:

#### Available Functions

**`process_data(data: Dict[str, Any]) -> Dict[str, Any]`**
- Main data processing function
- Validates input data
- Calculates statistics for numeric values
- Returns structured results

**`transform_data(data: Dict[str, Any], operation: str) -> Dict[str, Any]`**
- Transform data with various operations:
  - `"uppercase"` - Convert string values to uppercase
  - `"lowercase"` - Convert string values to lowercase
  - `"double"` - Multiply numeric values by 2

**`validate_input(data: Dict[str, Any]) -> tuple[bool, Optional[str]]`**
- Validate input data before processing
- Returns validation status and error message

**`get_info() -> Dict[str, Any]`**
- Get module information
- List of available functions

### Frontend Application (`frontend/app.py`)

Streamlit-based interactive UI with:
- 🎨 Clean, modern interface
- 🔄 Real-time data processing
- 📊 Statistics and history tracking
- 🎯 Data transformation options
- 📈 Results visualization

#### Key Components

**Input Section:**
- JSON text area for data input
- Validation and error handling
- Example data provided

**Sidebar:**
- Backend module information
- Transformation options
- Configuration settings

**Main Area:**
- Data processing interface
- Results display with JSON formatting
- Status messages and feedback

**Statistics Panel:**
- Processing history
- Transformation usage stats
- Last result quick view

## 🛠️ Development Guide

### Adding New Backend Functions

1. **Add function to `backend/main.py`:**

```python
def my_custom_function(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Description of what this function does
    
    Args:
        data: Input data dictionary
        
    Returns:
        Processed result dictionary
    """
    # Your logic here
    return result
```

2. **Import and use in `frontend/app.py`:**

```python
from main import my_custom_function

result = my_custom_function(input_data)
```

3. **Update `get_info()` to include your new function in the list**

### Adding Frontend Features

#### New Input Widget

```python
# Add a new input widget
user_input = st.text_input("Enter value", "default")

# Use it in processing
data = {"user_value": user_input}
result = process_data(data)
```

#### New Visualization

```python
# Add charts or metrics
st.metric("Total Processed", len(history))
st.line_chart(data)
```

#### Using Session State

```python
# Access session state
if "history" not in st.session_state:
    st.session_state.history = []

# Store data
st.session_state.history.append(result)
```

### Testing Backend Functions

```bash
make test
# or
cd backend && python main.py
```

### Managing Dependencies

> **Note about UV commands**: This project uses `uv` for package management. UV automatically manages dependencies defined in `pyproject.toml` and creates a `uv.lock` file for reproducible installs. The `uv sync` command ensures your environment matches the lockfile.

#### Adding New Dependencies

```bash
# Method 1: Use uv add command (recommended)
uv add <package-name>
# This automatically updates pyproject.toml and uv.lock

# Method 2: Add to pyproject.toml manually, then sync
# Edit pyproject.toml to add under [project] dependencies:
# dependencies = [
#     "streamlit>=1.50.0",
#     "your-new-package>=1.0.0",
# ]
# Then run:
make sync
```

#### Updating Dependencies

```bash
# Check for outdated packages
make check-outdated

# Update all dependencies to latest versions
make lock-upgrade
# Or use the alias:
make update

# Just update the lockfile without upgrading
make lock

# Check if lockfile is up to date
make lock-check

# Update a specific package
uv add <package-name>@latest
```

#### Syncing Dependencies

```bash
# Sync environment with lockfile
make sync
# This runs: uv sync

# This ensures your environment exactly matches uv.lock
# which is generated from pyproject.toml
```

## 📝 Available Make Commands

Run `make help` to see all available commands:

### Setup & Installation
- `make setup` - **Complete setup for new developers** (installs uv + all dependencies)
- `make install-uv` - Install uv package manager
- `make install` - Install all dependencies from pyproject.toml

### Dependency Management
- `make sync` - Sync environment with lockfile
- `make lock` - Update uv.lock file
- `make lock-check` - Check if uv.lock is up to date
- `make lock-upgrade` - Upgrade all dependencies to latest versions
- `make update` - Update dependencies (alias for lock-upgrade)
- `make check-outdated` - Check for outdated packages

### Development
- `make dev` / `make run` - Run application locally
- `make test` - Test backend functions

### Docker
- `make docker-build` - Build Docker image
- `make docker-up` - Start the application
- `make docker-down` - Stop the application
- `make docker-restart` - Restart the application
- `make docker-logs` - View application logs

### Utilities
- `make clean` - Clean generated files and caches

## 🎨 Customization

### Streamlit Configuration

Edit `frontend/.streamlit/config.toml` to customize:
- Server settings (port, address)
- Browser behavior
- CORS and XSRF settings

### UI Customization

Edit `frontend/app.py` to modify:
- **Layout**: Change column widths, add sections
- **Styling**: Update page config, colors, themes
- **Widgets**: Add new input methods
- **Visualization**: Customize result displays

### Backend Logic

Edit `backend/main.py` to add:
- Custom processing functions
- Data transformations
- Validation rules
- Integration with external services

## 📦 Technology Stack

- **Frontend**: Streamlit 1.50+
- **Backend**: Pure Python functions (no framework needed!)
- **Package Manager**: UV (Astral)
- **Python**: 3.10+
- **Container**: Docker & Docker Compose
- **Testing**: pytest 8.4+
- **HTTP Client**: httpx 0.28+ (dev dependency)

## ✨ Key Features

- ✅ **Simple Architecture**: Direct function imports, no API overhead
- ✅ **Modular Structure**: Well-organized backend (core, utils) and frontend (components, pages, config)
- ✅ **Fast Development**: Make changes and see results immediately
- ✅ **Interactive UI**: Rich Streamlit interface with real-time feedback
- ✅ **Multi-Page App**: Main processing page + About + Documentation pages
- ✅ **Reusable Components**: Modular UI components for easy customization
- ✅ **Data Transformations**: Built-in transformation options (uppercase, lowercase, double)
- ✅ **Processing History**: Track and review past operations
- ✅ **Statistics Dashboard**: Visualize processing metrics
- ✅ **Docker Ready**: Easy containerized deployment
- ✅ **Development Mode**: Live reload with mounted volumes
- ✅ **Type Hints**: Full type annotations for better IDE support
- ✅ **Input Validation**: Built-in validation with helpful error messages
- ✅ **Session Management**: Centralized session state handling

## 🎓 Development Tips

### Streamlit Best Practices

1. **Auto-reload**: Streamlit automatically reloads on file changes
2. **Debugging**: Use `st.write()` to debug values
3. **Cache**: Use `@st.cache_data` for expensive operations
4. **State**: Use session state for data persistence
5. **Layout**: Use columns and expanders for organization

### Common Patterns

**Loading Spinner:**
```python
with st.spinner("Processing..."):
    result = process_data(data)
```

**Error Handling:**
```python
try:
    result = process_data(data)
    st.success("Success!")
except Exception as e:
    st.error(f"Error: {str(e)}")
```

**Conditional Display:**
```python
if condition:
    st.info("Information message")
else:
    st.warning("Warning message")
```

### Streamlit Components Reference

- `st.title()` - Page title
- `st.header()` / `st.subheader()` - Section headers
- `st.text_area()` - JSON input
- `st.button()` - Action triggers
- `st.selectbox()` - Dropdown selection
- `st.columns()` - Layout columns
- `st.json()` - JSON display
- `st.metric()` - Key metrics
- `st.spinner()` - Loading states
- `st.success()` / `st.error()` - Status messages

## 🔐 PoC Notes

This is designed as a **Proof of Concept** with simplicity in mind:

- Backend functions are directly imported (great for PoC, not for production microservices)
- No authentication/authorization (add if needed)
- Minimal error handling (expand as needed)
- In-memory state only (add database if needed)

### Why This Architecture?

**For PoC, direct function imports provide:**
- **Simplicity**: No HTTP overhead, routes, or middleware
- **Speed**: Direct function calls are faster
- **Debugging**: Easier to debug with direct calls
- **Development**: Faster iteration during development

**When to add an API layer:**
- When you need to separate services
- When scaling to multiple instances
- When supporting multiple clients
- When deploying services independently

### For Production Considerations:

1. Add proper error handling and logging
2. Implement authentication if needed
3. Add database integration for persistence
4. Consider API layer for service separation (FastAPI, Flask)
5. Add comprehensive test suite
6. Implement proper configuration management
7. Add monitoring and observability
8. Use environment variables for configuration
9. Add rate limiting if needed
10. Implement proper security measures

## 🐛 Troubleshooting

### Port already in use
If port 8501 is already in use, modify the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"  # Use port 8502 instead
```

### Import errors in Streamlit
Make sure the backend path is correctly added in `frontend/app.py`. The code handles this automatically by adding the parent backend directory to `sys.path`.

### Dependencies not found
Run `make install` to ensure all dependencies are installed:
```bash
make install
```

### Docker build issues
Clean up and rebuild:
```bash
make clean
make docker-build
make docker-up
```

### Clean up caches
If you encounter issues with Python caches:
```bash
make clean
```

## 💡 Quick Start for New Developers

### First Time Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd SUDOCODE_Pose2Pose

# Run complete setup (installs everything you need)
make setup

# Start the application
make dev
```

### Example Usage

1. **Open the app** at http://localhost:8501
2. **Enter JSON data** in the input field (example provided):
   ```json
   {"name": "example", "value": 42, "score": 85.5}
   ```
3. **Select a transformation** (optional) from the sidebar
4. **Click "Process Data"** to see results
5. **View statistics** and history in the right column

## 📚 Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Components](https://streamlit.io/components)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Docker Documentation](https://docs.docker.com/)

## 🎯 Next Steps

### Immediate Enhancements:
1. Add your specific business logic to `backend/main.py`
2. Customize the UI in `frontend/app.py`
3. Add more transformation options
4. Test with your actual data

### Future Enhancements:
1. Add file upload functionality (CSV, JSON, images)
2. Integrate with external APIs or services
3. Add data persistence (SQLite, PostgreSQL)
4. Implement authentication and user management
5. Add more visualization options (charts, graphs)
6. Create data export functionality
7. Add comprehensive test suite (pytest)
8. Implement logging and monitoring
9. Add configuration management
10. Consider API layer if needed (FastAPI)

---

**Built with ❤️ using Streamlit and Python | PoC Version 1.0.0**
